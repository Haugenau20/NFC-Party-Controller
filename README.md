# NFC Party Controller

> Physical NFC cards meet smart home automation for intuitive multi-room audio and party control

An interactive home automation system using NFC-enabled cards to control Spotify playlists, multi-room audio, and coordinated party experiences across Bang & Olufsen speakers.

**Status**: Early Development - Hardware configured, awaiting card printing for full deployment

---

## Features

- **100 Physical NFC Cards**: Tactile, intuitive music and scene control
- **Multi-Room Audio**: Seamless Beolink synchronization across Bang & Olufsen speakers
- **Spotify Integration**: Direct playlist control via NFC card scans
- **ESP32 Controller**: Custom hardware with buttons, volume control, and NFC reader
- **Event-Driven Architecture**: Scalable automation framework built on Home Assistant
- **Party Mode**: Coordinated audio, lighting, and automation scenes
- **Future**: Philips Hue lighting integration for synchronized visual experiences

## Demo

> Add photos/videos here: NFC cards, ESP32 controller, in-use demonstration

## Quick Start

### Prerequisites
- Home Assistant installation
- ESP32 DevKitC with USB-C
- PN532 NFC reader module
- NTAG215 NFC tags
- Python 3.7+ with pip

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/nfc-party-controller.git
cd nfc-party-controller
```

2. Set up ESPHome
```bash
pip install esphome
cp esphome/secrets.yaml.example esphome/secrets.yaml
# Edit secrets.yaml with your WiFi credentials
esphome run esphome/nfc_controller.yaml
```

3. Configure Home Assistant
```bash
# Copy packages to Home Assistant config directory
cp -r home-assistant/packages /config/packages/

# Edit configuration.yaml to enable packages
# Add: homeassistant:
#        packages: !include_dir_named packages/
```

4. Register NFC tags and create automations

Full setup guide: [docs/SETUP.md](docs/SETUP.md)

## Architecture

```
Physical Cards → PN532 NFC Reader → ESP32 (ESPHome)
                                       ↓
                              Home Assistant
                               ↓         ↓
                          Spotify    Bang & Olufsen
```

**Design Principles**:
- Event-driven NFC handling (no hardcoded tag IDs)
- Logic in Home Assistant, not ESP32 firmware
- Modular package-based configuration
- Native integration with audio systems

Read more: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Hardware

**ESP32 DevKitC** with:
- PN532 NFC reader (I2C)
- 3x tactile buttons (play/pause, next, group)
- 10kΩ potentiometer (volume control)
- 5V buzzer with MOSFET driver circuit
- Custom MOSFET switching for 5V components

**Bill of Materials**: ~$50-60 total cost

See: [hardware/README.md](hardware/README.md) for schematics and assembly guide

## Software Stack

- **ESPHome**: ESP32 firmware and hardware abstraction
- **Home Assistant**: Automation platform and integration hub
- **Spotify API**: Music playback control
- **Bang & Olufsen Integration**: Native Beolink multi-room audio
- **Future**: Philips Hue for synchronized lighting

## Project Structure

```
nfc-party-controller/
├── esphome/               # ESP32 firmware configuration
├── home-assistant/        # HA packages and config
│   └── packages/          # Modular automation packages
├── hardware/              # Schematics, BOM, photos
├── cards/                 # NFC tag mapping and printing guide
└── docs/                  # Setup, architecture, troubleshooting
```

## Key Files

- `esphome/nfc_controller.yaml` - ESP32 firmware config
- `home-assistant/packages/nfc_tags.yaml` - Tag event handling
- `home-assistant/packages/party_mode.yaml` - Party mode state management
- `home-assistant/packages/audio_control.yaml` - Multi-room audio control
- `cards/tag_mapping.csv` - Tag assignments (100 tags)

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
