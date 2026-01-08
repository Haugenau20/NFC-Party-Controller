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

## Related Project: Visual Dashboard

This NFC controller can be enhanced with an optional **real-time visualization dashboard**:

**[New Year Dashboard](https://github.com/Haugenau20/new-year-dashboard)** - React/TypeScript web application providing:
- Real-time Spotify playback display with album artwork and dynamic backgrounds
- Special song detection (highlights tracks triggered by NFC cards)
- Integration with Home Assistant API and Spotify Web API
- Built for New Year celebration, adaptable for general "now playing" displays

The dashboard is **purely a visual enhancement** - the NFC controller functions completely independently. Together, they demonstrate a full-stack IoT ecosystem from embedded hardware to modern web frontend.

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

---

## Key Features Demonstrated

**Embedded Systems**:
- Custom circuit design with MOSFET-based level shifting
- ADC signal processing with multi-stage filtering
- I2C peripheral communication
- Power optimization for battery operation

**IoT Integration**:
- WiFi-connected ESP32 with OTA firmware updates
- Event-driven architecture with Home Assistant API
- OAuth-based Spotify API integration
- RESTful API interactions with Philips Hue

**Problem Solving**:
- 75% volume clamp to prevent excessive volume in social settings
- Delta filtering to reduce unnecessary network traffic from potentiometer updates
- WiFi light sleep mode achieving 40-60 hour battery life
- NFC duty cycle optimization balancing responsiveness and power consumption

---

## Documentation

- [System Architecture](docs/ARCHITECTURE.md) - Design principles and key technical decisions
- [Hardware Details](hardware/README.md) - Complete schematics, pinouts, and component selection rationale
- [ESPHome Configuration](esphome/README.md) - Firmware architecture and configuration details
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md) - Hardware and software debugging reference

---

## About This Project

This project represents a practical exploration of embedded systems, IoT integration, and home automation. It demonstrates end-to-end system design from hardware assembly through firmware development to application-level automation logic.

**Technical Skills Showcased**:
- Embedded C/C++ (ESP32/ESPHome)
- Circuit design and prototyping
- YAML-based declarative configuration
- API integration (Spotify, Philips Hue)
- Git-based version control and documentation

---

## License

MIT License - See [LICENSE](LICENSE) for details

---

**Developer**: Søren
**Location**: Haderslev, South Denmark
**Built**: 2024-2025
