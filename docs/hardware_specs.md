# Hardware Specifications

## Overview
This document details all hardware components in the distillery automation system.

## Raspberry Pi 4B

**Model:** Raspberry Pi 4 Model B  
**RAM:** 4GB (minimum recommended)  
**OS:** Raspberry Pi OS (64-bit recommended)  
**Storage:** 32GB microSD (minimum)  

**Interfaces Used:**
- GPIO pins for relay/SSR control
- SPI for thermocouple amplifiers
- I2C available for future expansion
- USB for keyboard/mouse during setup
- HDMI for display (if using local GUI)
- Ethernet/WiFi for remote access

## Sensors

### Load Cells
**Quantity:** 4  
**Type:** [To be specified - e.g., 500kg capacity load cells]  
**Amplifier:** [To be specified - e.g., HX711 24-bit ADC]  
**Interface:** GPIO (data + clock pins per cell)  
**Accuracy:** [To be determined after selection]  

**Locations:**
1. Mash Tank (1050L capacity monitoring)
2. Still (200L capacity monitoring)
3. Discharge Tank (1050L capacity monitoring)
4. Distillate Collection (0-25L precision monitoring)

**Specifications to Consider:**
- Overload protection
- Temperature compensation
- Weatherproof/washdown rating if needed
- Mounting hardware compatibility

### Thermocouples
**Quantity:** 3+ (expandable)  
**Type:** [To be specified - typically Type K]  
**Amplifier:** [To be specified - e.g., MAX31855]  
**Interface:** SPI  
**Range:** -200°C to +1350°C (Type K typical)  
**Accuracy:** ±2°C (typical for MAX31855)  

**Locations:**
1. Still Mash (primary temperature control)
2. Condenser (cooling verification)
3. Ambient (reference)
4. [Future: Vapor temperature, etc.]

**Specifications to Consider:**
- Probe length and thread size
- Probe material (stainless steel for food contact)
- Response time
- Cold junction compensation (built into amplifier)

## Actuators

### Heating Elements
**Quantity:** 2  
**Power:** 5.5kW each (11kW total)  
**Voltage:** [To be specified - likely 240V]  
**Control Method:** Solid State Relay (SSR) with PWM  

**SSR Specifications Needed:**
- Current rating: Minimum 30A per element (5500W / 240V ≈ 23A)
- Heat sink requirements
- Zero-crossing control for reduced EMI
- Opto-isolated input (compatible with Pi 3.3V logic)

**Safety Considerations:**
- Thermal fuse or cutoff
- Dry-run protection (heating only when liquid present)
- Gradual power ramping
- Emergency cutoff circuit

### Pumps
**Quantity:** 4  
**Type:** [To be specified - likely centrifugal, food-grade]  
**Control:** On/Off via relay  

1. **Mash Transfer Pump**
   - Flow rate: 10-20 L/min suggested
   - Ability to handle particulate matter
   - Self-priming helpful

2. **Condenser Cooling Pump**
   - Flow rate: Based on condenser requirements
   - Continuous duty rated

3. **Discharge Pump**
   - Flow rate: Similar to mash transfer
   - Handles thick/particulate matter

4. **CIP (Clean-In-Place) Pump**
   - Flow rate: Adequate for cleaning spray
   - Chemical compatible

**Relay Requirements:**
- Voltage rating matching pumps
- Current rating with safety margin
- Normally-open contacts
- Flyback diode protection for inductive loads

### Valves
**Quantity:** 6  
**Type:** [To be specified - likely solenoid or motorized ball valves]  
**Voltage:** [To be specified - 12V/24V DC or 120V/240V AC]  
**Control:** On/Off via relay  

**Locations:**
1. Mash Inlet (to still)
2. Heads Collection
3. Hearts Collection
4. Tails Collection
5. Discharge
6. CIP Water

**Specifications to Consider:**
- Port size (matching pipe diameter)
- Material (food-grade, alcohol compatible)
- Normally-closed vs normally-open
- Manual override capability
- Response time

## Power Distribution

### Power Requirements Summary
- Heating Elements: 11kW (240V)
- Pumps: [TBD based on selection]
- Valves: [TBD based on selection]
- Raspberry Pi: 5V @ 3A (15W)
- Relays/SSRs: Minimal

**Recommended Setup:**
- Dedicated 240V circuit for heating elements
- Separate 120V/240V circuits for pumps
- 24V/12V DC power supply for valves (if applicable)
- Isolated 5V power supply for Raspberry Pi
- Emergency stop button (hardware interrupt)

## Interface Boards

### Relay Board
**Recommended:** 8-channel relay module  
**Voltage:** 5V logic, contacts rated for load  
**Isolation:** Opto-isolated inputs  
**Features:** LED indicators, screw terminals  

**Channels Needed:**
- 4 pumps
- 6 valves
- Total: 10 channels (may need two 8-channel boards)

### SSR Mounting
- Individual SSRs on heat sinks
- Or integrated SSR module
- Adequate ventilation
- Thermal monitoring

## Wiring Specifications

### Control Wiring (Low Voltage)
- GPIO to relays/SSRs: 22 AWG stranded
- SPI/I2C: Shielded twisted pair if >1m
- Thermocouple extension wire: Match thermocouple type

### Power Wiring (High Voltage)
- Heating elements: Per electrical code (likely 10 AWG or larger)
- Pumps: Per manufacturer spec
- Proper conduit and junction boxes
- Ground fault protection

## Environmental Considerations

**Operating Environment:**
- Temperature: 10-40°C
- Humidity: 20-80% (non-condensing)
- Ventilation required for heat dissipation
- Alcohol vapor considerations (explosion-proof not required for this setup, but good ventilation essential)

**Enclosure Recommendations:**
- NEMA 4 or IP65 for control panel
- Separate high-voltage and low-voltage sections
- Access panels for maintenance
- Cable glands for wire entry

## Shopping List Template

### To Be Determined:
- [ ] Load cells (4x) + amplifiers
- [ ] Thermocouples (3x) + amplifiers  
- [ ] Solid state relays (2x, 30A+)
- [ ] Heat sinks for SSRs
- [ ] Relay modules (2x 8-channel)
- [ ] Pumps (4x - specify models)
- [ ] Valves (6x - specify models)
- [ ] Power supplies (5V for Pi, others as needed)
- [ ] Enclosure/panel
- [ ] Wire, terminals, connectors
- [ ] Emergency stop button
- [ ] Indicator lights (optional)
- [ ] Touchscreen display (if local GUI)

## Notes
This document will be updated as hardware is selected and installed. Always verify specifications with manufacturer datasheets before ordering or installation.
