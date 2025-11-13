# Home Assistant Configuration

This directory contains Home Assistant configuration for the NFC Party Controller project.

## Structure

```
home-assistant/
├── packages/               # Package-based configuration
│   ├── nfc_tags.yaml      # NFC event handling and tag automation
│   ├── party_mode.yaml    # Party mode helpers and state management
│   ├── audio_control.yaml # Multi-room audio control
│   └── lighting_scenes.yaml # Philips Hue scenes (future)
├── blueprints/            # Automation blueprints (future)
├── dashboards/            # Lovelace dashboard configs (future)
├── configuration.yaml.example  # Main config template
└── README.md              # This file
```

## Package System

This project uses Home Assistant's **package system** for modular configuration. Each package is self-contained with its own automations, scripts, helpers, and sensors.

### Benefits

- **Modularity**: Each feature is in its own file
- **Maintainability**: Easy to find and update specific functionality
- **Portability**: Packages can be shared and reused
- **Version Control**: Clean git diffs for specific features

### Packages Overview

#### `party_mode.yaml`
Contains all party mode state management:
- `input_boolean.party_mode` - Master switch for party mode
- `input_select.music_mood` - Music mood selection (Energetic, Chill, etc.)
- `input_number.party_volume` - Party mode volume setting
- `counter.songs_played_today` - Track songs played
- Automations for party mode on/off sequences

#### `nfc_tags.yaml`
Handles all NFC tag scanning logic:
- Event router for `tag_scanned` events
- Example tag automation templates
- Generic Spotify playlist script
- Tag-to-action mapping framework

**Important**: Tag IDs are managed via Home Assistant's native tag system. No hardcoded tag IDs in ESPHome.

#### `audio_control.yaml`
Multi-room audio management:
- Beolink speaker grouping scripts
- Volume control automations (potentiometer sync)
- Button controls (play/pause, next track, group toggle)
- Audio system status sensors

#### `lighting_scenes.yaml` *(Future)*
Philips Hue integration placeholder:
- Light scene definitions
- Mood-synchronized lighting
- NFC-triggered lighting effects

## Setup Instructions

### 1. Copy Configuration Template

```bash
cp configuration.yaml.example /config/configuration.yaml
```

Edit as needed for your setup.

### 2. Enable Package Loading

Ensure your `configuration.yaml` includes:

```yaml
homeassistant:
  packages: !include_dir_named packages/
```

### 3. Copy Packages

Copy the `packages/` directory to your Home Assistant config:

```bash
cp -r packages/ /config/packages/
```

### 4. Configure Bang & Olufsen Integration

In Home Assistant UI:
1. Go to **Settings** → **Devices & Services**
2. Add **Bang & Olufsen** integration
3. Configure each speaker (Kontor, Køkken, Stue)
4. Note the entity IDs - update in `audio_control.yaml` if different

### 5. Configure Spotify

1. Create a Spotify Developer app: https://developer.spotify.com/dashboard
2. Add integration in Home Assistant UI
3. Authorize with your Spotify account

### 6. Configure ESPHome Device

1. The ESP32 should auto-discover after firmware upload
2. Go to **Settings** → **Devices & Services** → **ESPHome**
3. Add device and enter API encryption key from `esphome/secrets.yaml`

### 7. Register NFC Tags

As you assign tags:
1. Scan a tag in Home Assistant (use developer tools or mobile app)
2. Go to **Settings** → **Tags**
3. Name the tag and set an identifier
4. Create automation using the tag trigger
5. Update `cards/tag_mapping.csv` with assignments

## Customizing Automations

### Adding a New Playlist Tag

1. Edit `home-assistant/packages/nfc_tags.yaml`
2. Duplicate the example automation
3. Update the tag ID and playlist URI
4. Reload automations or restart Home Assistant

Example:

```yaml
- id: nfc_tag_chill_vibes
  alias: "NFC: Play Chill Vibes Playlist"
  trigger:
    - platform: event
      event_type: tag_scanned
      event_data:
        tag_id: "04-AB-CD-EF-12-34-56"  # Your tag UID
  action:
    - service: script.nfc_play_spotify_playlist
      data:
        playlist_uri: "spotify:playlist:37i9dQZF1DWZd79rJ6a7lp"
        speaker: media_player.stue
        volume: 60
        mood: "Chill"
```

### Adjusting Button Functions

Edit `audio_control.yaml` and modify the button automations to trigger different actions.

## Entity Reference

### Input Helpers

| Entity ID | Description | Default |
|-----------|-------------|---------|
| `input_boolean.party_mode` | Party mode active state | Off |
| `input_select.music_mood` | Current music mood | Off |
| `input_number.party_volume` | Party mode volume % | 70 |

### Counters

| Entity ID | Description |
|-----------|-------------|
| `counter.songs_played_today` | Songs played today (resets at midnight) |

### ESP32 Entities

| Entity ID | Description |
|-----------|-------------|
| `sensor.nfc_party_controller_volume_pot` | Potentiometer value (0-100%) |
| `binary_sensor.nfc_party_controller_button_1` | Button 1 state |
| `binary_sensor.nfc_party_controller_button_2` | Button 2 state |
| `binary_sensor.nfc_party_controller_button_3` | Button 3 state |

### Media Players

| Entity ID | Room | Device |
|-----------|------|--------|
| `media_player.stue` | Living Room | Beoconnect Core |
| `media_player.kontor` | Office | Beoplay M5 |
| `media_player.køkken` | Kitchen | Beoplay M5 |

**Note**: Verify actual entity IDs in Home Assistant - they may differ based on configuration.

## Troubleshooting

### Packages not loading

- Check `configuration.yaml` has the correct `packages:` line
- Ensure YAML syntax is valid (use YAML validator)
- Check Home Assistant logs for errors
- Restart Home Assistant after changes

### Tags not triggering automations

- Verify tag is registered in **Settings** → **Tags**
- Check automation trigger uses correct event data format
- Enable debug logging for automations
- Test tag scanning in Developer Tools → Events (listen for `tag_scanned`)

### Volume control not working

- Verify `sensor.nfc_party_controller_volume_pot` is updating
- Check rate limiting condition in automation
- Ensure media player entity IDs are correct
- Test with manual volume service calls

### Spotify playlists not playing

- Verify Spotify integration is working
- Check playlist URIs are correct format
- Ensure speaker supports Spotify playback
- Test manual playlist playback first

## Further Reading

- [Home Assistant Packages Documentation](https://www.home-assistant.io/docs/configuration/packages/)
- [Bang & Olufsen Integration](https://www.home-assistant.io/integrations/bang_olufsen/)
- [Spotify Integration](https://www.home-assistant.io/integrations/spotify/)
- [ESPHome Integration](https://www.home-assistant.io/integrations/esphome/)
