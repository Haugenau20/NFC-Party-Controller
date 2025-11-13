# NFC Party Controller - Smart Home Automation Project

## Project Overview

An interactive home automation system using physical NFC-enabled cards to control multi-room audio, lighting, and party experiences. Users scan cards to trigger Spotify playlists, lighting scenes, and coordinated home automation routines.

**Status**: Early development - hardware configured, awaiting card printing for full integration

## Goals

### Primary Goals
- Create 50-100 physical NFC cards for tactile music/scene control
- Seamless multi-room audio control via Bang & Olufsen Beolink
- Coordinated lighting and audio experiences
- Scalable, maintainable automation framework
- Portfolio-ready codebase with excellent documentation

### Technical Goals
- Professional Git workflow with proper version control
- Clean separation between ESPHome (hardware) and Home Assistant (logic)
- Event-based NFC handling (not hardcoded tag IDs in ESPHome)
- Reproducible setup that others can learn from

## Current Hardware Setup

### Audio System
- **Beoplay M5** ("Kontor") - Office speaker
- **Beoplay M5** ("Køkken") - Kitchen speaker
- **Beoconnect Core** ("Stue") - Living room 
- Native Beolink multiroom support for the Core (superior to Chromecast grouping)
- Spotify integration for playback

### ESP32 Control Board
- **Board**: ESP32 USB-C IoT DevKitC
- **Components configured**:
  - Buttons on GPIO for radio control and channel selection
  - Potentiometer for volume (GPIO with 12db attenuation, sliding window averaging, delta filtering)
  - Buzzer on GPIO23 (5V via MOSFET switching circuit - IRLD120 MOSFET, 1N5818 Schottky diode)
  - PN532 NFC reader (I2C connection) - ready but not yet tested with tags

### NFC Tags
- **Quantity**: 150 tags on roll
- **Type**: NTAG215 (assumed standard)
- **Status**: Unassigned - waiting for card printing to integrate
- **Strategy**: Will use Home Assistant's native tag management, not hardcoded in ESPHome

### Planned Additions
- Philips Hue lighting integration
- Additional room coverage
- Custom enclosure for ESP32 control board

## Technical Stack

### Software
- **Home Assistant**: Main automation platform
- **ESPHome**: ESP32 firmware and hardware abstraction
- **Spotify API**: Music playback via Bang & Olufsen integration
- **Git/GitHub**: Version control and portfolio showcase

### Development Environment
- **Local ESPHome CLI**: Installed and ready for compilation
- **VSCode with Remote SSH**: For editing Home Assistant configs
- **Home Assistant OS**: Running on VM (considering migration to Home Assistant Yellow for Zigbee + SSD reliability)

## Architecture Decisions

### Key Principles
1. **Logic in Home Assistant, not ESPHome**: ESPHome exposes sensors/events, HA handles complex logic via automations
2. **Event-based NFC**: Tags trigger generic events, HA maps tag IDs to actions using native tag management
3. **Systematic debugging**: Hardware-first approach - configure ESPHome YAML → test onboard components → verify in HA → build automations
4. **Automation reliability**: HA automations > direct ESPHome service calls for complex integrations

### Hardware Design Patterns
- **Analog inputs**: Use specific ESPHome parameters (11db attenuation, sliding window averaging, delta filtering) for responsive control
- **Voltage level conversion**: MOSFET switching for 5V components (buzzer uses IRLD120 + 1N5818 Schottky diode)
- **Component verification**: Use onboard LEDs for debugging before integration

### Configuration Organization
```
home-assistant/
├── packages/
│   ├── nfc_tags.yaml        # NFC automation logic
│   ├── party_mode.yaml      # Party mode state and coordination
│   ├── audio_control.yaml   # Multi-room audio management
│   └── lighting_scenes.yaml # Hue integration (future)
├── blueprints/
│   └── nfc_action_template.yaml
└── dashboards/
    └── party_control.yaml   # Manual controls + testing interface

esphome/
├── nfc_controller.yaml      # Main ESP32 configuration
└── secrets.yaml            # Credentials (gitignored)
```

## Current State

### Working
✅ ESP32 hardware configured with buttons, potentiometer, buzzer
✅ Home Assistant integration established
✅ Bang & Olufsen speakers integrated with Beolink multiroom
✅ ESPHome CLI installed locally
✅ Basic understanding of HA/ESPHome workflow

### In Progress
🔄 NFC reader configured in ESPHome (not yet tested with tags)
🔄 Waiting for printer toner to print physical cards
🔄 Setting up Git workflow and repository structure

### To Do
⏳ Create tag mapping spreadsheet (ID → action assignments)
⏳ Set up Home Assistant helpers (input_boolean.party_mode, etc.)
⏳ Integrate Spotify control automations
⏳ Build NFC event handling automations
⏳ Create party mode dashboard
⏳ Add Philips Hue integration (when hardware available)
⏳ Design and print physical cards
⏳ Write comprehensive documentation for GitHub

## Integration Details

### Bang & Olufsen Integration
- Use `bang_olufsen` integration (native Beolink support)
- Entity IDs: `media_player.kontor`, `media_player.stue`
- Grouping via Beolink is more reliable than Chromecast alternatives
- Check entity naming in HA - may differ from expected formats

### ESPHome NFC Configuration
```yaml
# Current approach (to be implemented)
pn532_i2c:
  id: pn532_board

binary_sensor:
  - platform: pn532
    id: pn532_tag_reader
    on_tag:
      then:
        - homeassistant.tag_scanned: !lambda 'return x;'
```

This sends tag IDs to Home Assistant where native tag management maps IDs to automations.

### Planned Home Assistant Helpers
```yaml
input_boolean:
  party_mode:
    name: Party Mode Active
    icon: mdi:party-popper

input_select:
  music_mood:
    name: Music Mood
    options:
      - Energetic
      - Chill
      - Romantic
      - Focus
    icon: mdi:music

input_number:
  party_volume:
    name: Party Volume
    min: 0
    max: 100
    step: 5
    initial: 70
    unit_of_measurement: "%"

counter:
  songs_played:
    name: Songs Played Today
    icon: mdi:music-note
```

## File Structure for Repository

```
nfc-party-controller/
├── README.md                    # Main documentation
├── PROJECT.md                   # This file - project context
├── LICENSE                      # MIT or Apache 2.0
├── .gitignore                   # Secrets and generated files
├── hardware/
│   ├── schematics/
│   │   ├── buzzer_circuit.png
│   │   ├── esp32_pinout.md
│   │   └── bom.csv
│   ├── photos/
│   └── README.md
├── esphome/
│   ├── nfc_controller.yaml
│   ├── secrets.yaml.example
│   └── README.md
├── home-assistant/
│   ├── packages/
│   │   ├── nfc_tags.yaml
│   │   ├── party_mode.yaml
│   │   ├── audio_control.yaml
│   │   └── lighting_scenes.yaml
│   ├── blueprints/
│   ├── dashboards/
│   ├── configuration.yaml.example
│   └── README.md
├── cards/
│   ├── templates/
│   ├── tag_mapping.csv
│   └── printing_guide.md
└── docs/
    ├── SETUP.md
    ├── ARCHITECTURE.md
    ├── API.md
    └── TROUBLESHOOTING.md
```

## Development Workflow

### Current Workflow
1. Edit ESPHome YAML locally
2. Compile and upload: `esphome upload esphome/nfc_controller.yaml`
3. Edit Home Assistant configs via SSH in VSCode
4. Test in Home Assistant
5. Commit changes to Git
6. Document learnings

### SSH Access to Home Assistant
- Host: `homeassistant.local`
- Port: 22222 (typical)
- Config directory: `/config/`
- Install "Terminal & SSH" add-on in HA

## Next Immediate Tasks

1. **Initialize Git repository** with proper structure
2. **Copy current ESPHome config** to repo
3. **Create tag mapping spreadsheet** (50-100 entries)
4. **Set up Home Assistant helpers** (party mode, music mood, etc.)
5. **Integrate Spotify** and test B&O speaker control
6. **Write first NFC automation template**
7. **Create party mode dashboard** for manual testing
8. **Document hardware setup** with photos and schematics

## Questions to Resolve

- [ ] Exact PN532 I2C configuration (SDA/SCL pins on ESP32)
- [ ] Home Assistant Yellow migration timeline
- [ ] Philips Hue hardware availability
- [ ] Card design specifics (size, graphics, printing method)
- [ ] Enclosure requirements for ESP32 board

## Technical Notes

### Lessons Learned
- Component naming in HA may differ from expected formats - verify entity IDs
- HA automations more reliable than ESPHome service calls for complex logic
- Analog inputs need careful filtering: 12db attenuation + sliding window + delta filtering
- Beolink native grouping > Chromecast for B&O speakers
- Event-based NFC at scale > hardcoded tag IDs

### Design Patterns
- **Volume control**: ESPHome sensor → HA automation with rate limiting
- **Multi-room audio**: Group speakers via Beolink, sync volume
- **Party mode**: Master boolean triggers coordinated lighting + audio changes
- **NFC feedback**: Buzzer confirms scans, different tones for success/error

## Portfolio Presentation

This project demonstrates:
- **Hardware design**: Custom circuits with proper component selection
- **Embedded systems**: ESPHome firmware development for ESP32
- **Home automation**: Complex automation logic and system integration
- **API integration**: Spotify, Bang & Olufsen, Philips Hue
- **System architecture**: Event-driven design, separation of concerns
- **Documentation**: Professional README, architecture docs, setup guides
- **Version control**: Proper Git workflow, clean commit history

## Contact & Links

- **Developer**: Søren (Electronics & Software Engineer)
- **Location**: Haderslev, South Denmark, DK
- **GitHub**: [To be added]
- **Portfolio**: [To be added]

---

**Last Updated**: November 2025
**Version**: 0.1.0 - Initial project setup