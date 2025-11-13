# Hardware Documentation

This directory contains hardware documentation, schematics, photos, and bill of materials for the NFC Party Controller.

## Hardware Overview

**Main Controller**: ESP32 USB-C IoT DevKitC

### Components

| Component | Model/Spec | GPIO Pin | Purpose |
|-----------|------------|----------|---------|
| ESP32 Board | ESP32 DevKitC USB-C | - | Main microcontroller |
| NFC Reader | PN532 | SDA=21, SCL=22 | Read NTAG215 tags |
| Button 1 | Tactile switch | GPIO 18 | Play/Pause control |
| Button 2 | Tactile switch | GPIO 19 | Next track |
| Button 3 | Tactile switch | GPIO 5 | Group/ungroup speakers |
| Potentiometer | 10kΩ linear | GPIO 34 (ADC) | Volume control |
| Buzzer | 5V active buzzer | GPIO 23 (via MOSFET) | Audio feedback |
| MOSFET | IRLD120 | GPIO 23 (gate) | 5V buzzer driver |
| Flyback Diode | 1N5818 Schottky | Across buzzer | Inductive spike protection |
| Status LED | Built-in | GPIO 2 | Status indication |

## Circuit Schematics

### Buzzer MOSFET Switching Circuit

The buzzer requires 5V but the ESP32 GPIO outputs 3.3V. A MOSFET switching circuit allows the ESP32 to control the 5V buzzer:

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
                [MOSFET] IRLD120 (N-channel)
                     |
Gate (GPIO 23) ------+---- Gate
                     |
                  Source
                     |
                    GND
```

**Components**:
- **MOSFET**: IRLD120 (logic-level N-channel MOSFET)
  - V_GS(th): 1-2V (can be driven by 3.3V GPIO)
  - I_D(max): 3.1A
- **Diode**: 1N5818 Schottky diode
  - Forward voltage: 0.45V @ 1A
  - Purpose: Flyback protection for inductive buzzer load

**Operation**:
1. GPIO 23 HIGH (3.3V) → MOSFET conducts → Buzzer ON
2. GPIO 23 LOW (0V) → MOSFET off → Buzzer OFF
3. Diode protects against voltage spikes when buzzer turns off

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

### Button Connections

All buttons use internal pullup resistors (configured in ESPHome):

```
ESP32                   Button
-----                   ------
GPIO 18 --------------  Pin 1
GND    ----------------  Pin 2

(Repeat for GPIO 19 and GPIO 5)
```

**Logic**: Button press connects GPIO to GND (active LOW with pullup).

### Potentiometer Connection

```
ESP32                   Potentiometer (10kΩ)
-----                   --------------------
3.3V  ----------------  Pin 1 (VCC)
GPIO 34 (ADC) --------  Pin 2 (Wiper)
GND   ----------------  Pin 3 (GND)
```

**ADC Configuration**:
- 11dB attenuation for full 0-3.3V range
- 12-bit resolution (0-4095 raw values)
- Converted to 0-100% in ESPHome

## Bill of Materials (BOM)

| Qty | Component | Specification | Source | Approx. Cost |
|-----|-----------|---------------|--------|--------------|
| 1 | ESP32 DevKitC | USB-C version | AliExpress/Amazon | $8-12 |
| 1 | PN532 NFC Module | I2C interface, with antenna | AliExpress | $5-8 |
| 3 | Tactile buttons | 12mm, through-hole | Local electronics | $1-2 |
| 1 | Potentiometer | 10kΩ linear, PCB mount | Local electronics | $1-2 |
| 1 | Active buzzer | 5V, through-hole | Local electronics | $1 |
| 1 | MOSFET | IRLD120 (N-channel, logic-level) | Local electronics | $0.50 |
| 1 | Schottky diode | 1N5818 | Local electronics | $0.20 |
| 1 | Breadboard/PCB | For prototyping | Local electronics | $3-5 |
| - | Jumper wires | M-M, M-F assortment | Local electronics | $3 |
| 150 | NFC tags | NTAG215, 30mm stickers | Amazon | $15-25 |
| **Total** | | | | **~$40-60** |

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

### 3. Buttons

1. Connect buttons to GPIO 18, 19, and 5
2. Connect other pin of each button to GND
3. Test using ESPHome logs when button is pressed

### 4. Potentiometer

1. Connect outer pins to 3.3V and GND
2. Connect center (wiper) to GPIO 34
3. Test by reading ADC value in ESPHome

### 5. Buzzer Circuit

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
4. **Test**: Trigger buzzer via ESPHome service call

### 6. Final Assembly

1. Secure all components to breadboard or PCB
2. Double-check all connections
3. Upload final ESPHome configuration
4. Test all functions before enclosure

## Photos

*Add your build photos to the `hardware/photos/` directory*

Suggested photos:
- Overall assembly
- Close-up of MOSFET circuit
- PN532 wiring
- Completed build in enclosure
- In use with NFC cards

## Enclosure Design

### Requirements

- Accessible NFC reader area
- Button access
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
   - Drill holes for buttons and potentiometer
   - Cut window for NFC reader

3. **Wooden Box**
   - Aesthetic vintage look
   - Route cable channels
   - Mount components with standoffs

## Design Files

*Future: Add to `hardware/schematics/` directory*

- Fritzing schematic (`.fzz`)
- KiCad PCB design (if creating custom PCB)
- 3D enclosure models (`.stl` files)
- Wiring diagrams (PDF/PNG)

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
- Total: ~300-450mA (peak)

## Safety Notes

- **ESD Protection**: Handle ESP32 with anti-static precautions
- **Polarity**: Double-check all power connections before powering on
- **MOSFET heat**: IRLD120 should not heat up significantly; if hot, check wiring
- **Short circuits**: Inspect for solder bridges or wire shorts before first power-on
- **Testing**: Test each component individually before full integration

## Future Improvements

- [ ] Custom PCB design (eliminate breadboard)
- [ ] Add LED indicators for each button
- [ ] RGB LED strip control for visual feedback
- [ ] Battery operation with charging circuit
- [ ] Add display (OLED) for visual feedback
- [ ] Rotary encoder instead of potentiometer

## Troubleshooting

See `docs/TROUBLESHOOTING.md` for common hardware issues and solutions.

## Resources

- [ESP32 Pinout Reference](https://randomnerdtutorials.com/esp32-pinout-reference-gpios/)
- [PN532 Module Guide](https://www.electrodragon.com/w/PN532_NFC_Module)
- [MOSFET Tutorial](https://learn.sparkfun.com/tutorials/transistors/applications-i-switches)
- [ESP32 ADC Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/adc.html)

---

**Status**: Prototype complete, awaiting custom enclosure design
