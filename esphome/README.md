# ESPHome Configuration

This directory contains the ESPHome firmware configuration for the NFC Party Controller ESP32 board.

## Hardware

**Board**: ESP32 USB-C IoT DevKitC

**Components**:
- PN532 NFC Reader (I2C: SDA=GPIO21, SCL=GPIO22)
- 3x GPIO Buttons (GPIO18, GPIO19, GPIO5) with internal pullups
- Potentiometer for volume control (GPIO34, analog input)
- Buzzer (GPIO25, DAC output) - **Note**: Physical circuit uses GPIO23 with 5V MOSFET (IRLD120 + 1N5818 diode)
- Status LED (GPIO2, built-in)

## Files

- `nfc_controller.yaml` - Main ESPHome configuration
- `secrets.yaml.example` - Template for credentials (copy to `secrets.yaml`)
- `secrets.yaml` - Your actual credentials (gitignored)

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

**First time** (via USB):
```bash
esphome run nfc_controller.yaml
```

**Subsequent updates** (via OTA):
```bash
esphome upload nfc_controller.yaml
```

### 4. View Logs

```bash
esphome logs nfc_controller.yaml
```

## Configuration Details

### NFC Reader (PN532)

The PN532 is configured in I2C mode and sends tag scan events to Home Assistant:

- When a tag is scanned, the UID is sent to HA via `homeassistant.tag_scanned`
- Home Assistant's native tag management maps tag IDs to automation actions
- Audio feedback plays on successful scan

**No tag IDs are hardcoded in ESPHome** - all logic is in Home Assistant for easy maintenance.

### Volume Potentiometer

Configured with specific parameters for smooth, responsive control:

- **11db attenuation**: Full 0-3.3V range
- **Sliding window average**: 5 samples to smooth out noise
- **Delta filter**: Only updates when change > 2% to reduce unnecessary events
- **100ms update interval**: Responsive but not overwhelming

### Buttons

Three GPIO buttons with internal pullups (inverted logic):

- Button 1 (GPIO18) - Radio control
- Button 2 (GPIO19) - Channel selection  
- Button 3 (GPIO5) - Additional control

Each button sends an event to Home Assistant when pressed, allowing flexible automation without firmware changes.

### Buzzer Circuit

**Important**: The YAML uses GPIO25 (DAC output) for the RTTTL component, but the physical buzzer is connected to GPIO23 via a 5V MOSFET switching circuit:

- MOSFET: IRLD120 (logic-level N-channel)
- Flyback diode: 1N5818 Schottky
- This allows driving a 5V buzzer from 3.3V GPIO logic

If you're using a 3.3V piezo buzzer directly, you can connect it to GPIO25 without the MOSFET circuit.

## Integration with Home Assistant

After uploading the firmware:

1. ESP32 should appear in Home Assistant integrations
2. Accept the device and enter your API encryption key
3. All sensors, buttons, and NFC events will be available in HA
4. Configure automations in Home Assistant to respond to tag scans

See `../home-assistant/README.md` for Home Assistant setup details.

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

## Pin Reference

| Component | GPIO | Notes |
|-----------|------|-------|
| NFC SDA | 21 | I2C data |
| NFC SCL | 22 | I2C clock |
| Button 1 | 18 | Internal pullup |
| Button 2 | 19 | Internal pullup |
| Button 3 | 5 | Internal pullup |
| Volume Pot | 34 | ADC, 11db attenuation |
| Buzzer | 25 | DAC output (or GPIO23 with MOSFET) |
| Status LED | 2 | Built-in LED |

## Further Reading

- [ESPHome Documentation](https://esphome.io/)
- [PN532 Component](https://esphome.io/components/binary_sensor/pn532.html)
- [Home Assistant Integration](https://esphome.io/components/api.html)
