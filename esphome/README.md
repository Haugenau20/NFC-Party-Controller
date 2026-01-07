# ESPHome Configuration

This directory contains ESPHome firmware configurations for the two NFC Party Controller devices.

For hardware details, circuit schematics, and assembly instructions, see [`/hardware/README.md`](/hardware/README.md).

---

## Device Overview

This project uses two ESP32 controllers with different firmware configurations:

- **Device 1** (`nfc_controller_1.yaml`) - Living Room (Stue)
- **Device 2** (`nfc_controller_2.yaml`) - Kitchen (Kokken) - adds pause/play button

See [`/hardware/README.md#device-comparison`](/hardware/README.md#device-comparison) for complete hardware specifications.

---

## Files

- `common.yaml` - Shared configuration for both devices (WiFi, API, NFC, buzzer, volume)
- `nfc_controller_1.yaml` - Device 1 firmware (Living Room)
- `nfc_controller_2.yaml` - Device 2 firmware (Kitchen, adds pause button)
- `nfc_controller_test.yaml` - Test configuration for hardware validation
- `secrets.yaml.example` - Template for credentials (copy to `secrets.yaml`)
- `secrets.yaml` - Your actual credentials (gitignored)

---

## Setup

### 1. Install ESPHome

```bash
pip install esphome
```

### 2. Create Secrets File

```bash
cp secrets.yaml.example secrets.yaml
```

Edit `secrets.yaml` with your WiFi credentials and API keys:

```yaml
wifi_ssid: "YourWiFiSSID"
wifi_password: "YourWiFiPassword"
api_encryption_key: "generate-with-python-command-below"
ota_password: "your-secure-password"
```

Generate encryption key:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Compile and Upload

Choose which device you're configuring (Device 1 or Device 2).

**First time** (via USB):
```bash
# For Device 1 (Living Room)
esphome run nfc_controller_1.yaml

# For Device 2 (Kitchen)
esphome run nfc_controller_2.yaml
```

**Subsequent updates** (via OTA):
```bash
# For Device 1
esphome upload nfc_controller_1.yaml

# For Device 2
esphome upload nfc_controller_2.yaml
```

### 4. View Logs

```bash
# For Device 1
esphome logs nfc_controller_1.yaml

# For Device 2
esphome logs nfc_controller_2.yaml
```

---

## Configuration Architecture

The configuration uses ESPHome's package system for code reuse:

- `common.yaml` contains shared components (imported by both device configs)
- Device-specific YAMLs add unique features (e.g., Device 2's pause button)
- **No tag IDs hardcoded in firmware** - all logic in Home Assistant
- **Event-driven**: Devices send events to HA, HA handles all logic

---

## Configuration Details

### NFC Reader (PN532)

**ESPHome Configuration**:
- I2C mode (SDA=GPIO21, SCL=GPIO22)
- Update interval: 1s
- Scan duration: ~100-200ms per second (10-20% duty cycle for power saving)

**Operation**:
- On tag scan: sends `homeassistant.tag_scanned` event with UID
- Plays quick beep for audio feedback (`scan:d=4,o=5,b=100:16e6`)
- All tag-to-action mapping handled in Home Assistant

For I2C wiring details, see [`/hardware/README.md#pn532-i2c-connection`](/hardware/README.md#pn532-i2c-connection).

---

### Volume Potentiometer

**ESPHome Configuration**:
```yaml
platform: adc
pin: GPIO34
attenuation: 12db              # Full 0-3.3V range
update_interval: 100ms         # Responsive but not overwhelming
filters:
  - sliding_window_moving_average:
      window_size: 5           # Smooth out noise
      send_every: 1
  - calibrate_linear:
      - 0.142 -> 0.0           # Measured voltage range
      - 3.118 -> 100.0
  - clamp:
      min_value: 0
      max_value: 75            # Prevent excessive volume
      ignore_out_of_range: true
  - delta: 2.0                 # Only send when >2% change
```

**Why these settings?**:
- **12dB attenuation**: Allows full voltage range from potentiometer
- **Sliding window**: Reduces electrical noise from long wires
- **Delta filter**: Prevents event spam from minor fluctuations
- **75% clamp**: Prevents guests from making speakers too loud for conversation

For circuit wiring, see [`/hardware/README.md#potentiometer-connection`](/hardware/README.md#potentiometer-connection).

---

### Buzzer

**ESPHome Configuration**:
```yaml
output:
  - platform: ledc            # PWM via LED Control peripheral
    pin: GPIO23               # Connected via MOSFET circuit
    id: buzzer_output

rtttl:
  output: buzzer_output
  id: buzzer_rtttl
```

**Sound Library**:
- **Success sounds**: Level Up, Party Horn, Mario, Fanfare (randomized)
- **Failure sound**: Buzz pattern
- **Master sounds**: Rising/falling frequency sweeps
- All sounds defined in `common.yaml` scripts

For MOSFET circuit details, see [`/hardware/README.md#buzzer-mosfet-switching-circuit`](/hardware/README.md#buzzer-mosfet-switching-circuit).

---

### Pause/Play Button (Device 2 Only)

**ESPHome Configuration**:
```yaml
binary_sensor:
  - platform: gpio
    pin:
      number: GPIO18
      mode:
        input: true
        pullup: true         # Internal pullup resistor
      inverted: true         # Active LOW (button connects to GND)
    filters:
      - delayed_on: 10ms     # Debounce
      - delayed_off: 10ms
    on_press:
      - homeassistant.event:
          event: esphome.speaker_button_pressed
          data:
            device: nfc-party-controller-2
```

Device 1 does not have this button configured.

For button wiring, see [`/hardware/README.md#button-connection-device-2-only`](/hardware/README.md#button-connection-device-2-only).

---

### Power Saving

**WiFi Configuration**:
```yaml
wifi:
  power_save_mode: light      # Reduces power between transmissions
```

This reduces average ESP32 power consumption from ~160-260mA to ~80-120mA.

For battery life estimates, see [`/hardware/README.md#power-considerations`](/hardware/README.md#power-considerations).

---

## Home Assistant Integration

After uploading firmware:

1. ESP32 device appears automatically in Home Assistant integrations
2. Accept the device and enter your API encryption key from `secrets.yaml`
3. All sensors, buttons, and NFC events available in HA
4. NFC tags trigger Home Assistant automations (see `/automations/` folder)

### Entities Exposed

**Both Devices**:
- `sensor.<device>_volume_pot` - Volume potentiometer (0-75%)
- `button.<device>_play_success` - Trigger success sound
- `button.<device>_play_failure` - Trigger failure sound
- `button.<device>_play_master` - Trigger admin sound
- `button.<device>_play_master_on` - Rising sweep sound
- `button.<device>_play_master_off` - Falling sweep sound

**Device 2 Only**:
- `binary_sensor.<device>_speaker_button` - Pause button state

### Events

- `tag_scanned` - NFC tag detected with UID
- `esphome.speaker_button_pressed` - (Device 2 only) Button pressed

---

## Troubleshooting

### Device won't connect to WiFi

- Check that `secrets.yaml` has correct credentials
- Look for fallback AP: "NFC Party Controller Fallback"
- Connect to it and configure WiFi via captive portal

### NFC tags not detected

- Verify I2C wiring: SDA=GPIO21, SCL=GPIO22
- Check ESPHome logs for PN532 initialization
- Ensure PN532 is in I2C mode (check DIP switches)
- Test with known-good NTAG215 tags

### Compilation errors

- Ensure ESPHome is up to date: `pip install -U esphome`
- Check YAML syntax (indentation must be exact)
- Review logs for specific error messages

### OTA updates fail

- Verify device is on same network
- Check OTA password matches `secrets.yaml`
- Try USB upload if OTA is problematic

### Hardware issues

For hardware troubleshooting (buzzer not working, button issues, etc.), see [`/hardware/README.md#troubleshooting`](/hardware/README.md#troubleshooting).

---

## Pin Reference

For complete pin assignments and available expansion pins, see [`/hardware/schematics/esp32_pinout.md`](/hardware/schematics/esp32_pinout.md).

---

## Resources

**ESPHome Components**:
- [ADC Sensor](https://esphome.io/components/sensor/adc.html)
- [RTTTL Component](https://esphome.io/components/rtttl.html)
- [Binary Sensor GPIO](https://esphome.io/components/binary_sensor/gpio.html)
- [Home Assistant Integration](https://esphome.io/components/api.html)
- [WiFi Component](https://esphome.io/components/wifi.html)

**Hardware Documentation**:
- [Hardware README](/hardware/README.md) - Circuit schematics and assembly
- [ESP32 Pinout](/hardware/schematics/esp32_pinout.md) - Complete pin reference
