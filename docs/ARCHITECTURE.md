# NFC Party Controller - Architecture

## System Overview

Multi-tier home automation combining hardware, firmware, and automation logic.

## Layers
1. Physical: NFC Cards → PN532 → ESP32
2. Firmware: ESPHome (hardware abstraction)
3. Automation: Home Assistant (business logic)
4. Services: Spotify API, Bang & Olufsen API

## Design Principles

### Separation of Concerns
- ESPHome handles hardware, events
- Home Assistant handles logic, integrations

### Event-Driven
- NFC tags send UIDs to HA
- No hardcoded tag IDs in firmware
- Scalable and flexible

### Modular Packages
- Each feature in separate YAML file
- Clean version control

## Key Decisions

**Event-based NFC**: Allows tag reassignment without firmware reflash
**HA Packages**: Modularity and maintainability
**Beolink over Chromecast**: Superior multi-room audio sync
**MOSFET buzzer circuit**: 5V buzzer from 3.3V logic
**ADC filtering**: Smooth potentiometer readings

## Security
- Encrypted API communication
- Secrets in gitignored files
- OAuth for Spotify

## Future
- Philips Hue lighting
- Guest DJ mode
- Usage analytics
