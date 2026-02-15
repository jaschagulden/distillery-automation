# Calibration Procedures

## Overview
Proper calibration ensures accurate measurements and safe, consistent operation. This document provides step-by-step procedures for calibrating all sensors.

## Safety First
- Perform calibrations when system is cool and depressurized
- Disconnect power to heating elements during calibration
- Use appropriate personal protective equipment
- Have a second person present for safety

---

## Load Cell Calibration

### Required Equipment
- Calibrated weights (suggest 50kg, 100kg, 200kg)
- Digital multimeter (for troubleshooting)
- Notebook for recording values

### Procedure

#### 1. Pre-Calibration Checks
- Verify load cell is mounted securely
- Check all wiring connections
- Ensure vessel is completely empty and clean
- Ambient temperature should be stable

#### 2. Tare Calibration
```python
# Run the calibration script
python src/utils/calibration_tools.py --device load_cell --name still --step tare

# Or manually:
# 1. Ensure vessel is empty
# 2. Record raw reading (this becomes tare_value)
# 3. Update config/calibration/load_cells.yaml
```

**Steps:**
1. Empty the vessel completely
2. Run tare command
3. Allow reading to stabilize (30 seconds)
4. Record the tare value
5. Repeat 3 times and average

#### 3. Calibration Factor Determination
```python
# Run calibration with known weight
python src/utils/calibration_tools.py --device load_cell --name still --step calibrate --weight 100

# System will:
# 1. Prompt you to add known weight
# 2. Calculate calibration factor
# 3. Update configuration file
```

**Steps:**
1. Place known weight on scale (e.g., 100kg)
2. Allow reading to stabilize (30 seconds)
3. Run calibration command with actual weight
4. System calculates: `calibration_factor = (raw_reading - tare_value) / known_weight_kg`
5. Verify by testing with different known weights

#### 4. Verification
Test with at least 3 different known weights across the expected range:
- Low range: 20% of capacity
- Mid range: 50% of capacity  
- High range: 80% of capacity

**Acceptable tolerance:** ±0.5% of reading

#### 5. Documentation
Update `config/calibration/load_cells.yaml`:
```yaml
still:
  calibration_factor: [calculated value]
  tare_value: [recorded value]
  last_calibrated: "2025-02-11"
  calibration_weight_kg: 100
  notes: "Calibrated with certified weights, verified at 20kg, 100kg, 180kg"
```

### Troubleshooting
- **Unstable readings:** Check for vibration, air currents, temperature changes
- **Non-linear response:** May indicate damaged load cell
- **Zero drift:** Re-tare more frequently or check for mechanical binding

---

## Thermocouple Calibration

### Required Equipment
- Ice water bath (0°C reference)
- Boiling water (100°C reference, adjust for altitude)
- Calibrated reference thermometer
- Insulated container

### Procedure

#### 1. Ice Point Verification (0°C)
**Setup:**
1. Fill container with crushed ice
2. Add small amount of distilled water
3. Stir to achieve uniform 0°C
4. Insert thermocouple and reference thermometer
5. Wait 2-3 minutes for stabilization

**Measurement:**
```python
python src/utils/calibration_tools.py --device thermocouple --name still_mash --step ice_point

# Record the reading
# True value should be 0°C (32°F)
# Calculate offset if needed
```

#### 2. Boiling Point Verification (100°C at sea level)
**Setup:**
1. Boil distilled water
2. Ensure vigorous boiling
3. Insert thermocouple in steam/water (not touching container)
4. Wait 1-2 minutes for stabilization

**Adjustment for altitude:**
- Sea level: 100°C
- 500m: 98.3°C
- 1000m: 96.7°C
- 1500m: 95.0°C

**Measurement:**
```python
python src/utils/calibration_tools.py --device thermocouple --name still_mash --step boiling_point --altitude_m 0

# Record reading
# Calculate offset from expected value
```

#### 3. Calculate Offset
```
offset = (measured_value - true_value)
```

If offset is consistent across both points, apply it in configuration:
```yaml
still_mash:
  offset_c: -1.5  # Example: sensor reads 1.5°C high
  last_verified: "2025-02-11"
  verification_temp_c: "0, 100"
  notes: "Verified at ice and boiling points"
```

#### 4. Verification
- Offsets should be small (< 2°C for quality amplifiers)
- If offset > 5°C, check connections or replace sensor
- MAX31855 and similar amplifiers have internal cold junction compensation

### Troubleshooting
- **Erratic readings:** Check for loose connections, damaged wire
- **Open circuit error:** Broken thermocouple, check continuity
- **Large offset:** May indicate wrong thermocouple type setting

---

## PID Controller Tuning

While not a "calibration" in the traditional sense, PID tuning is critical for performance.

### Heating Control PID
**Goal:** Reach and maintain target temperature without overshoot

#### Ziegler-Nichols Method (Starting Point)
1. Set Ki = 0, Kd = 0
2. Increase Kp until oscillation occurs (Ku)
3. Measure oscillation period (Tu)
4. Calculate:
   - Kp = 0.6 * Ku
   - Ki = 1.2 * Ku / Tu
   - Kd = 0.075 * Ku * Tu

#### Manual Tuning (Recommended)
```python
# Test PID parameters
python tests/test_pid.py --kp 50 --ki 0.1 --kd 10 --setpoint 78 --duration 600

# Monitor performance:
# - Rise time (how fast it reaches setpoint)
# - Overshoot (should be < 2°C)
# - Settling time (how long to stabilize)
# - Steady-state error (should be < 0.5°C)
```

**Tuning Guidelines:**
- **Too much overshoot:** Reduce Kp, increase Kd
- **Too slow:** Increase Kp, reduce Kd
- **Oscillation:** Reduce Kp and Ki
- **Steady-state error:** Increase Ki

### Flow Rate PID
**Goal:** Maintain consistent distillate flow rate

This is more challenging as it's an indirect control (adjusting heat to control flow).

**Start conservatively:**
- Kp = 2.0
- Ki = 0.05
- Kd = 0.5

**Tune during actual distillation runs:**
1. Monitor flow rate stability
2. Adjust gains based on response
3. Document final values in recipe

---

## Calibration Schedule

### Required Frequency
- **Load cells:** Monthly, or after any mechanical work
- **Thermocouples:** Quarterly, or if readings seem suspect
- **PID tuning:** After any hardware changes, seasonally due to ambient conditions

### Record Keeping
Maintain a calibration log:
```
Date: 2025-02-11
Device: Still Load Cell
Technician: [Name]
Calibration Weight: 100kg
Result: Pass (within 0.3% tolerance)
Next Due: 2025-03-11
```

---

## Automated Calibration Tools

The system includes helper scripts:

```bash
# Interactive calibration wizard
python src/utils/calibration_tools.py --wizard

# Individual device calibration
python src/utils/calibration_tools.py --device [load_cell|thermocouple] --name [device_name]

# Verification only (no changes)
python src/utils/calibration_tools.py --verify-all
```

These tools will:
- Guide you through the process
- Automatically update configuration files
- Generate calibration reports
- Alert if devices are out of tolerance

---

## Notes
- Always calibrate in the actual installation environment when possible
- Temperature affects all sensors - control ambient conditions
- Keep calibration records for traceability
- Some jurisdictions may require certified calibrations for commercial use
