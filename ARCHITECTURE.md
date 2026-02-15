# System Architecture

## Overview
The distillery automation system is built using a modular architecture with clear separation between hardware interfaces, control logic, process sequences, and user interface.

## System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface (GUI)                      │
│                    Recipe Selection & Monitoring                 │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                     Sequence Controller                          │
│   Fill → Heat → Distill (Heads/Hearts/Tails) → Discharge → CIP │
└───────────────────────────────┬─────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
┌───────▼────────┐    ┌────────▼─────────┐   ┌────────▼──────────┐
│   Controllers  │    │  Safety Monitor  │   │  Data Recorder    │
│                │    │                  │   │                   │
│ - PID Heating  │    │ - Temp limits    │   │ - Log all data    │
│ - Flow Control │    │ - Weight limits  │   │ - Event tracking  │
│                │    │ - E-stop         │   │                   │
└───────┬────────┘    └────────┬─────────┘   └───────────────────┘
        │                      │
┌───────▼──────────────────────▼─────────────────────────────────┐
│                    Hardware Interface Layer                      │
│                                                                  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐          │
│  │ Sensors │  │ Pumps   │  │ Valves  │  │ Heating  │          │
│  │         │  │         │  │         │  │ Elements │          │
│  │ Load    │  │ Mash    │  │ Mash    │  │          │          │
│  │ Cells   │  │ Cooling │  │ Heads   │  │ 2x 5.5kW │          │
│  │         │  │ Disch.  │  │ Hearts  │  │          │          │
│  │ Thermo- │  │ CIP     │  │ Tails   │  │ SSR PWM  │          │
│  │ couples │  │         │  │ Disch.  │  │ Control  │          │
│  │         │  │         │  │ CIP     │  │          │          │
│  └─────────┘  └─────────┘  └─────────┘  └──────────┘          │
└──────────────────────────────────────────────────────────────────┘
```

## Component Descriptions

### 1. Hardware Interface Layer (`src/hardware/`)
Low-level drivers for all physical components. Each module is independent and testable.

**Load Cells** (`load_cell.py`)
- Interface with HX711 or similar ADC
- Tare, calibrate, and read weight
- 4 instances: mash tank, still, discharge tank, distillate collection

**Thermocouples** (`thermocouple.py`)
- Interface with MAX31855 or similar
- Temperature reading with error detection
- Multiple instances throughout system

**Relays/SSRs** (`relay.py`)
- GPIO control for pumps and valves
- PWM support for SSR heating control
- Safety interlocks

**Pumps** (`pump.py`)
- On/off control
- Runtime tracking
- Safety timeouts

**Valves** (`valve.py`)
- On/off control
- State tracking
- Interlock logic

### 2. Controllers (`src/controllers/`)
Closed-loop control algorithms.

**PID Controller** (`pid_controller.py`)
- Generic PID implementation
- Tunable parameters (Kp, Ki, Kd)
- Anti-windup protection
- Used for heating and flow control

**Heating Controller** (`heating_controller.py`)
- Manages 2x heating elements
- Temperature setpoint control
- Power modulation via PWM to SSRs

**Flow Controller** (`flow_controller.py`)
- Controls distillate flow rate by adjusting heat
- Monitors weight change over time
- Critical for quality separation

### 3. Process Sequences (`src/sequences/`)
High-level automation sequences for each process stage.

**Fill Sequence** (`fill_sequence.py`)
- Open mash valve
- Start mash pump
- Monitor still weight
- Stop at setpoint
- Close valve

**Distillation Sequence** (`distillation_sequence.py`)
- Heat to temperature setpoint
- Start condenser cooling
- Monitor distillate flow
- Sequential collection: heads → hearts → tails
- Weight-based transitions

**Discharge Sequence** (`discharge_sequence.py`)
- Open discharge valve
- Start discharge pump
- Monitor still weight
- Detect completion (stable low weight)

**CIP Sequence** (`cip_sequence.py`)
- Timed water flush
- Discharge to waste
- Prepare for next cycle

### 4. Safety Monitor (`src/safety/`)
Continuous monitoring and emergency responses.

**Safety Interlocks:**
- Maximum temperature limits
- Minimum/maximum weight limits
- Flow rate verification
- Heating element protection
- Emergency stop functionality

### 5. User Interface (`src/gui/`)
Operator control and monitoring.

**Features:**
- Recipe selection
- Process monitoring (temperatures, weights, flow rates)
- Manual overrides
- Data visualization
- Alarm notifications

### 6. Utilities (`src/utils/`)
Supporting functions.

**Logger** (`logger.py`)
- Timestamped event logging
- Error tracking

**Data Recorder** (`data_recorder.py`)
- CSV/JSON data export
- Runtime statistics
- Historical analysis

**Calibration Tools** (`calibration_tools.py`)
- Sensor calibration routines
- Verification procedures

## Process State Machine

```
┌─────────┐
│  IDLE   │
└────┬────┘
     │ User presses "RUN"
     ▼
┌─────────┐
│  FILL   │──── Monitor still weight
└────┬────┘
     │ Weight setpoint reached
     ▼
┌─────────┐
│  HEAT   │──── PID control to temperature
└────┬────┘
     │ Temperature setpoint reached
     ▼
┌──────────┐
│ DISTILL  │──── Flow control, sequential collection
│          │     HEADS → HEARTS → TAILS
└────┬─────┘
     │ Tails weight reached
     ▼
┌──────────┐
│DISCHARGE │──── Empty still to waste
└────┬─────┘
     │ Still empty
     ▼
┌─────────┐
│   CIP   │──── Clean-in-place
└────┬────┘
     │ Timer complete
     ▼
┌─────────┐
│  IDLE   │──── Ready for next cycle
└─────────┘
```

## Data Flow

1. **Sensors** → Hardware layer reads raw data
2. **Hardware layer** → Controllers receive processed data
3. **Controllers** → Calculate outputs (heating power, valve states)
4. **Sequence controller** → Orchestrates process stages
5. **Safety monitor** → Validates all actions, can override
6. **GUI** → Displays status, accepts user input
7. **Data recorder** → Logs everything for analysis

## Configuration Management

All operational parameters stored in YAML files:
- Hardware pin assignments
- Calibration coefficients
- PID tuning parameters
- Recipe definitions (setpoints, timings, weights)

This allows:
- Easy parameter tuning without code changes
- Multiple recipe storage
- Version control of settings

## Future Enhancements (Planned)

- [ ] Remote monitoring via web interface
- [ ] Automated recipe optimization
- [ ] Predictive maintenance alerts
- [ ] Multi-still support
- [ ] Cloud data backup
- [ ] Mobile app integration

## Testing Strategy

Each component tested independently:
1. Unit tests for each hardware module
2. Controller tests with simulated inputs
3. Sequence tests with mock hardware
4. Integration tests with actual hardware
5. Full system validation runs

## Error Handling

Hierarchical error response:
1. **Component level**: Retry, fallback to safe state
2. **Sequence level**: Pause, alert operator, allow intervention
3. **System level**: Emergency stop, safe shutdown

All errors logged with timestamp and context.
