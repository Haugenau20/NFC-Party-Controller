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
| Battery Power | 2x 18650 | 1x 18650 |
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
| Gate Resistor | 100Ω | GPIO23 to gate | MOSFET gate protection |
| Flyback Diode | 1N5818 Schottky | Across buzzer | Inductive spike protection |
| Battery | 2x 18650 (3.7V) | - | Portable power |
| Charging Circuit | 18650 charger module | - | Battery management |

### Device 2 Components

| Component | Model/Spec | GPIO Pin | Purpose |
|-----------|------------|----------|---------|
| *(All Device 1 components)* | | | |
| **Pause/Play Button** | Tactile switch | **GPIO18** | Pause/resume playback |
| **Battery** | **1x 18650 (3.7V)** | - | Portable power (smaller capacity) |

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
GPIO 23 ----[100Ω]---+---- Gate
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
- **Gate Resistor**: 100Ω resistor between GPIO23 and MOSFET gate
  - Limits inrush current to gate
  - Provides gate protection
- **Diode**: 1N5818 Schottky diode
  - Forward voltage: 0.45V @ 1A
  - Purpose: Flyback protection for inductive buzzer load
- **Buzzer**: 5V passive buzzer (PWM-driven via LEDC)

**Operation**:
1. GPIO 23 HIGH (3.3V PWM) → Current flows through 100Ω resistor → MOSFET conducts → Buzzer sounds
2. GPIO 23 LOW (0V) → MOSFET off → Buzzer silent
3. Diode protects against voltage spikes when buzzer turns off
4. Gate resistor limits current and protects both GPIO and MOSFET gate

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

| Qty | Component | Specification |
|-----|-----------|---------------|
| 1 | ESP32 DevKitC | USB-C version |
| 1 | PN532 NFC Module | I2C interface, with antenna |
| 1 | Potentiometer | 10kΩ linear, PCB mount |
| 1 | Passive buzzer | 5V, through-hole |
| 1 | MOSFET | 2N7000 (N-channel, logic-level) |
| 1 | Resistor | 100Ω (for MOSFET gate protection) |
| 1 | Schottky diode | 1N5818 |
| 1 | Protoboard | Soldered permanent assembly |
| - | Wire | For soldered connections |

### Device 1 Additional Components

| Qty | Component | Specification |
|-----|-----------|---------------|
| 2 | 18650 Battery | 3.7V lithium-ion |
| 1 | Battery Holder | 2x 18650 |
| 1 | Charging Circuit | 18650 battery charger module |

### Device 2 Additional Components

| Qty | Component | Specification |
|-----|-----------|---------------|
| 1 | Tactile button | 12mm, through-hole |
| 1 | 18650 Battery | 3.7V lithium-ion |
| 1 | Battery Holder | 1x 18650 |
| 1 | Charging Circuit | 18650 battery charger module |

### Shared Components

| Qty | Component | Specification |
|-----|-----------|---------------|
| 150 | NFC tags | NTAG215, 30mm stickers |

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
   - Gate → 100Ω resistor → GPIO 23
   - Source → GND
   - Drain → Buzzer negative lead
2. **Connect buzzer**:
   - Positive lead → 5V (VIN pin on ESP32 or battery output)
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

### 6. Battery and Charging Circuit

1. **Device 1**: Install 2x 18650 batteries in holder
2. **Device 2**: Install 1x 18650 battery in holder
3. Connect charging circuit to battery holder
4. Wire charging circuit output to ESP32 5V/VIN and GND
5. Ensure charging circuit has overcurrent/overvoltage protection
6. Test charging with USB power before final assembly

### 7. Final Assembly

1. Solder all components to protoboard for permanent connections
2. Double-check all solder joints for cold joints or bridges
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

**Power Configuration**:
Both devices use rechargeable 18650 lithium-ion batteries with integrated charging circuits:
- **Device 1**: 2x 18650 batteries in series/parallel (higher capacity)
- **Device 2**: 1x 18650 battery (more compact)
- Charging circuit handles battery management and protection
- USB-C port used for charging and programming

**Power Consumption** (Estimated):
- ESP32 (WiFi active): ~160-260mA
- PN532: ~100-150mA
- Buzzer (when active): ~30-50mA
- **Total: ~300-450mA (peak)**

**Battery Life** (Approximate):
- Device 1 with 2x 3000mAh batteries: ~13-20 hours continuous use
- Device 2 with 1x 3000mAh battery: ~6-10 hours continuous use
- Actual runtime depends on WiFi activity and buzzer usage

---

## Safety Notes

- **ESD Protection**: Handle ESP32 with anti-static precautions
- **Polarity**: Double-check all power connections before powering on
- **MOSFET heat**: 2N7000 should not heat up significantly; if hot, check wiring
- **Short circuits**: Inspect for solder bridges or wire shorts before first power-on
- **Testing**: Test each component individually before full integration

---

## Potential Enhancements

Ideas for further development or customization:

- Custom PCB design (eliminate protoboard soldering)
- LED indicators for visual feedback (battery level, WiFi status)
- RGB LED strip control for integrated party lighting
- OLED display for track/status information
- Rotary encoder instead of potentiometer for improved feel
- Additional buttons for more direct controls
- Accelerometer for gesture-based controls

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
