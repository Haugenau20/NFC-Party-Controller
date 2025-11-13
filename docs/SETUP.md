# NFC Party Controller - Complete Setup Guide

This guide will walk you through setting up the NFC Party Controller from scratch.

## Prerequisites

### Hardware
- ESP32 USB-C IoT DevKitC
- PN532 NFC reader module
- All components from hardware/schematics/bom.csv
- Computer with USB port
- NTAG215 NFC tags

### Software
- Home Assistant installed and running
- Python 3.7 or newer
- Git (for version control)

### Accounts
- Spotify account (Premium recommended for full API access)
- Home Assistant cloud account (optional, for remote access)

---

## Part 1: Hardware Assembly

### Step 1: Assemble Components

Follow the instructions in hardware/README.md to:

1. Connect PN532 to ESP32 (I2C: GPIO 21/22)
2. Wire buttons to GPIO 18, 19, 5
3. Connect potentiometer to GPIO 34
4. Build MOSFET buzzer circuit (GPIO 23)
5. Verify all connections before powering on

**Verification**: Visual inspection of all wiring before first power-up.

---

## Part 2: ESPHome Setup

### Step 2: Install ESPHome

```bash
# Install ESPHome
pip install esphome

# Verify installation
esphome version
```

### Step 3: Configure Secrets

```bash
# Navigate to repository
cd nfc-party-controller

# Create secrets file
cp esphome/secrets.yaml.example esphome/secrets.yaml

# Edit with your credentials
nano esphome/secrets.yaml
```

Fill in:
- wifi_ssid: Your WiFi network name
- wifi_password: Your WiFi password
- api_encryption_key: Generate with: python3 -c "import secrets; print(secrets.token_hex(32))"
- ota_password: Your chosen OTA password

### Step 4: Compile and Upload Firmware

**First upload** (via USB):

```bash
# Connect ESP32 via USB-C
# Check device is recognized

# Compile and upload
esphome run esphome/nfc_controller.yaml

# Select serial port when prompted
```

**Monitor logs**:

```bash
esphome logs esphome/nfc_controller.yaml
```

**Verify**:
- WiFi connected
- PN532 initialized
- Buttons respond when pressed
- Potentiometer values change (0-100%)

---

## Part 3: Home Assistant Integration

### Step 5: Add ESP32 to Home Assistant

1. Go to Settings → Devices & Services
2. ESPHome integration should auto-discover the device
3. Click Configure
4. Enter API encryption key from secrets.yaml
5. Device "NFC Party Controller" should appear

### Step 6: Install Required Integrations

#### Bang & Olufsen

1. Settings → Devices & Services → Add Integration
2. Search for "Bang & Olufsen"
3. Configure each speaker

#### Spotify

1. Create Spotify Developer App at https://developer.spotify.com/dashboard
2. In Home Assistant: Add Spotify integration
3. Enter credentials and authorize

### Step 7: Configure Home Assistant Packages

Copy package files to your Home Assistant /config/packages/ directory and enable package loading in configuration.yaml.

### Step 8: Restart Home Assistant

Settings → System → Restart

---

## Part 4: NFC Tag Configuration

### Step 10: Register First Tag

1. Scan tag near PN532 reader
2. Check ESPHome logs for tag UID
3. Register in Home Assistant: Settings → Tags
4. Create automation for the tag

### Step 11: Get Spotify Playlist URIs

In Spotify app:
- Share playlist → Copy link
- Convert URL to URI format (spotify:playlist:ID)

---

## Part 5: Testing

Test buttons, potentiometer, NFC tags, and party mode functionality.

See docs/TROUBLESHOOTING.md for common issues.

---

**Congratulations!** Your NFC Party Controller is now operational.
