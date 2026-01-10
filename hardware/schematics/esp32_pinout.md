# ESP32 Pinout Reference - NFC Party Controller

## Device Comparison

| Feature | Device 1 | Device 2 |
|---------|----------|----------|
| NFC Reader (PN532) | ✅ | ✅ |
| Buzzer Feedback | ✅ | ✅ |
| Volume Potentiometer | ✅ | ✅ |
| Pause/Play Button | ❌ | ✅ |

---

## Pin Assignments

### Used Pins

| GPIO | Function | Component | Device(s) | Notes |
|------|----------|-----------|-----------|-------|
| GPIO 18 | Digital Input | Pause/Play Button | **Device 2 only** | Pullup enabled, active LOW |
| GPIO 21 | I2C SDA | PN532 NFC Reader | Both | Default I2C SDA |
| GPIO 22 | I2C SCL | PN532 NFC Reader | Both | Default I2C SCL |
| GPIO 23 | PWM Output | Buzzer (MOSFET gate) | Both | Drives 5V passive buzzer via 2N7000 |
| GPIO 34 | ADC Input | Volume Potentiometer | Both | Input-only, no pullup available |

### Pin Configuration Details

**GPIO 34 - Volume Potentiometer:**
- ADC attenuation: 12dB
- Voltage range: 0.142V - 3.118V (calibrated)
- Output range: 0-75% (clamped to prevent excessive volume)
- Filtering: 5-sample sliding window + 2% delta threshold
- Update interval: 100ms

**GPIO 23 - Buzzer PWM:**
- MOSFET: 2N7000 N-channel
- Flyback diode: 1N5818 Schottky
- Buzzer type: 5V passive buzzer
- PWM via LEDC peripheral

**GPIO 18 - Pause/Play Button (Device 2):**
- Internal pullup enabled
- Active LOW (button press connects to GND)
- Debounce: 10ms delayed_on/delayed_off
- Sends ESPHome event to Home Assistant

---

## Notes

### Input-Only Pins (GPIO 34-39)
- GPIO 34 is used for the volume potentiometer
- These pins do NOT have internal pullups
- Only suitable for analog input or external pullup circuits

### I2C Bus
- Default pins: SDA=21, SCL=22
- Can be changed in ESPHome configuration if needed
- External pullup resistors (4.7kΩ) usually included on PN532 module

### PWM Capable Pins
- Most GPIOs support PWM for buzzer control
- Using LEDC (LED Control) peripheral for tone generation

---

## Reserved/Used Pins

**Do NOT use:**
- GPIO 1: TX (serial) - used for logging
- GPIO 3: RX (serial) - used for logging
- GPIO 6-11: Flash memory - **NEVER USE**

---

## Available for Future Expansion

| GPIO | Type | Notes |
|------|------|-------|
| GPIO 2 | I/O | Available (built-in LED not used) |
| GPIO 4 | I/O | Available |
| GPIO 5 | I/O | Available |
| GPIO 12 | I/O | Available (boot voltage pin - use with caution) |
| GPIO 13 | I/O | Available |
| GPIO 14 | I/O | Available |
| GPIO 15 | I/O | Available |
| GPIO 16 | I/O | Available |
| GPIO 17 | I/O | Available |
| GPIO 19 | I/O | Available (Device 1 only; used on Device 2 for future expansion) |
| GPIO 25 | I/O/DAC | Available (DAC2) |
| GPIO 26 | I/O/DAC | Available (DAC1) |
| GPIO 27 | I/O | Available |
| GPIO 32 | I/O/ADC | Available (ADC1_CH4) |
| GPIO 33 | I/O/ADC | Available (ADC1_CH5) |
| GPIO 35 | Input Only/ADC | Available (ADC1_CH7) |
| GPIO 36 (VP) | Input Only/ADC | Available (ADC1_CH0) |
| GPIO 39 (VN) | Input Only/ADC | Available (ADC1_CH3) |

---

## Power Pins

- **3.3V**: Regulated 3.3V output (max 600mA)
- **5V (VIN)**: Connected to USB 5V (use for 5V buzzer power)
- **GND**: Multiple ground pins available
- **EN**: Enable pin (pulled HIGH normally)

---

## Expansion Ideas

Use available pins for:
- RGB LED strip (WS2812B) on GPIO 4
- Additional NFC readers (separate I2C addresses)
- Rotary encoder for volume (GPIO 13, 14)
- OLED display (share I2C bus with PN532)
- Additional buttons or sensors
- Status indicator LEDs

---

## Schematic Symbol

```
                   ESP32 DevKitC
           ┌─────────────────────────┐
       3V3 │1                     23│ GPIO 23 → Buzzer MOSFET (2N7000)
       EN  │2                     22│ GPIO 22 → PN532 SCL
  VP (36)  │3                     TX│ (Serial - logging)
  VN (39)  │4                     RX│ (Serial - logging)
   GPIO 34 │5   ← Potentiometer  21│ GPIO 21 → PN532 SDA
   GPIO 35 │6                     19│ GPIO 19 (available)
   GPIO 32 │7                     18│ GPIO 18 → Pause Button (Device 2)
   GPIO 33 │8                      5│ GPIO 5 (available)
   GPIO 25 │9                     17│ GPIO 17 (available)
   GPIO 26 │10                    16│ GPIO 16 (available)
   GPIO 27 │11                     4│ GPIO 4 (available)
   GPIO 14 │12                     2│ GPIO 2 (available)
   GPIO 12 │13                    15│ GPIO 15 (available)
       GND │14                   GND│
           └─────────────────────────┘
```

---

Use this reference when adding new components or troubleshooting connections.
