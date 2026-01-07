# NFC Party Controller

> Tap a card. Play a playlist. Control your home.

A battery-powered, event-driven home automation system using custom ESP32 hardware and NFC cards to control Spotify playback and Philips Hue lighting. Built with ESPHome and Home Assistant, this project showcases embedded systems design, IoT integration, and smart home architecture.

---

## What It Does

**Physical NFC cards** trigger Spotify playlists, lighting scenes, and system controls through two battery-powered ESP32 devices strategically placed in my home.

- **Music Control**: Scan a card to start a playlist, rotate the potentiometer to adjust volume, press the pause button (kitchen device)
- **Lighting Automation**: NFC cards trigger Philips Hue lighting scenes coordinated with music playback
- **Admin Functions**: Dedicated NFC cards reset playback queue, toggle permissions, restart system, or control smart plugs
- **Battery-Powered**: Each device runs 40-60 hours on 18650 lithium-ion cells with WiFi power-saving optimizations
- **Event-Driven**: NFC tag IDs aren't hardcoded in firmware—all logic lives in Home Assistant for easy reconfiguration
- **Dual Devices**: Living room device with volume control, kitchen device adds a physical pause button

## Demo

_Photos and videos to be added: Hardware assembly, NFC cards in use, device enclosures_

---

## Technical Highlights

### Hardware Design

**Custom ESP32 Controller** built from scratch with hand-soldered components on protoboard:
- **PN532 NFC Reader**: I2C communication (GPIO 21/22) for reading NTAG215 cards
- **10kΩ Potentiometer**: ADC input (GPIO 34) with 12dB attenuation for volume control
- **2N7000 MOSFET Circuit**: Level-shifted buzzer driver with 100Ω gate resistor and 1N5818 flyback diode for driving 5V passive buzzer from 3.3V GPIO
- **Pause Button**: GPIO 18 pullup input (Device 2 only)
- **Battery System**: 18650 lithium-ion cells (2x for Device 1, 1x for Device 2) with charging circuit

**Power Optimization Challenges**:
- Achieved 40-60 hour battery life through ESPHome WiFi light sleep mode
- PN532 duty cycle optimization (1s scan interval, 100-200ms active scanning)
- Average power draw: 100-150mA per device

### Firmware Architecture

**ESPHome Configuration**:
- **Modular Package System**: `common.yaml` contains shared configuration, device-specific files extend it
- **ADC Filtering**: Sliding window moving average + delta filter eliminates potentiometer noise
- **75% Volume Clamp**: Prevents guests from setting excessive volume levels
- **RTTTL Buzzer Feedback**: PWM-driven audio feedback on NFC scan events

### Software Design

**Event-Driven Architecture**:
- ESP32 devices emit NFC tag events to Home Assistant (no business logic in firmware)
- All playlist assignments, lighting triggers, and automation logic in Home Assistant
- Tags can be reassigned without reflashing firmware

**Home Assistant Integration**:
- **Spotcast**: Handles Spotify playback initiation and speaker targeting
- **SpotifyPlus**: Provides Spotify API access for advanced controls
- **Philips Hue**: Synchronized lighting scenes triggered by NFC cards
- **Automations/Scripts/Blueprints**: Modular YAML configuration organized by function

---

## System Architecture

```
NFC Cards → PN532 Readers → ESP32 Devices (ESPHome)
                                  ↓
                         Home Assistant
                          ↓      ↓      ↓
                     Spotify  Hue  Admin Controls
```

**Design Principles**:
- **Separation of Concerns**: ESPHome handles hardware events, Home Assistant handles all business logic
- **Event-Driven**: NFC tags emit events; no hardcoded tag IDs in firmware allows flexible reassignment
- **Modular Configuration**: Automations organized by function (device controls, NFC admin, lighting, Spotify integrations)
- **Security**: API encryption, OAuth tokens, secrets in gitignored files

See detailed architecture decisions: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## Hardware Details

**Two ESP32 DevKitC USB-C Controllers** with hand-soldered protoboard assembly:
- PN532 NFC reader module (I2C communication)
- 10kΩ linear potentiometer for volume control
- 2N7000 MOSFET buzzer driver circuit (5V passive buzzer)
- GPIO pause button (Device 2 only)
- 18650 lithium-ion battery system with charging circuit
- All components chosen for low power consumption

See complete schematics, pinouts, and assembly notes: [hardware/README.md](hardware/README.md)

## Technology Stack

**Firmware**:
- [ESPHome](https://esphome.io/) - ESP32 firmware framework with YAML configuration

**Platform**:
- [Home Assistant](https://www.home-assistant.io/) - Automation platform and integration hub

**Integrations**:
- [Spotcast](https://github.com/fondberg/spotcast) - Spotify playback control
- [SpotifyPlus](https://github.com/thlucas1/homeassistantcomponent_spotifyplus) - Spotify Web API integration
- [Philips Hue](https://www.home-assistant.io/integrations/hue/) - Smart lighting control

---

## Project Structure

```
nfc-party-controller/
├── esphome/                    # ESP32 firmware configurations
│   ├── common.yaml             # Shared device configuration
│   ├── nfc_controller_1.yaml  # Device 1 (living room)
│   └── nfc_controller_2.yaml  # Device 2 (kitchen with pause button)
├── home-assistant/             # Home Assistant automations and configs
│   ├── device_controls/        # Volume and button automations
│   ├── nfc_admin/              # Admin card functions
│   ├── spotcast/               # Spotify playback scripts
│   ├── spotifyplus/            # Spotify API automations
│   └── lighting/               # Hue lighting automations
├── hardware/                   # Schematics, pinouts, assembly notes
│   ├── README.md               # Hardware documentation
│   └── schematics/             # Circuit diagrams and pinout tables
└── docs/                       # Architecture and troubleshooting
    ├── ARCHITECTURE.md         # System design and decisions
    └── TROUBLESHOOTING.md      # Common issues and solutions
```

## Use Cases

**Music Control**:
- Scan "Energetic Party Mix" card → Spotify playlist starts on all speakers
- Rotate volume knob → All speakers adjust in sync
- Press button → Skip track or toggle play/pause

**Party Mode**:
- Scan "Party Mode" card → Activates party mode, sets volume, future: lighting scenes
- Mood-based automation (energetic, chill, romantic, focus)
- Track song play count and statistics

**Multi-Room**:
- Group all Bang & Olufsen speakers with single button
- Room-specific cards (office, kitchen, living room)
- Native Beolink synchronization for superior audio quality

## Technical Highlights

**Hardware**:
- Logic-level MOSFET switching for 5V buzzer from 3.3V GPIO
- ADC filtering (sliding window + delta) for smooth potentiometer readings
- I2C communication with PN532 NFC module
- Flyback diode protection for inductive loads

**Software**:
- Event-driven architecture (no hardcoded tag IDs in firmware)
- Home Assistant package system for modular configuration
- Generic script templates for scalable tag automation
- Native integration with Bang & Olufsen Beolink

**Best Practices**:
- Separation of concerns (ESPHome = hardware, HA = logic)
- Gitignored secrets for security
- Comprehensive documentation
- Version-controlled configuration

## Roadmap

### Current Progress
- [x] ESP32 hardware assembly
- [x] PN532 NFC reader integration
- [x] ESPHome firmware with buttons, potentiometer, buzzer
- [x] Home Assistant package structure
- [x] Bang & Olufsen speaker integration
- [x] Basic Spotify control

### Next Steps
- [ ] Print and assign 100 NFC cards
- [ ] Create card designs and templates
- [ ] Add Philips Hue integration
- [ ] Build custom enclosure for ESP32
- [ ] Create Lovelace dashboard for manual control
- [ ] Implement guest DJ mode
- [ ] Add usage analytics and statistics

## Documentation

- [Setup Guide](docs/SETUP.md) - Complete installation instructions
- [Architecture](docs/ARCHITECTURE.md) - System design and decisions
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [Hardware](hardware/README.md) - Schematics and assembly
- [Card Printing](cards/printing_guide.md) - NFC card design and printing

## License

MIT License - see [LICENSE](LICENSE)

## Acknowledgments

- ESPHome community for excellent ESP32 framework
- Home Assistant for powerful automation platform
- Bang & Olufsen for native Beolink integration
- Spotify API for music control

## Contact

**Developer**: Søren  
**Location**: Haderslev, South Denmark, DK  
**GitHub**: [Your GitHub Profile]  
**Portfolio**: [Your Portfolio]

---

Built with passion for music, technology, and great parties.
