# ESP32 Pinout Reference - NFC Party Controller

## Pin Assignments

| GPIO | Function | Component | Notes |
|------|----------|-----------|-------|
| GPIO 2 | Status LED | Built-in LED | Active HIGH |
| GPIO 5 | Digital Input | Button 3 | Pullup enabled, active LOW |
| GPIO 18 | Digital Input | Button 1 | Pullup enabled, active LOW |
| GPIO 19 | Digital Input | Button 2 | Pullup enabled, active LOW |
| GPIO 21 | I2C SDA | PN532 NFC Reader | Default I2C SDA |
| GPIO 22 | I2C SCL | PN532 NFC Reader | Default I2C SCL |
| GPIO 23 | Digital Output | Buzzer (MOSFET gate) | Drives 5V buzzer via IRLD120 |
| GPIO 25 | DAC Output | (Alternative buzzer) | Can use DAC for RTTTL tones |
| GPIO 34 | ADC Input | Volume Potentiometer | Input-only, no pullup available |

## Notes

### Input-Only Pins (GPIO 34-39)
- GPIO 34 is used for the potentiometer
- These pins do NOT have internal pullups
- Only suitable for analog input or external pullup circuits

### I2C Bus
- Default pins: SDA=21, SCL=22
- Can be changed in ESPHome configuration if needed
- External pullup resistors (4.7kΩ) usually included on PN532 module

### PWM Capable Pins
- Most GPIOs support PWM for buzzer control
- DAC pins (25, 26) can generate analog waveforms

### Boot Mode Pins (Avoid if possible)
- GPIO 0: Boot mode selection (pulled HIGH on boot)
- GPIO 12: Boot voltage selection
- Avoid using these for critical functions that might interfere with boot

## Reserved/Used Pins

**Do NOT use**:
- GPIO 1: TX (serial) - used for logging
- GPIO 3: RX (serial) - used for logging
- GPIO 6-11: Flash memory - **NEVER USE**

## Available for Future Expansion

| GPIO | Type | Notes |
|------|------|-------|
| GPIO 4 | I/O | Available |
| GPIO 12 | I/O | Available (boot voltage pin - use with caution) |
| GPIO 13 | I/O | Available |
| GPIO 14 | I/O | Available |
| GPIO 15 | I/O | Available |
| GPIO 16 | I/O | Available |
| GPIO 17 | I/O | Available |
| GPIO 26 | I/O/DAC | Available (DAC2) |
| GPIO 27 | I/O | Available |
| GPIO 32 | I/O/ADC | Available (ADC1_CH4) |
| GPIO 33 | I/O/ADC | Available (ADC1_CH5) |
| GPIO 35 | Input Only/ADC | Available (ADC1_CH7) |
| GPIO 36 (VP) | Input Only/ADC | Available (ADC1_CH0) |
| GPIO 39 (VN) | Input Only/ADC | Available (ADC1_CH3) |

## Power Pins

- **3.3V**: Regulated 3.3V output (max 600mA)
- **5V (VIN)**: Connected to USB 5V (use for 5V buzzer)
- **GND**: Multiple ground pins available
- **EN**: Enable pin (pulled HIGH normally)

## Expansion Ideas

Use available pins for:
- RGB LED strip (WS2812B) on GPIO 4
- Additional NFC readers (separate I2C addresses)
- Rotary encoder for volume (GPIO 13, 14)
- OLED display (share I2C bus with PN532)
- Additional buttons or sensors

## Schematic Symbol

```
                   ESP32 DevKitC
           ┌─────────────────────────┐
       3V3 │1                     23│ GPIO 23 → Buzzer MOSFET
       EN  │2                     22│ GPIO 22 → PN532 SCL
  VP (36)  │3                     TX│ (Serial)
  VN (39)  │4                     RX│ (Serial)
   GPIO 34 │5   ← Potentiometer  21│ GPIO 21 → PN532 SDA
   GPIO 35 │6                     19│ GPIO 19 → Button 2
   GPIO 32 │7                     18│ GPIO 18 → Button 1
   GPIO 33 │8                      5│ GPIO 5  → Button 3
   GPIO 25 │9                     17│
   GPIO 26 │10                    16│
   GPIO 27 │11                     4│
   GPIO 14 │12                     2│ → Status LED
   GPIO 12 │13                    15│
       GND │14                   GND│
           └─────────────────────────┘
```

---

Use this reference when adding new components or troubleshooting connections.
