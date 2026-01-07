# Hardware Documentation

This directory contains hardware documentation, schematics, and bill of materials for the NFC Party Controller.

## Hardware Overview

**Main Controller**: ESP32 USB-C IoT DevKitC (esp32dev board, ESP-IDF framework)

The project uses two identical ESP32 controllers with slightly different configurations:
- **Device 1**: NFC reader, buzzer, volume control
- **Device 2**: NFC reader, buzzer, volume control, **+ pause/play button**

---

## Device Comparison

| Feature | Device 1 | Device 2 |
|---------|----------|----------|
| NFC Reader (PN532) | ✅ | ✅ |
| Buzzer Feedback | ✅ | ✅ |
| Volume Potentiometer | ✅ | ✅ |
| Pause/Play Button | ❌ | ✅ |
| **Location** | Living Room (Stue) | Kitchen (Kokken) |

---

## Component List

### Device 1 Components

| Component | Model/Spec | GPIO Pin | Purpose |
|-----------|------------|----------|---------|
| ESP32 Board | ESP32 DevKitC USB-C | - | Main microcontroller |
| NFC Reader | PN532 | I2C (SDA=21, SCL=22) | Read NTAG215 tags |
| Potentiometer | 10kΩ linear | GPIO34 (ADC) | Volume control (0-75%) |
| Buzzer | 5V passive buzzer | GPIO23 (via MOSFET) | Audio feedback |
| MOSFET | 2N7000 N-channel | GPIO23 (gate) | 5V buzzer driver |
| Flyback Diode | 1N5818 Schottky | Across buzzer | Inductive spike protection |

### Device 2 Components

| Component | Model/Spec | GPIO Pin | Purpose |
|-----------|------------|----------|---------|
| *(All Device 1 components)* | | | |
| **Pause/Play Button** | Tactile switch | **GPIO18** | Pause/resume playback |

---

## Circuit Schematics

### Buzzer MOSFET Switching Circuit

The buzzer requires 5V but the ESP32 GPIO outputs 3.3V. A MOSFET switching circuit allows the ESP32 to control the 5V passive buzzer:

```
                    +5V
                     |
                     |
                 [Buzzer]
                     |
                     +---- Anode of D1 (1N5818)
                     |
                  Drain
                     |
                [MOSFET] 2N7000 (N-channel)
                     |
Gate (GPIO 23) ------+---- Gate
                     |
                  Source
                     |
                    GND
```

**Components**:
- **MOSFET**: 2N7000 (logic-level N-channel MOSFET)
  - V_GS(th): 2.1V max (can be driven by 3.3V GPIO)
  - I_D(max): 200mA
  - V_DS(max): 60V
- **Diode**: 1N5818 Schottky diode
  - Forward voltage: 0.45V @ 1A
  - Purpose: Flyback protection for inductive buzzer load
- **Buzzer**: 5V passive buzzer (PWM-driven via LEDC)

**Operation**:
1. GPIO 23 HIGH (3.3V PWM) → MOSFET conducts → Buzzer sounds
2. GPIO 23 LOW (0V) → MOSFET off → Buzzer silent
3. Diode protects against voltage spikes when buzzer turns off

---

### PN532 I2C Connection

```
ESP32                   PN532 Module
-----                   ------------
3.3V  ----------------  VCC
GND   ----------------  GND
GPIO 21 (SDA) --------  SDA
GPIO 22 (SCL) --------  SCL
```

**Important**: Ensure PN532 is set to I2C mode (check DIP switches on module).

---

### Button Connection (Device 2 Only)

The pause/play button uses ESP32's internal pullup resistor:

```
ESP32                   Button
-----                   ------
GPIO 18 --------------  Pin 1
GND    ----------------  Pin 2
```

**Logic**: Button press connects GPIO to GND (active LOW with internal pullup).

**Configuration**:
- Internal pullup enabled
- Inverted logic (pressed = HIGH signal)
- Debounce: 10ms delayed_on/delayed_off

---

### Potentiometer Connection

```
ESP32                   Potentiometer (10kΩ)
-----                   --------------------
3.3V  ----------------  Pin 1 (VCC)
GPIO 34 (ADC) --------  Pin 2 (Wiper)
GND   ----------------  Pin 3 (GND)
```

**ADC Configuration**:
- 12dB attenuation for full 0-3.3V range
- Calibrated voltage range: 0.142V - 3.118V
- Output range: 0-75% (clamped to prevent excessive volume)
- Filtering: 5-sample sliding window moving average
- Delta threshold: 2% (reduces noise)
- Update interval: 100ms

**Note**: Volume is intentionally clamped at 75% to prevent guests from turning speakers too loud for comfortable conversation.

---

## Bill of Materials (BOM)

### Per Device

| Qty | Component | Specification | Source |
|-----|-----------|---------------|--------|
| 1 | ESP32 DevKitC | USB-C version | AliExpress/Amazon |
| 1 | PN532 NFC Module | I2C interface, with antenna | AliExpress |
| 1 | Potentiometer | 10kΩ linear, PCB mount | Local electronics |
| 1 | Passive buzzer | 5V, through-hole | Local electronics |
| 1 | MOSFET | 2N7000 (N-channel, logic-level) | Local electronics |
| 1 | Schottky diode | 1N5818 | Local electronics |
| 1 | Breadboard/PCB | For prototyping | Local electronics |
| - | Jumper wires | M-M, M-F assortment | Local electronics |

### Device 2 Additional Component

| Qty | Component | Specification | Source |
|-----|-----------|---------------|--------|
| 1 | Tactile button | 12mm, through-hole | Local electronics |

### Shared Components (One-Time Purchase)

| Qty | Component | Specification | Source |
|-----|-----------|---------------|--------|
| 150 | NFC tags | NTAG215, 30mm stickers | Amazon |

---

## Assembly Instructions

### 1. ESP32 Setup

1. Connect ESP32 to computer via USB-C
2. Verify device is recognized
3. Note the COM port (for ESPHome upload)

### 2. PN532 NFC Reader

1. **Set I2C mode**: Check DIP switches on PN532 module
   - Usually: Switch 1 OFF, Switch 2 ON
2. **Connect to ESP32**:
   - VCC → 3.3V
   - GND → GND
   - SDA → GPIO 21
   - SCL → GPIO 22
3. **Test**: Upload ESPHome firmware and check logs for "PN532 initialized"

### 3. Potentiometer (Both Devices)

1. Connect outer pins to 3.3V and GND
2. Connect center (wiper) to GPIO 34
3. Test by reading ADC value in ESPHome logs
4. Calibrate voltage range if needed (current: 0.142-3.118V)

### 4. Buzzer Circuit (Both Devices)

1. **Place MOSFET**:
   - Gate → GPIO 23
   - Source → GND
   - Drain → Buzzer negative lead
2. **Connect buzzer**:
   - Positive lead → 5V (VIN pin on ESP32)
   - Negative lead → MOSFET drain
3. **Add flyback diode**:
   - Cathode (marked end) → 5V
   - Anode → MOSFET drain
4. **Test**: Trigger buzzer via ESPHome button entity in Home Assistant

### 5. Pause/Play Button (Device 2 Only)

1. Connect button to GPIO 18
2. Connect other pin of button to GND
3. Internal pullup is configured in firmware
4. Test using ESPHome logs when button is pressed

### 6. Final Assembly

1. Secure all components to breadboard or PCB
2. Double-check all connections
3. Upload final ESPHome configuration
4. Test all functions before enclosure

---

## Enclosure Design

### Requirements

- Accessible NFC reader area (top surface)
- Button access (Device 2)
- Potentiometer knob access
- USB-C port access (for programming/power)
- Ventilation for ESP32

### Enclosure Ideas

1. **3D Printed Custom Enclosure**
   - Design in Fusion 360 or Tinkercad
   - Print in PLA or PETG
   - Add decorative elements

2. **Project Box**
   - Hammond or similar ABS enclosure
   - Drill holes for button and potentiometer
   - Cut window for NFC reader

3. **Wooden Box**
   - Aesthetic vintage look
   - Route cable channels
   - Mount components with standoffs

---

## Power Considerations

**Power Source Options**:
1. **USB-C power** (recommended for desk use)
   - 5V, 1A minimum
   - Standard USB charger

2. **Battery powered** (optional, for portable use)
   - 3.7V LiPo battery with voltage regulator
   - Battery management module required
   - Check ESP32 power consumption

**Power Consumption** (Estimated):
- ESP32 (WiFi active): ~160-260mA
- PN532: ~100-150mA
- Buzzer (when active): ~30-50mA
- **Total: ~300-450mA (peak)**

---

## Safety Notes

- **ESD Protection**: Handle ESP32 with anti-static precautions
- **Polarity**: Double-check all power connections before powering on
- **MOSFET heat**: 2N7000 should not heat up significantly; if hot, check wiring
- **Short circuits**: Inspect for solder bridges or wire shorts before first power-on
- **Testing**: Test each component individually before full integration

---

## Future Improvements

- [ ] Custom PCB design (eliminate breadboard)
- [ ] Add LED indicators for visual feedback
- [ ] RGB LED strip control for party lighting integration
- [ ] Battery operation with charging circuit
- [ ] Add display (OLED) for track/status display
- [ ] Rotary encoder instead of potentiometer

---

## Troubleshooting

See `/docs/TROUBLESHOOTING.md` for common hardware issues and solutions.

---

## Resources

- [ESP32 Pinout Reference](https://randomnerdtutorials.com/esp32-pinout-reference-gpios/)
- [PN532 Module Guide](https://www.electrodragon.com/w/PN532_NFC_Module)
- [MOSFET Tutorial](https://learn.sparkfun.com/tutorials/transistors/applications-i-switches)
- [ESP32 ADC Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/adc.html)
- [ESPHome Documentation](https://esphome.io/)

---

**Status**: Hardware complete and operational, awaiting custom enclosure design
