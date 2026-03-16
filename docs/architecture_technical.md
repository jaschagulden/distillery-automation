# Technical Architecture Reference
### Distillery Automation System — Implementation Detail

*This is the companion to `docs/architecture_for_jascha.md`, which has the plain-language overview and the suggested workflow for working through these proposals with Claude Code. Read that document first.*

*Section numbers here correspond to the "for implementation detail, see §N" references in the high-level document. When working with Claude Code, you can ask it to "implement Suggestion 3" or "show me the detail for §5" and it will find the right section.*

---

## Table of Contents

1. [Guiding Principles](#1-guiding-principles)
2. [System Boundaries](#2-system-boundaries)
3. [Hardware Abstraction Layer](#3-hardware-abstraction-layer) ← *Suggestion 1*
4. [Simulator](#4-simulator) ← *Suggestion 2*
5. [Safety Monitor](#5-safety-monitor) ← *Suggestion 3*
6. [Control Layer](#6-control-layer)
7. [Recipe System (S88-inspired)](#7-recipe-system-s88-inspired) ← *Suggestion 4*
8. [Message Bus (MQTT)](#8-message-bus-mqtt) ← *Suggestion 5*
9. [Data Layer](#9-data-layer)
10. [Build Order and Parallel Workstreams](#10-build-order-and-parallel-workstreams)
11. [What We Are Not Building Yet](#11-what-we-are-not-building-yet)
12. [Known Issues to Fix](#12-known-issues-to-fix) ← *Suggestion 6 (pin conflicts)*

---

## 1. Guiding Principles

*These are Tim's proposed principles — the reasoning behind the suggestions. Review and adjust as you see fit.*

**Define interfaces top-down; implement bottom-up.**
All control logic, safety systems, and sequences would be written against abstract interfaces. Concrete hardware drivers are written independently. The system is assembled by injection.

**Safety is not a module — it is a constraint.**
The proposed safety monitor runs independently of the control process. It cannot be disabled by a control logic bug or crash. Tim's recommendation is that it be built before any automated sequences run on real hardware.

**The simulator is a first-class citizen.**
Every hardware interface would have a simulated implementation. The full control system could then run end-to-end on a laptop with no Pi hardware — enabling development, testing, and iteration without physical access to the distillery.

**Configuration over code for process parameters.**
Setpoints, limits, sequence transitions, and recipe parameters live in YAML files. The code reads them; it does not contain them. A new recipe is a new YAML file, not a code change.

**The control system is not the whole system.**
The Pi controls the still. It is not responsible for inventory management, batch record keeping, or business logic. Those belong to a separate layer with a well-defined interface to the control system.

---

## 2. System Boundaries

The full "farming to packaging" scope spans multiple systems with different requirements:

```
┌──────────────────────────────────────────────────────────────────┐
│  BUSINESS / MES LAYER  (web app + database, not on Pi)           │
│  Batch records, inventory, quality, recipes, regulatory          │
└───────────────────────────┬──────────────────────────────────────┘
                            │  batch_complete event (JSON)
┌───────────────────────────▼──────────────────────────────────────┐
│  CONTROL SYSTEM  (Pi 1)                                          │
│  Real-time hardware control, safety, sequences, data logging     │
└───────────────────────────┬──────────────────────────────────────┘
                            │  MQTT topics
┌───────────────────────────▼──────────────────────────────────────┐
│  EXPERIENCE LAYER  (Pi 2, Pi 3)                                  │
│  Displays, voice AI kiosk — read-only subscribers to MQTT        │
└──────────────────────────────────────────────────────────────────┘
```

**This repository is the control system only.** The experience layer (voice AI, displays) should be a separate repository that consumes the MQTT API. The MES layer is a future concern.

---

## 3. Hardware Abstraction Layer

### Location: `src/hardware/interfaces.py`

All hardware interfaces are defined as Python Abstract Base Classes. No code outside `src/hardware/` ever imports a concrete driver class.

```python
from abc import ABC, abstractmethod

class TemperatureSensor(ABC):
    """Any device that measures temperature."""
    @abstractmethod
    def read_celsius(self) -> float: ...
    @abstractmethod
    def is_fault(self) -> bool: ...

class WeightSensor(ABC):
    """Any device that measures weight."""
    @abstractmethod
    def read_kg(self) -> float: ...
    @abstractmethod
    def tare(self) -> None: ...
    @abstractmethod
    def is_fault(self) -> bool: ...

class Switch(ABC):
    """Any binary actuator: pump, valve, relay."""
    @abstractmethod
    def on(self) -> None: ...
    @abstractmethod
    def off(self) -> None: ...
    @abstractmethod
    def is_on(self) -> bool: ...
    def set(self, state: bool) -> None:
        self.on() if state else self.off()

class PWMOutput(ABC):
    """Any continuously variable output: SSR for heating elements."""
    @abstractmethod
    def set_duty_cycle(self, percent: float) -> None: ...
    @abstractmethod
    def get_duty_cycle(self) -> float: ...
    @abstractmethod
    def off(self) -> None: ...
```

### Concrete driver location: `src/hardware/drivers/`

```
src/hardware/
├── interfaces.py          ← ABCs only, no hardware dependencies
├── drivers/
│   ├── sequent_thermocouple.py   ← SequentThermocouple(TemperatureSensor)
│   ├── hx711_load_cell.py        ← HX711LoadCell(WeightSensor)
│   ├── sequent_mosfet.py         ← SequentMosfetSwitch(Switch)
│   └── ssr_pwm.py                ← SSRHeatingElement(PWMOutput)
└── simulator/
    ├── simulated_thermocouple.py
    ├── simulated_load_cell.py
    ├── simulated_switch.py
    └── simulated_pwm.py
```

### Dependency injection pattern

Controllers receive interface types, never concrete types:

```python
# CORRECT — control logic depends only on the interface
class HeatingController:
    def __init__(self, sensor: TemperatureSensor, output: PWMOutput):
        self.sensor = sensor
        self.output = output

# In main.py (Pi) — inject real hardware
controller = HeatingController(
    sensor=SequentThermocouple(stack=0, channel=1),
    output=SSRHeatingElement(pin=12)
)

# In tests — inject simulator
controller = HeatingController(
    sensor=SimulatedThermocouple(profile=[20, 30, 50, 70, 76, 78]),
    output=SimulatedPWM()
)
```

---

## 4. Simulator

### Location: `src/hardware/simulator/`

The simulator provides plausible physics for testing control logic without hardware. It does not need to be accurate — it needs to be *testable*.

**Minimum viable still model:**
- Temperature rises proportionally to PWM duty cycle input
- Above 78°C (ethanol boiling point) distillate flows at a rate proportional to temperature overshoot
- Weight in collection vessel increases as distillate flows
- Cooling water flow reduces condenser temperature

The simulator is what makes it possible for Tgulden to develop and test control sequences from a MacBook. It also enables fast iteration: running a simulated 3-hour distillation in seconds.

**Fault injection for safety testing:**
```python
sensor = SimulatedThermocouple(
    profile=[20, 50, 80, 90, 95, 100, 106],  # will exceed limit
    fault_at_index=10                          # simulate sensor failure
)
```

---

## 5. Safety Monitor

### Location: `src/safety/safety_monitor.py`

**The safety monitor is built before any automated sequences run on real hardware. This is non-negotiable.**

Architectural requirements:
- Runs in its own thread (or process), not called by the control loop
- Reads sensors directly and independently — does not consume data from the control system
- Can cut power to all actuators regardless of control system state
- Never disabled by a control logic exception or deadlock
- Logs every action with timestamp and triggering condition

```
Thread: Control Loop       Thread: Safety Monitor
─────────────────────      ──────────────────────────
read sensors               read sensors (independently)
run PID                    check all limits
command actuators          if any limit exceeded:
                             → emergency_stop()
                             → log(condition, timestamp)
                             → alert operator
                           check watchdog heartbeat
                             if no heartbeat in N sec:
                               → emergency_stop()
```

**Safety limits** (from `config/hardware_config.yaml`):
- Max still temp: 105°C / Emergency shutdown: 110°C
- Max still weight: 220kg
- Max pump runtime: 30 minutes
- Max heating time: 180 minutes
- Watchdog timeout: 10 seconds

**Hardware note:** Software safety is a complement to, not a replacement for, a hardware interlock (physical relay that cuts mains power independently of the Pi). The hardware interlock should be implemented on the physical build.

---

## 6. Control Layer

### Location: `src/controllers/`

**PID Controller** (`pid_controller.py`)
Generic implementation, no hardware dependencies. Pure math. Tested against simulator.
Consider using the `simple-pid` library (already in requirements.txt) rather than writing from scratch.

**Heating Controller** (`heating_controller.py`)
Wraps PID + PWMOutput + TemperatureSensor. Manages the two 5.5kW heating elements. Exposes `set_target(celsius)` and `update()`.

**Flow Controller** (`flow_controller.py`)
Monitors distillate weight over time to compute flow rate. Adjusts heat to maintain target flow. Critical for quality separation.

All controllers accept hardware interfaces via injection. All are testable against simulator.

---

## 7. Recipe System (S88-inspired)

### Location: `config/recipes/`

A recipe defines a complete distillation run as a sequence of phases. Control logic reads recipes; it does not contain process parameters.

```yaml
# config/recipes/standard_grain.yaml
name: Standard Grain Spirit
description: 200L grain mash, standard cuts

phases:
  fill:
    target_weight_kg: 180
    max_duration_min: 20
    abort_if_weight_above_kg: 200

  heat:
    target_temp_c: 78.5
    heat_ramp_pct_per_min: 10
    max_duration_min: 180
    abort_if_temp_above_c: 105

  heads:
    collection_weight_kg: 2.0
    target_flow_ml_per_min: 60

  hearts:
    collection_weight_kg: 8.0
    target_flow_ml_per_min: 40

  tails:
    collection_weight_kg: 4.0
    target_flow_ml_per_min: 60

  discharge:
    target_weight_kg: 5   # still considered empty below this
    max_duration_min: 30

  cip:
    duration_min: 15
```

The sequence engine (`src/sequences/sequence_engine.py`) reads any recipe and executes it. A new recipe is a new YAML file.

---

## 8. Message Bus (MQTT)

### Why MQTT

You already have a three-Pi network. MQTT (via Mosquitto, runs on Pi 1) is the right backbone:
- Decouples subsystems — control system, displays, voice AI, logging
- Zero-config for new subscribers (add a display without touching control code)
- Standard in industrial IoT

### Topic schema

```
distillery/sensors/still_temp_c         # float
distillery/sensors/condenser_temp_c     # float
distillery/sensors/still_weight_kg      # float
distillery/sensors/distillate_weight_kg # float
distillery/control/phase                # string: fill|heat|heads|hearts|tails|discharge|cip|idle
distillery/control/recipe               # string: current recipe name
distillery/safety/status                # string: ok|alarm|emergency_stop
distillery/safety/alarm                 # string: alarm message when triggered
distillery/batch/complete               # JSON: full batch summary on run completion
```

### Migration path

`sensor_server.py` (the existing Flask server) becomes an MQTT publisher. The Flask endpoints can remain for backward compatibility but the primary data path is MQTT.

Pi 3 voice AI subscribes to `distillery/sensors/#` and `distillery/control/#` — no changes to control system code required.

---

## 9. Data Layer

### What runs on Pi 1

- **SQLite** (via Python's stdlib) for sensor time-series during a run
- Write a row per second: timestamp, all sensor values, current phase, actuator states
- On batch complete, export a JSON/CSV summary

### What does NOT run on Pi 1

- Long-term historical storage
- Recipe management UI
- Batch record keeping
- Inventory tracking

These belong to a separate system (future work). The interface is the `distillery/batch/complete` MQTT topic — Pi 1 publishes a batch summary; an external system subscribes and stores it.

---

## 10. Build Order and Parallel Workstreams

### Sequential (must be in order)

1. `src/hardware/interfaces.py` — all ABCs
2. `src/hardware/simulator/` — fake implementations
3. `src/safety/safety_monitor.py` — before any real sequences
4. `src/controllers/pid_controller.py`
5. `src/controllers/heating_controller.py`
6. Recipe YAML schema + `src/sequences/sequence_engine.py`
7. Full end-to-end test against simulator

### Parallel (after interfaces are defined)

| Tgulden | Jascha |
|---|---|
| Simulator | Real hardware drivers |
| Safety monitor | Pin assignment audit + hardware_config.yaml fix |
| PID + controllers | Hardware test scripts for each driver |
| Sequence engine | Integration testing drivers against interfaces |

### After integration

8. MQTT publisher in sensor_server.py
9. GUI (can be a simple web dashboard initially)
10. Voice AI integration (subscribes to MQTT — minimal changes to Pi 3 code)

---

## 11. What We Are Not Building Yet

- Web UI / remote dashboard
- Mobile app
- Multi-still support
- MES / batch record system
- Cloud backup
- Advanced recipe optimization

These are valid future features. The architecture described here is designed to accommodate them without structural changes. Resist the temptation to build them now.

---

## 12. Known Issues to Fix Before Writing Control Code

### Pin conflicts in `config/hardware_config.yaml`

The following GPIO pins are currently assigned to multiple devices:

| Pin | Assigned to (1) | Assigned to (2) |
|-----|----------------|----------------|
| 12  | heating/element_1 | valves/cip |
| 16  | heating/element_2 | pumps/discharge |
| 25  | thermocouples/ambient (cs_pin) | valves/heads |
| 8   | thermocouples/still_mash (cs_pin) | valves/hearts |
| 7   | thermocouples/condenser (cs_pin) | valves/tails |

**This must be resolved with Jascha before any control code is written.** The correct pin assignments should come from the actual wiring on Pi 1, not the config file. The config file should be updated to match reality.

### SESSION_*.md file size

Session notes are full AI chat transcripts (SESSION_6 is 365KB). These should be replaced with concise summaries. The transcript content is not useful for code context and inflates the repo significantly.

### No branch protection on `main`

Set up branch protection on GitHub: require PRs to merge to main, disable direct push. This prevents a bad push from reaching the Pi's deployed code.

### `src/` is scaffolding only

`src/main.py` is a skeleton. `src/controllers/`, `src/safety/`, `src/sequences/`, `src/gui/` contain only empty `__init__.py` files. The working code (`sensor_server.py`, `weigh.py`, etc.) lives at the repo root. The migration path: implement proper modules in `src/`, then update the Pi's startup scripts to point to `src/main.py`.

---

*From Tim, March 2026. These are proposals — nothing is implemented or decided until Jascha reviews and agrees.*
