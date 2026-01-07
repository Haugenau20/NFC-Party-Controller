# NFC Party Controller - Architecture

## System Overview

Multi-tier home automation system combining battery-powered ESP32 hardware, ESPHome firmware, and Home Assistant automation logic for music and lighting control via NFC cards.

## Layers
1. Physical: NFC Cards → PN532 → ESP32 (two devices: living room + kitchen)
2. Firmware: ESPHome (hardware abstraction, event-driven)
3. Automation: Home Assistant (business logic, automations, scripts, blueprints)
4. Services: Spotify (Spotcast/SpotifyPlus), Philips Hue

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
**HA Automations/Scripts/Blueprints**: Modularity and maintainability
**Spotcast + SpotifyPlus**: Dual Spotify integrations for playback control and API access
**Battery-powered**: 18650 lithium-ion cells (2x Device 1, 1x Device 2) with WiFi power save mode
**MOSFET buzzer circuit**: 5V passive buzzer driven from 3.3V GPIO via 2N7000 with 100Ω gate resistor
**ADC filtering + 75% clamp**: Smooth potentiometer readings, prevent excessive volume
**Two devices**: Device 1 (living room), Device 2 (kitchen with pause button)

## Security
- Encrypted API communication
- Secrets in gitignored files
- OAuth for Spotify

## Components

**Hardware**: PN532 NFC reader, 10kΩ volume potentiometer, 2N7000 MOSFET buzzer circuit, GPIO pause button (Device 2)
**Firmware**: ESPHome with modular package system (common.yaml shared config)
**NFC Functions**: Music playback, lighting control, NFC admin cards (queue reset, permissions, system controls)
**Integrations**: Spotify playback (Spotcast), Spotify API (SpotifyPlus), Philips Hue lighting
