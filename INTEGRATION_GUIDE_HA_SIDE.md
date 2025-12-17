# Home Assistant Integration Guide
## Connecting Your New Year Dashboard to Home Assistant

This guide covers the Home Assistant and ESPHome configuration needed to integrate with your Firebase-hosted dashboard website.

---

## Overview

Your dashboard will connect to Home Assistant to:
- Display real-time playback information from both Device 1 and Device 2
- React to NFC tag scans and show what's being queued
- Display diagnostics when a special diagnostic tag is scanned
- Show queue status, helper states, and recent events
- Provide visual feedback for successes/failures during the party

---

## Architecture

```
NFC Tag Scan → ESPHome Device → Home Assistant
                                      ↓
                                  WebSocket API
                                      ↓
                         Firebase Cloud Function ← Your Dashboard Website
                                      ↓
                              Real-time Updates
```

---

## Part 1: Home Assistant API Access

### 1.1 Create Long-Lived Access Token

Your Firebase Cloud Functions will use this token to authenticate with Home Assistant.

**Steps:**
1. Log into Home Assistant web interface
2. Click your profile (bottom left corner)
3. Scroll down to "Long-Lived Access Tokens"
4. Click "Create Token"
5. Name it: `New Year Dashboard`
6. Copy the token immediately (you can't see it again!)
7. Store this securely in your Firebase Cloud Function environment variables

**Security Note:** This token has full access to your HA instance. Keep it secret!

### 1.2 Enable Home Assistant API

The Home Assistant API should already be enabled (it's used by ESPHome devices), but verify:

**File:** `configuration.yaml` (in your Home Assistant config directory)

```yaml
# Enable the HTTP integration (required for REST API and WebSocket)
http:
  # Optional: Only allow connections from specific IPs
  # trusted_proxies:
  #   - 127.0.0.1

  # Optional: Enable CORS for specific domains
  cors_allowed_origins:
    - https://your-firebase-app.web.app
    - https://your-firebase-app.firebaseapp.com
```

**Restart Home Assistant** after making changes.

### 1.3 Find Your Home Assistant URL

Your dashboard needs to know where to connect:

- **Local network access:** `http://homeassistant.local:8123` or `http://YOUR_HA_IP:8123`
- **Remote access (recommended):**
  - Option A: Use **Nabu Casa** (Home Assistant Cloud) - gives you a secure `https://xxxxx.ui.nabu.casa` URL
  - Option B: Set up **DuckDNS + Let's Encrypt** for your own HTTPS domain
  - Option C: Use **Tailscale/VPN** for secure remote access

**For party use:** If everyone is on the same WiFi network, local access works fine!

---

## Part 2: Understanding Available Data

### 2.1 Key Entities Your Dashboard Can Access

#### **Media Players**
- `media_player.spotify_soren_kjaedegaard_haug` - Device 1 Spotify player
- `media_player.spotify_soren_nytar` - Device 2 Spotify player
- `media_player.stue_1140714430_spotcast` - Device 1 Spotcast entity
- `media_player.kokken_31fi44dypurzlvw6e6ftr6mu673y_spotcast` - Device 2 Spotcast entity

**Attributes you can read:**
- `state` - playing, paused, idle
- `attributes.media_title` - Current song name
- `attributes.media_artist` - Artist name
- `attributes.media_album_name` - Album name
- `attributes.media_duration` - Song length
- `attributes.media_position` - Current playback position
- `attributes.volume_level` - Current volume (0.0 - 1.0)
- `attributes.media_content_id` - Spotify URI of current track

#### **Input Helpers (Queue & State Management)**
- `input_text.nfc_queue_tracker` - Comma-separated list of queued Spotify URIs on Device 1
- `input_text.base_playlist_uri` - Current base playlist for idle recovery
- Other permission/state helpers (check your HA setup for complete list)

#### **ESPHome Device Sensors**
- `sensor.nfc_party_controller_2_volume_pot` - Volume potentiometer value (0-100%)
- `binary_sensor.nfc_party_controller_2_speaker_button` - Speaker button state
- `sensor.nfc_party_controller_1_wifi_signal` - Device 1 WiFi strength
- `sensor.nfc_party_controller_2_wifi_signal` - Device 2 WiFi strength

#### **Buttons (for triggering sounds)**
- `button.nfc_party_controller_1_play_success`
- `button.nfc_party_controller_1_play_failure`
- `button.nfc_party_controller_2_play_success`
- `button.nfc_party_controller_2_play_failure`

### 2.2 Key Events Your Dashboard Can Subscribe To

#### **NFC Tag Scans**
- Event type: `tag_scanned`
- Data includes:
  - `tag_id` - The NFC tag UID
  - `device_id` - Which ESP32 scanned it (Device 1 or Device 2)

#### **Custom ESPHome Events**
- Event type: `esphome.speaker_button_pressed`
- Data includes:
  - `device` - Always `nfc-party-controller-2`

#### **Automation Events**
- Event type: `automation_triggered`
- Fired when any automation runs
- Data includes:
  - `entity_id` - Which automation fired
  - `source` - What triggered it

#### **State Changes**
You can subscribe to state changes for any entity:
- When songs change on media players
- When queue tracker updates
- When volume changes
- etc.

---

## Part 3: Setting Up Diagnostic Tag

### 3.1 Create a Diagnostic Tag Automation

This automation will fire an event when your special diagnostic tag is scanned, which your dashboard can listen for.

**File:** Create `diagnostic_tag_automation.yaml` in project root

```yaml
automation:
  - alias: "Diagnostic Tag - Trigger Dashboard Debug View"
    description: "Sends diagnostic event to dashboard when special tag is scanned"

    trigger:
      - platform: tag
        tag_id: "YOUR-DIAGNOSTIC-TAG-UID-HERE"

    action:
      # Fire custom event that dashboard will listen for
      - event: nfc_dashboard_diagnostics
        event_data:
          timestamp: "{{ now().isoformat() }}"
          device_id: "{{ trigger.event.data.device_id }}"
          # Include current system state
          queue_tracker: "{{ states('input_text.nfc_queue_tracker') }}"
          base_playlist: "{{ states('input_text.base_playlist_uri') }}"
          device_1_state: "{{ states('media_player.spotify_soren_kjaedegaard_haug') }}"
          device_2_state: "{{ states('media_player.spotify_soren_nytar') }}"
          device_1_current_song: "{{ state_attr('media_player.spotify_soren_kjaedegaard_haug', 'media_title') }}"
          device_2_current_song: "{{ state_attr('media_player.spotify_soren_nytar', 'media_title') }}"

      # Optional: Play a distinct sound to confirm diagnostic mode
      - action: button.press
        target:
          entity_id: button.nfc_party_controller_1_play_master

    mode: single
```

**Steps:**
1. Create the file above in your project root
2. Scan a blank NFC tag with your phone to get its UID
3. Replace `YOUR-DIAGNOSTIC-TAG-UID-HERE` with the actual tag UID
4. Add this automation to your Home Assistant configuration
5. Reload automations in HA

### 3.2 Test the Diagnostic Tag

After setup:
1. Scan the diagnostic tag
2. Check Home Assistant → Developer Tools → Events
3. Listen for `nfc_dashboard_diagnostics` event
4. You should see it appear with all the diagnostic data

---

## Part 4: WebSocket API Connection Details

### 4.1 WebSocket Endpoint

```
ws://YOUR_HA_URL:8123/api/websocket
# or for HTTPS:
wss://YOUR_HA_URL:8123/api/websocket
```

### 4.2 Authentication Flow

Your Firebase Cloud Function should handle this:

1. Connect to WebSocket
2. Receive `auth_required` message
3. Send authentication with long-lived token:
   ```json
   {
     "type": "auth",
     "access_token": "YOUR_LONG_LIVED_TOKEN"
   }
   ```
4. Receive `auth_ok` message
5. Now you can subscribe to events and states

### 4.3 Subscribing to Events

**Subscribe to all tag scans:**
```json
{
  "id": 1,
  "type": "subscribe_events",
  "event_type": "tag_scanned"
}
```

**Subscribe to diagnostic events:**
```json
{
  "id": 2,
  "type": "subscribe_events",
  "event_type": "nfc_dashboard_diagnostics"
}
```

**Subscribe to state changes for a media player:**
```json
{
  "id": 3,
  "type": "subscribe_events",
  "event_type": "state_changed",
  "event_data": {
    "entity_id": "media_player.spotify_soren_nytar"
  }
}
```

### 4.4 Getting Current States

**Get current state of an entity:**
```json
{
  "id": 4,
  "type": "call_service",
  "domain": "homeassistant",
  "service": "get_state",
  "service_data": {
    "entity_id": "media_player.spotify_soren_nytar"
  }
}
```

**Get all states (initial load):**
```json
{
  "id": 5,
  "type": "get_states"
}
```

---

## Part 5: REST API Alternative (Simpler but Less Real-Time)

If WebSocket is too complex initially, you can use REST API for polling:

### 5.1 Get Entity State

**Endpoint:**
```
GET http://YOUR_HA_URL:8123/api/states/media_player.spotify_soren_nytar
```

**Headers:**
```
Authorization: Bearer YOUR_LONG_LIVED_TOKEN
Content-Type: application/json
```

**Response:**
```json
{
  "entity_id": "media_player.spotify_soren_nytar",
  "state": "playing",
  "attributes": {
    "media_title": "Song Name",
    "media_artist": "Artist Name",
    "volume_level": 0.5
  }
}
```

### 5.2 Get Recent Events

**Endpoint:**
```
GET http://YOUR_HA_URL:8123/api/events
```

This gives you a stream of events, but WebSocket is better for real-time.

---

## Part 6: Security Considerations

### 6.1 Network Security

**For local network only (party at your place):**
- ✅ No special configuration needed
- ✅ Devices on same WiFi can access HA directly
- ⚠️ Make sure your WiFi has a password!

**For remote access (party elsewhere):**
- ✅ Use Nabu Casa Cloud (easiest, $6.50/month)
- ✅ Or set up DuckDNS + Let's Encrypt for free HTTPS
- ❌ Don't expose plain HTTP Home Assistant to the internet!

### 6.2 Token Security

**Best practices:**
- ✅ Store token in Firebase Cloud Function environment variables
- ✅ Never expose token to client-side code
- ✅ Create a dedicated user in HA with limited permissions (optional)
- ✅ Rotate token periodically
- ❌ Don't commit token to git repos

### 6.3 Rate Limiting

Your dashboard might poll frequently. Consider:
- Limit WebSocket subscriptions to only entities you need
- For REST API, don't poll faster than every 1-2 seconds
- Use state change subscriptions instead of polling when possible

---

## Part 7: Testing the Integration

### 7.1 Test WebSocket Connection

Use a WebSocket testing tool (like `websocat` or browser extensions):

```bash
# Install websocat
brew install websocat

# Connect to HA WebSocket
websocat ws://homeassistant.local:8123/api/websocket

# You'll receive auth_required, then send:
{"type": "auth", "access_token": "YOUR_TOKEN"}

# Then subscribe to tag scans:
{"id": 1, "type": "subscribe_events", "event_type": "tag_scanned"}

# Now scan an NFC tag - you should see the event!
```

### 7.2 Test REST API

```bash
# Get Device 2 media player state
curl -X GET \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  http://homeassistant.local:8123/api/states/media_player.spotify_soren_nytar
```

### 7.3 Verify CORS Settings

If your dashboard shows CORS errors:
1. Add your Firebase domain to `cors_allowed_origins` in `configuration.yaml`
2. Restart Home Assistant
3. Clear browser cache and try again

---

## Part 8: Recommended Dashboard Features

### 8.1 Essential Views

**Normal View (Always Visible):**
- Device 1 & Device 2 currently playing
- Album artwork
- Song progress bars
- Queue visualization for Device 1 (3 slots)

**Diagnostic View (Triggered by Diagnostic Tag):**
- All helper states (queue tracker, base playlist, etc.)
- Last 10-20 events with timestamps
- Color-coded status indicators (green = playing, yellow = paused, red = error)
- WiFi signal strength for both ESP32 devices
- Quick actions: Reset queue, change base playlist

### 8.2 Event Handling Priorities

**High Priority (Show immediately):**
- Tag scans (show what was queued)
- Failure sounds (alert user to queue limit or errors)
- Diagnostic tag scans (switch to diagnostic view)

**Medium Priority (Update UI):**
- Song changes
- Volume changes
- Play/pause state changes

**Low Priority (Background updates):**
- WiFi signal changes
- Uptime updates

---

## Part 9: Troubleshooting

### Issue: Can't connect to WebSocket

**Check:**
- ✅ Is Home Assistant running?
- ✅ Is the URL correct? (check http vs https, port 8123)
- ✅ Is the long-lived token valid?
- ✅ Are you on the same network (for local access)?
- ✅ Check HA logs: Settings → System → Logs

### Issue: CORS errors in browser console

**Fix:**
- Add your Firebase domain to `cors_allowed_origins` in `configuration.yaml`
- Restart Home Assistant
- Clear browser cache

### Issue: Events not appearing

**Check:**
- ✅ Is the automation enabled in HA?
- ✅ Scan a tag and check HA → Developer Tools → Events
- ✅ Are you subscribed to the correct event type in WebSocket?
- ✅ Check automation traces: Settings → Automations → [automation] → Traces

### Issue: Diagnostic tag not working

**Debug:**
- Scan the tag near the NFC reader
- Check HA logs for tag UID
- Verify tag UID matches the one in `diagnostic_tag_automation.yaml`
- Check if `nfc_dashboard_diagnostics` event appears in Developer Tools → Events

---

## Part 10: Next Steps

Once you have the HA side configured:

1. ✅ Create long-lived access token
2. ✅ Configure CORS in `configuration.yaml`
3. ✅ Create diagnostic tag automation
4. ✅ Test WebSocket connection manually
5. ✅ Document all entity IDs your dashboard needs
6. ✅ Scan diagnostic NFC tag and assign its UID

**You're ready for the website integration guide!**

The dashboard can now:
- Connect to your Home Assistant instance
- Subscribe to real-time events
- Read entity states
- React to NFC tag scans
- Display diagnostics on demand

---

## Useful References

- [Home Assistant WebSocket API Documentation](https://developers.home-assistant.io/docs/api/websocket)
- [Home Assistant REST API Documentation](https://developers.home-assistant.io/docs/api/rest)
- [Authentication Documentation](https://developers.home-assistant.io/docs/auth_api)
- [Firebase Cloud Functions + WebSocket Setup](https://firebase.google.com/docs/functions)

---

## Questions or Issues?

Check the Home Assistant community forums or open an issue in this repository. Good luck with your New Year's party! 🎉
