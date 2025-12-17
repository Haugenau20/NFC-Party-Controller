# Dashboard Integration Guide
## Connecting Your Vite + React + TypeScript Dashboard to Home Assistant

This guide covers the Firebase Cloud Functions and React frontend implementation needed to integrate your New Year Dashboard with Home Assistant.

---

## Overview

Your dashboard architecture:

```
React Frontend (Firebase Hosting)
        ↓
Firebase Cloud Functions (Middleware)
        ↓
Home Assistant WebSocket API
        ↓
Real-time Events & State Updates
```

**Why use Cloud Functions as middleware?**
- ✅ Keeps HA access token secret (never exposed to client)
- ✅ Handles WebSocket connection management and reconnection
- ✅ Can transform/filter data before sending to frontend
- ✅ Provides a stable SSE endpoint for frontend to consume
- ✅ Can handle authentication/rate limiting

---

## Part 1: Firebase Setup

### 1.1 Environment Variables

Store your Home Assistant credentials securely in Firebase.

**Set environment variables:**

```bash
# Navigate to your Firebase project directory
cd new-year-dashboard

# Set the Home Assistant URL
firebase functions:config:set ha.url="http://homeassistant.local:8123"

# Set the long-lived access token
firebase functions:config:set ha.token="YOUR_LONG_LIVED_ACCESS_TOKEN_HERE"

# Deploy the config
firebase deploy --only functions
```

**For local development (`.runtimeconfig.json`):**

```json
{
  "ha": {
    "url": "http://homeassistant.local:8123",
    "token": "YOUR_LONG_LIVED_ACCESS_TOKEN_HERE"
  }
}
```

Add `.runtimeconfig.json` to your `.gitignore`!

### 1.2 Install Dependencies

```bash
# In your functions directory
cd functions
npm install ws
npm install @types/ws --save-dev

# Optional: For REST API fallback
npm install axios
```

---

## Part 2: Cloud Functions Implementation

### 2.1 TypeScript Types

Create `functions/src/types/homeassistant.ts`:

```typescript
// Home Assistant WebSocket message types
export interface HAAuthMessage {
  type: 'auth';
  access_token: string;
}

export interface HASubscribeMessage {
  id: number;
  type: 'subscribe_events';
  event_type: string;
}

export interface HAGetStatesMessage {
  id: number;
  type: 'get_states';
}

// Home Assistant entity state
export interface HAEntityState {
  entity_id: string;
  state: string;
  attributes: Record<string, any>;
  last_changed: string;
  last_updated: string;
}

// Home Assistant events
export interface HATagScannedEvent {
  event_type: 'tag_scanned';
  data: {
    tag_id: string;
    device_id: string;
  };
  origin: string;
  time_fired: string;
}

export interface HADiagnosticEvent {
  event_type: 'nfc_dashboard_diagnostics';
  data: {
    timestamp: string;
    device_id: string;
    queue_tracker: string;
    base_playlist: string;
    device_1_state: string;
    device_2_state: string;
    device_1_current_song: string | null;
    device_2_current_song: string | null;
  };
  origin: string;
  time_fired: string;
}

export interface HAStateChangedEvent {
  event_type: 'state_changed';
  data: {
    entity_id: string;
    old_state: HAEntityState;
    new_state: HAEntityState;
  };
  origin: string;
  time_fired: string;
}

// Media player attributes
export interface MediaPlayerAttributes {
  media_content_id?: string;
  media_title?: string;
  media_artist?: string;
  media_album_name?: string;
  media_duration?: number;
  media_position?: number;
  media_position_updated_at?: string;
  volume_level?: number;
  is_volume_muted?: boolean;
  media_playlist?: string;
  shuffle?: boolean;
  repeat?: string;
}

// Dashboard-specific types
export interface DashboardUpdate {
  type: 'state_update' | 'tag_scanned' | 'diagnostic' | 'error' | 'connected';
  timestamp: string;
  data: any;
}
```

### 2.2 WebSocket Manager

Create `functions/src/services/haWebSocket.ts`:

```typescript
import WebSocket from 'ws';
import * as functions from 'firebase-functions';
import type {
  HAAuthMessage,
  HASubscribeMessage,
  HAGetStatesMessage,
  DashboardUpdate,
} from '../types/homeassistant';

export class HAWebSocketManager {
  private ws: WebSocket | null = null;
  private messageId = 1;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 5000;
  private listeners: Set<(update: DashboardUpdate) => void> = new Set();

  constructor(
    private haUrl: string,
    private haToken: string
  ) {}

  /**
   * Connect to Home Assistant WebSocket API
   */
  async connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      const wsUrl = this.haUrl.replace('http://', 'ws://').replace('https://', 'wss://');

      console.log(`Connecting to Home Assistant: ${wsUrl}/api/websocket`);
      this.ws = new WebSocket(`${wsUrl}/api/websocket`);

      this.ws.on('open', () => {
        console.log('WebSocket connection opened');
      });

      this.ws.on('message', (data: WebSocket.Data) => {
        const message = JSON.parse(data.toString());
        this.handleMessage(message, resolve, reject);
      });

      this.ws.on('error', (error) => {
        console.error('WebSocket error:', error);
        reject(error);
      });

      this.ws.on('close', () => {
        console.log('WebSocket connection closed');
        this.handleReconnect();
      });
    });
  }

  /**
   * Handle incoming messages from Home Assistant
   */
  private handleMessage(message: any, resolve?: () => void, reject?: (error: Error) => void): void {
    console.log('Received message:', message.type);

    switch (message.type) {
      case 'auth_required':
        this.authenticate();
        break;

      case 'auth_ok':
        console.log('Authentication successful');
        this.reconnectAttempts = 0;
        this.subscribeToEvents();
        this.notifyListeners({
          type: 'connected',
          timestamp: new Date().toISOString(),
          data: { message: 'Connected to Home Assistant' },
        });
        resolve?.();
        break;

      case 'auth_invalid':
        console.error('Authentication failed');
        reject?.(new Error('Invalid Home Assistant token'));
        break;

      case 'event':
        this.handleEvent(message.event);
        break;

      case 'result':
        // Handle response to our requests (get_states, etc.)
        if (message.success && message.result) {
          this.handleResult(message);
        }
        break;
    }
  }

  /**
   * Authenticate with Home Assistant
   */
  private authenticate(): void {
    const authMessage: HAAuthMessage = {
      type: 'auth',
      access_token: this.haToken,
    };
    this.send(authMessage);
  }

  /**
   * Subscribe to events we care about
   */
  private subscribeToEvents(): void {
    // Subscribe to tag scans
    this.subscribe('tag_scanned');

    // Subscribe to diagnostic events
    this.subscribe('nfc_dashboard_diagnostics');

    // Subscribe to state changes for media players
    this.subscribe('state_changed');

    // Get initial states
    this.getStates();
  }

  /**
   * Subscribe to a specific event type
   */
  private subscribe(eventType: string): void {
    const subscribeMessage: HASubscribeMessage = {
      id: this.messageId++,
      type: 'subscribe_events',
      event_type: eventType,
    };
    this.send(subscribeMessage);
  }

  /**
   * Get all current states
   */
  private getStates(): void {
    const getStatesMessage: HAGetStatesMessage = {
      id: this.messageId++,
      type: 'get_states',
    };
    this.send(getStatesMessage);
  }

  /**
   * Handle incoming events
   */
  private handleEvent(event: any): void {
    console.log('Event received:', event.event_type);

    switch (event.event_type) {
      case 'tag_scanned':
        this.notifyListeners({
          type: 'tag_scanned',
          timestamp: event.time_fired,
          data: event.data,
        });
        break;

      case 'nfc_dashboard_diagnostics':
        this.notifyListeners({
          type: 'diagnostic',
          timestamp: event.time_fired,
          data: event.data,
        });
        break;

      case 'state_changed':
        // Filter to only media player changes
        if (event.data.entity_id.startsWith('media_player.')) {
          this.notifyListeners({
            type: 'state_update',
            timestamp: event.time_fired,
            data: {
              entity_id: event.data.entity_id,
              new_state: event.data.new_state,
              old_state: event.data.old_state,
            },
          });
        }
        break;
    }
  }

  /**
   * Handle result messages (responses to our requests)
   */
  private handleResult(message: any): void {
    if (Array.isArray(message.result)) {
      // This is likely a get_states response
      const states = message.result;
      this.notifyListeners({
        type: 'state_update',
        timestamp: new Date().toISOString(),
        data: { initial_states: states },
      });
    }
  }

  /**
   * Send message to Home Assistant
   */
  private send(message: any): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }

  /**
   * Handle reconnection logic
   */
  private handleReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Attempting reconnect ${this.reconnectAttempts}/${this.maxReconnectAttempts}...`);

      setTimeout(() => {
        this.connect().catch((error) => {
          console.error('Reconnection failed:', error);
        });
      }, this.reconnectDelay);
    } else {
      console.error('Max reconnection attempts reached');
      this.notifyListeners({
        type: 'error',
        timestamp: new Date().toISOString(),
        data: { message: 'Connection lost to Home Assistant' },
      });
    }
  }

  /**
   * Register a listener for updates
   */
  addListener(listener: (update: DashboardUpdate) => void): void {
    this.listeners.add(listener);
  }

  /**
   * Remove a listener
   */
  removeListener(listener: (update: DashboardUpdate) => void): void {
    this.listeners.delete(listener);
  }

  /**
   * Notify all listeners of an update
   */
  private notifyListeners(update: DashboardUpdate): void {
    this.listeners.forEach((listener) => {
      try {
        listener(update);
      } catch (error) {
        console.error('Error in listener:', error);
      }
    });
  }

  /**
   * Disconnect and cleanup
   */
  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.listeners.clear();
  }
}
```

### 2.3 Server-Sent Events Endpoint

Create `functions/src/index.ts` (or add to existing):

```typescript
import * as functions from 'firebase-functions';
import { HAWebSocketManager } from './services/haWebSocket';
import type { DashboardUpdate } from './types/homeassistant';

// Global WebSocket manager instance (persists across requests)
let wsManager: HAWebSocketManager | null = null;

/**
 * Initialize WebSocket connection to Home Assistant
 */
async function ensureHAConnection(): Promise<HAWebSocketManager> {
  const haUrl = functions.config().ha.url;
  const haToken = functions.config().ha.token;

  if (!haUrl || !haToken) {
    throw new Error('Home Assistant configuration missing');
  }

  if (!wsManager) {
    wsManager = new HAWebSocketManager(haUrl, haToken);
    await wsManager.connect();
  }

  return wsManager;
}

/**
 * Server-Sent Events endpoint for real-time updates
 * Frontend connects to this and receives updates
 */
export const haStream = functions.https.onRequest(async (req, res) => {
  // Enable CORS
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET');

  if (req.method === 'OPTIONS') {
    res.status(204).send('');
    return;
  }

  // Set SSE headers
  res.set({
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
  });

  try {
    const manager = await ensureHAConnection();

    // Create listener for this connection
    const listener = (update: DashboardUpdate) => {
      const data = JSON.stringify(update);
      res.write(`data: ${data}\n\n`);
    };

    // Register listener
    manager.addListener(listener);

    // Send initial connection message
    res.write('data: {"type":"connected","message":"Stream established"}\n\n');

    // Handle client disconnect
    req.on('close', () => {
      console.log('Client disconnected from stream');
      manager.removeListener(listener);
    });

  } catch (error) {
    console.error('Error establishing HA connection:', error);
    res.status(500).json({ error: 'Failed to connect to Home Assistant' });
  }
});

/**
 * REST endpoint to get current state of a specific entity
 * Useful for initial page load or on-demand queries
 */
export const getEntityState = functions.https.onRequest(async (req, res) => {
  // Enable CORS
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, POST');
  res.set('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(204).send('');
    return;
  }

  const entityId = req.query.entity_id || req.body?.entity_id;

  if (!entityId) {
    res.status(400).json({ error: 'entity_id is required' });
    return;
  }

  try {
    const haUrl = functions.config().ha.url;
    const haToken = functions.config().ha.token;

    const response = await fetch(`${haUrl}/api/states/${entityId}`, {
      headers: {
        'Authorization': `Bearer ${haToken}`,
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();
    res.json(data);

  } catch (error) {
    console.error('Error fetching entity state:', error);
    res.status(500).json({ error: 'Failed to fetch entity state' });
  }
});

/**
 * Endpoint to call a Home Assistant service
 * Example: Trigger a sound, reset queue, etc.
 */
export const callService = functions.https.onRequest(async (req, res) => {
  // Enable CORS
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'POST');
  res.set('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(204).send('');
    return;
  }

  const { domain, service, entity_id, data } = req.body;

  if (!domain || !service) {
    res.status(400).json({ error: 'domain and service are required' });
    return;
  }

  try {
    const haUrl = functions.config().ha.url;
    const haToken = functions.config().ha.token;

    const response = await fetch(`${haUrl}/api/services/${domain}/${service}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${haToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        entity_id,
        ...data,
      }),
    });

    const result = await response.json();
    res.json(result);

  } catch (error) {
    console.error('Error calling service:', error);
    res.status(500).json({ error: 'Failed to call service' });
  }
});
```

### 2.4 Deploy Cloud Functions

```bash
# From your project root
firebase deploy --only functions

# Or deploy specific functions
firebase deploy --only functions:haStream,functions:getEntityState,functions:callService
```

---

## Part 3: React Frontend Implementation

### 3.1 TypeScript Types (Frontend)

Create `src/types/homeassistant.ts`:

```typescript
// Mirror the types from Cloud Functions
export interface DashboardUpdate {
  type: 'state_update' | 'tag_scanned' | 'diagnostic' | 'error' | 'connected';
  timestamp: string;
  data: any;
}

export interface MediaPlayerState {
  entity_id: string;
  state: 'playing' | 'paused' | 'idle' | 'unavailable';
  attributes: {
    media_title?: string;
    media_artist?: string;
    media_album_name?: string;
    media_duration?: number;
    media_position?: number;
    media_position_updated_at?: string;
    volume_level?: number;
    entity_picture?: string;
  };
}

export interface TagScannedData {
  tag_id: string;
  device_id: string;
}

export interface DiagnosticData {
  timestamp: string;
  device_id: string;
  queue_tracker: string;
  base_playlist: string;
  device_1_state: string;
  device_2_state: string;
  device_1_current_song: string | null;
  device_2_current_song: string | null;
}
```

### 3.2 Home Assistant Hook

Create `src/hooks/useHomeAssistant.ts`:

```typescript
import { useState, useEffect, useCallback } from 'react';
import type { DashboardUpdate, MediaPlayerState, TagScannedData, DiagnosticData } from '../types/homeassistant';

interface UseHomeAssistantReturn {
  device1Player: MediaPlayerState | null;
  device2Player: MediaPlayerState | null;
  lastTagScanned: TagScannedData | null;
  diagnosticData: DiagnosticData | null;
  queueTracker: string;
  isConnected: boolean;
  error: string | null;
  fetchEntityState: (entityId: string) => Promise<any>;
}

export function useHomeAssistant(): UseHomeAssistantReturn {
  const [device1Player, setDevice1Player] = useState<MediaPlayerState | null>(null);
  const [device2Player, setDevice2Player] = useState<MediaPlayerState | null>(null);
  const [lastTagScanned, setLastTagScanned] = useState<TagScannedData | null>(null);
  const [diagnosticData, setDiagnosticData] = useState<DiagnosticData | null>(null);
  const [queueTracker, setQueueTracker] = useState<string>('');
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Your Firebase Cloud Function URL
  const CLOUD_FUNCTION_BASE_URL = 'https://YOUR-REGION-YOUR-PROJECT.cloudfunctions.net';

  /**
   * Connect to Server-Sent Events stream
   */
  useEffect(() => {
    const eventSource = new EventSource(`${CLOUD_FUNCTION_BASE_URL}/haStream`);

    eventSource.onopen = () => {
      console.log('SSE connection opened');
      setIsConnected(true);
      setError(null);
    };

    eventSource.onmessage = (event) => {
      try {
        const update: DashboardUpdate = JSON.parse(event.data);
        handleUpdate(update);
      } catch (err) {
        console.error('Error parsing SSE message:', err);
      }
    };

    eventSource.onerror = (err) => {
      console.error('SSE error:', err);
      setIsConnected(false);
      setError('Connection lost to Home Assistant');

      // EventSource will automatically try to reconnect
    };

    // Cleanup on unmount
    return () => {
      eventSource.close();
    };
  }, []);

  /**
   * Handle incoming updates from SSE stream
   */
  const handleUpdate = (update: DashboardUpdate) => {
    console.log('Update received:', update.type);

    switch (update.type) {
      case 'connected':
        setIsConnected(true);
        setError(null);
        break;

      case 'state_update':
        handleStateUpdate(update.data);
        break;

      case 'tag_scanned':
        setLastTagScanned(update.data);
        // Auto-clear after 5 seconds
        setTimeout(() => setLastTagScanned(null), 5000);
        break;

      case 'diagnostic':
        setDiagnosticData(update.data);
        break;

      case 'error':
        setError(update.data.message);
        break;
    }
  };

  /**
   * Handle state updates for entities
   */
  const handleStateUpdate = (data: any) => {
    if (data.initial_states) {
      // Initial load - process all states
      const states = data.initial_states as MediaPlayerState[];

      states.forEach((state) => {
        if (state.entity_id === 'media_player.spotify_soren_kjaedegaard_haug') {
          setDevice1Player(state);
        } else if (state.entity_id === 'media_player.spotify_soren_nytar') {
          setDevice2Player(state);
        } else if (state.entity_id === 'input_text.nfc_queue_tracker') {
          setQueueTracker(state.state);
        }
      });
    } else if (data.entity_id && data.new_state) {
      // Individual state change
      const entityId = data.entity_id;
      const newState = data.new_state;

      if (entityId === 'media_player.spotify_soren_kjaedegaard_haug') {
        setDevice1Player(newState);
      } else if (entityId === 'media_player.spotify_soren_nytar') {
        setDevice2Player(newState);
      } else if (entityId === 'input_text.nfc_queue_tracker') {
        setQueueTracker(newState.state);
      }
    }
  };

  /**
   * Fetch a specific entity state on-demand
   */
  const fetchEntityState = useCallback(async (entityId: string) => {
    try {
      const response = await fetch(
        `${CLOUD_FUNCTION_BASE_URL}/getEntityState?entity_id=${entityId}`
      );
      return await response.json();
    } catch (err) {
      console.error('Error fetching entity state:', err);
      throw err;
    }
  }, []);

  return {
    device1Player,
    device2Player,
    lastTagScanned,
    diagnosticData,
    queueTracker,
    isConnected,
    error,
    fetchEntityState,
  };
}
```

### 3.3 React Context Provider (Optional but Recommended)

Create `src/contexts/HomeAssistantContext.tsx`:

```typescript
import { createContext, useContext, ReactNode } from 'react';
import { useHomeAssistant } from '../hooks/useHomeAssistant';
import type { MediaPlayerState, TagScannedData, DiagnosticData } from '../types/homeassistant';

interface HomeAssistantContextValue {
  device1Player: MediaPlayerState | null;
  device2Player: MediaPlayerState | null;
  lastTagScanned: TagScannedData | null;
  diagnosticData: DiagnosticData | null;
  queueTracker: string;
  isConnected: boolean;
  error: string | null;
  fetchEntityState: (entityId: string) => Promise<any>;
}

const HomeAssistantContext = createContext<HomeAssistantContextValue | undefined>(undefined);

export function HomeAssistantProvider({ children }: { children: ReactNode }) {
  const value = useHomeAssistant();

  return (
    <HomeAssistantContext.Provider value={value}>
      {children}
    </HomeAssistantContext.Provider>
  );
}

export function useHA() {
  const context = useContext(HomeAssistantContext);
  if (!context) {
    throw new Error('useHA must be used within HomeAssistantProvider');
  }
  return context;
}
```

### 3.4 Update App Root

Update `src/main.tsx` or `src/App.tsx`:

```typescript
import { HomeAssistantProvider } from './contexts/HomeAssistantContext';

function App() {
  return (
    <HomeAssistantProvider>
      {/* Your existing app components */}
      <Dashboard />
    </HomeAssistantProvider>
  );
}
```

---

## Part 4: React Components

### 4.1 Now Playing Component

Create `src/components/NowPlaying.tsx`:

```typescript
import { useHA } from '../contexts/HomeAssistantContext';

export function NowPlaying() {
  const { device1Player, device2Player, isConnected } = useHA();

  if (!isConnected) {
    return <div className="status-offline">Connecting to Home Assistant...</div>;
  }

  return (
    <div className="now-playing">
      {/* Device 1 */}
      <div className="player device-1">
        <h2>Device 1 - Living Room</h2>
        {device1Player && device1Player.state === 'playing' ? (
          <>
            <div className="album-art">
              {device1Player.attributes.entity_picture && (
                <img src={device1Player.attributes.entity_picture} alt="Album art" />
              )}
            </div>
            <div className="track-info">
              <div className="title">{device1Player.attributes.media_title}</div>
              <div className="artist">{device1Player.attributes.media_artist}</div>
            </div>
            <div className="progress-bar">
              {/* Implement progress bar using media_position and media_duration */}
            </div>
          </>
        ) : (
          <div className="idle">Not playing</div>
        )}
      </div>

      {/* Device 2 */}
      <div className="player device-2">
        <h2>Device 2 - Kitchen</h2>
        {device2Player && device2Player.state === 'playing' ? (
          <>
            <div className="album-art">
              {device2Player.attributes.entity_picture && (
                <img src={device2Player.attributes.entity_picture} alt="Album art" />
              )}
            </div>
            <div className="track-info">
              <div className="title">{device2Player.attributes.media_title}</div>
              <div className="artist">{device2Player.attributes.media_artist}</div>
            </div>
          </>
        ) : (
          <div className="idle">Not playing</div>
        )}
      </div>
    </div>
  );
}
```

### 4.2 Queue Status Component

Create `src/components/QueueStatus.tsx`:

```typescript
import { useHA } from '../contexts/HomeAssistantContext';

export function QueueStatus() {
  const { queueTracker } = useHA();

  const queuedSongs = queueTracker ? queueTracker.split(',') : [];
  const slotsUsed = queuedSongs.length;
  const maxSlots = 3;

  return (
    <div className="queue-status">
      <h3>Device 1 Queue ({slotsUsed}/{maxSlots})</h3>
      <div className="queue-slots">
        {[...Array(maxSlots)].map((_, index) => (
          <div
            key={index}
            className={`queue-slot ${index < slotsUsed ? 'filled' : 'empty'}`}
          >
            {index < slotsUsed ? '🎵' : '⭕'}
          </div>
        ))}
      </div>
      {slotsUsed >= maxSlots && (
        <div className="queue-full-warning">⚠️ Queue Full!</div>
      )}
    </div>
  );
}
```

### 4.3 Tag Scan Notification

Create `src/components/TagNotification.tsx`:

```typescript
import { useHA } from '../contexts/HomeAssistantContext';
import { useEffect, useState } from 'react';

export function TagNotification() {
  const { lastTagScanned } = useHA();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (lastTagScanned) {
      setVisible(true);
      const timer = setTimeout(() => setVisible(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [lastTagScanned]);

  if (!visible || !lastTagScanned) return null;

  const deviceName = lastTagScanned.device_id.includes('1') ? 'Device 1' : 'Device 2';

  return (
    <div className="tag-notification toast">
      <span className="icon">🏷️</span>
      <span className="message">
        Tag scanned on {deviceName}
      </span>
    </div>
  );
}
```

### 4.4 Diagnostic Panel

Create `src/components/DiagnosticPanel.tsx`:

```typescript
import { useHA } from '../contexts/HomeAssistantContext';
import { useEffect, useState } from 'react';

export function DiagnosticPanel() {
  const { diagnosticData } = useHA();
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (diagnosticData) {
      setIsVisible(true);
    }
  }, [diagnosticData]);

  if (!isVisible || !diagnosticData) return null;

  return (
    <div className="diagnostic-panel">
      <div className="diagnostic-header">
        <h2>🔍 Diagnostics</h2>
        <button onClick={() => setIsVisible(false)}>Close</button>
      </div>

      <div className="diagnostic-content">
        <section>
          <h3>Device States</h3>
          <div className="diagnostic-row">
            <span>Device 1:</span>
            <span className={`status ${diagnosticData.device_1_state}`}>
              {diagnosticData.device_1_state}
            </span>
          </div>
          <div className="diagnostic-row">
            <span>Device 2:</span>
            <span className={`status ${diagnosticData.device_2_state}`}>
              {diagnosticData.device_2_state}
            </span>
          </div>
        </section>

        <section>
          <h3>Currently Playing</h3>
          <div className="diagnostic-row">
            <span>Device 1:</span>
            <span>{diagnosticData.device_1_current_song || 'Nothing'}</span>
          </div>
          <div className="diagnostic-row">
            <span>Device 2:</span>
            <span>{diagnosticData.device_2_current_song || 'Nothing'}</span>
          </div>
        </section>

        <section>
          <h3>Queue Info</h3>
          <div className="diagnostic-row">
            <span>Queue Tracker:</span>
            <span className="mono">{diagnosticData.queue_tracker || 'Empty'}</span>
          </div>
          <div className="diagnostic-row">
            <span>Base Playlist:</span>
            <span className="mono">{diagnosticData.base_playlist}</span>
          </div>
        </section>

        <section>
          <h3>Scan Info</h3>
          <div className="diagnostic-row">
            <span>Scanned from:</span>
            <span>{diagnosticData.device_id}</span>
          </div>
          <div className="diagnostic-row">
            <span>Timestamp:</span>
            <span>{new Date(diagnosticData.timestamp).toLocaleTimeString()}</span>
          </div>
        </section>
      </div>
    </div>
  );
}
```

---

## Part 5: Main Dashboard Component

Create `src/components/Dashboard.tsx`:

```typescript
import { NowPlaying } from './NowPlaying';
import { QueueStatus } from './QueueStatus';
import { TagNotification } from './TagNotification';
import { DiagnosticPanel } from './DiagnosticPanel';
import { useHA } from '../contexts/HomeAssistantContext';

export function Dashboard() {
  const { isConnected, error } = useHA();

  return (
    <div className="dashboard">
      {/* Connection Status */}
      <div className={`connection-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
        {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
      </div>

      {/* Error Display */}
      {error && (
        <div className="error-banner">
          ⚠️ {error}
        </div>
      )}

      {/* Main Content */}
      <NowPlaying />
      <QueueStatus />

      {/* Overlays */}
      <TagNotification />
      <DiagnosticPanel />
    </div>
  );
}
```

---

## Part 6: Styling Example

Create `src/styles/dashboard.css`:

```css
.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
  color: white;
}

.connection-indicator {
  position: fixed;
  top: 1rem;
  right: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 600;
  z-index: 1000;
}

.connection-indicator.connected {
  background: rgba(34, 197, 94, 0.2);
  border: 2px solid rgb(34, 197, 94);
}

.connection-indicator.disconnected {
  background: rgba(239, 68, 68, 0.2);
  border: 2px solid rgb(239, 68, 68);
}

.error-banner {
  background: rgba(239, 68, 68, 0.9);
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  text-align: center;
  font-weight: 600;
}

.tag-notification {
  position: fixed;
  top: 5rem;
  right: 1rem;
  background: rgba(34, 197, 94, 0.95);
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  animation: slideIn 0.3s ease-out;
  z-index: 1000;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.diagnostic-panel {
  position: fixed;
  top: 0;
  right: 0;
  width: 400px;
  height: 100vh;
  background: rgba(0, 0, 0, 0.95);
  padding: 2rem;
  overflow-y: auto;
  box-shadow: -4px 0 8px rgba(0, 0, 0, 0.3);
  z-index: 999;
  animation: slideInRight 0.3s ease-out;
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}

.diagnostic-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.diagnostic-content section {
  margin-bottom: 2rem;
}

.diagnostic-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.status.playing {
  color: rgb(34, 197, 94);
}

.status.paused {
  color: rgb(251, 191, 36);
}

.status.idle {
  color: rgb(156, 163, 175);
}

.mono {
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
}
```

---

## Part 7: Environment Configuration

### 7.1 Firebase Hosting Config

Update `firebase.json`:

```json
{
  "hosting": {
    "public": "dist",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ],
    "headers": [
      {
        "source": "**",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "no-cache, no-store, must-revalidate"
          }
        ]
      }
    ]
  },
  "functions": {
    "source": "functions"
  }
}
```

### 7.2 Environment Variables (Frontend)

Create `.env.local`:

```bash
VITE_CLOUD_FUNCTION_BASE_URL=https://YOUR-REGION-YOUR-PROJECT.cloudfunctions.net
```

Update your hook to use:

```typescript
const CLOUD_FUNCTION_BASE_URL = import.meta.env.VITE_CLOUD_FUNCTION_BASE_URL;
```

---

## Part 8: Testing

### 8.1 Test Cloud Functions Locally

```bash
# Start Firebase emulators
firebase emulators:start

# Your functions will be available at:
# http://localhost:5001/YOUR-PROJECT/YOUR-REGION/haStream
```

### 8.2 Test SSE Connection

```bash
# Use curl to test SSE stream
curl http://localhost:5001/YOUR-PROJECT/YOUR-REGION/haStream

# You should see a stream of events
```

### 8.3 Test Frontend Development

```bash
# Update .env.local to point to local emulator
VITE_CLOUD_FUNCTION_BASE_URL=http://localhost:5001/YOUR-PROJECT/YOUR-REGION

# Start dev server
npm run dev
```

---

## Part 9: Deployment

### 9.1 Build and Deploy

```bash
# Build frontend
npm run build

# Deploy everything
firebase deploy

# Or deploy individually
firebase deploy --only hosting
firebase deploy --only functions
```

### 9.2 Post-Deployment

1. Update CORS settings in Home Assistant `configuration.yaml`:
   ```yaml
   http:
     cors_allowed_origins:
       - https://your-project.web.app
       - https://your-project.firebaseapp.com
   ```

2. Update `.env.local` to production Cloud Function URL

3. Test diagnostic tag scan

---

## Part 10: Troubleshooting

### Issue: SSE Connection Fails

**Check:**
- ✅ Cloud Function is deployed: `firebase functions:list`
- ✅ Environment variables are set: `firebase functions:config:get`
- ✅ Home Assistant is accessible from Cloud Function server
- ✅ Long-lived token is valid

### Issue: No Events Received

**Check:**
- ✅ Scan a tag and verify event appears in HA Developer Tools → Events
- ✅ Check Cloud Function logs: `firebase functions:log`
- ✅ Verify WebSocket connection in function logs

### Issue: CORS Errors

**Check:**
- ✅ Firebase domain added to HA `cors_allowed_origins`
- ✅ Cloud Function has CORS headers set
- ✅ Restart Home Assistant after config change

### Issue: Diagnostic Panel Not Appearing

**Check:**
- ✅ Diagnostic tag UID is correct in automation
- ✅ `diagnostic_tag_automation.yaml` is loaded in HA
- ✅ Event `nfc_dashboard_diagnostics` fires (check HA events)
- ✅ Frontend subscribes to this event type

---

## Part 11: Advanced Features

### 11.1 Add Service Calls from Dashboard

Update your hook to include:

```typescript
const callService = async (domain: string, service: string, entityId?: string) => {
  const response = await fetch(`${CLOUD_FUNCTION_BASE_URL}/callService`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ domain, service, entity_id: entityId }),
  });
  return response.json();
};
```

Then in your component:

```typescript
// Reset queue button
<button onClick={() => callService('input_text', 'set_value', 'input_text.nfc_queue_tracker')}>
  Clear Queue
</button>
```

### 11.2 Add Event History

Track recent events in state:

```typescript
const [eventHistory, setEventHistory] = useState<DashboardUpdate[]>([]);

// In handleUpdate:
setEventHistory(prev => [update, ...prev].slice(0, 20)); // Keep last 20
```

Display in diagnostic panel:

```typescript
<section>
  <h3>Recent Events</h3>
  {eventHistory.map((event, i) => (
    <div key={i} className="event-item">
      <span>{new Date(event.timestamp).toLocaleTimeString()}</span>
      <span>{event.type}</span>
    </div>
  ))}
</section>
```

---

## Summary

You now have:
- ✅ Secure Cloud Functions middleware for HA communication
- ✅ Real-time SSE stream for instant updates
- ✅ React hooks and context for easy data access
- ✅ Components for now playing, queue status, and diagnostics
- ✅ Tag scan notifications and diagnostic panel
- ✅ Full TypeScript typing throughout

**Next Steps:**
1. Deploy Cloud Functions
2. Update Home Assistant CORS config
3. Test SSE connection
4. Scan diagnostic tag to verify integration
5. Style to match your existing dashboard design

Enjoy your New Year's party with real-time dashboard updates! 🎉
