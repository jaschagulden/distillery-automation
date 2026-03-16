# Palmeri Distillery — Claude Code Context

## What This Project Is

Raspberry Pi-based automation system for a small-scale distillery. Three-Pi network:
- **Pi 1** (`distillery-pi`, 192.168.0.31): Main controller — sensors, MOSFET HAT, thermocouple HAT
- **Pi 2**: Portrait display kiosks (slideshow)
- **Pi 3** (`palmeri-ai`, 192.168.0.33): RPi 5 + Hailo-8L AI HAT — voice AI avatar kiosk

**This repo is Pi 1 control system only.** Pi 3 code lives in `~/palmeri-ai/` on Pi 3.

---

## Hardware on Pi 1

- **Sequent 8-MOSFET HAT** (Stack 0, `lib8mosind`): pumps, valves, heaters
- **Sequent 8-Thermocouple HAT** (Stack 0, `sm_tc`): K-type on channels 1 & 2
- **HX711 load cell amp**: GPIO 5 (data), GPIO 6 (clock)
- **2x 5.5kW heating elements** via SSR (PWM control)
- All libraries installed system-wide (no venv)

---

## Project Status (March 2026, ~70% complete)

### Working code (root level, runs on Pi 1)
- `sensor_server.py` — Flask server, `/sensors` and `/status` on port 5000
- `weigh.py`, `calibrate_hx711.py`, `test_hx711.py` — load cell utilities
- `src/hardware/mosfet_hat.py` — MOSFET HAT test script
- `src/hardware/thermocouple_hat.py` — thermocouple HAT test script

### Not yet implemented (stubs only)
- `src/main.py` — skeleton
- `src/controllers/`, `src/safety/`, `src/sequences/`, `src/gui/` — empty `__init__.py` only
- `tests/hardware_test_suite.py` — all test functions are stubs

---

## Architecture Direction

We are implementing an interface-first architecture. Read these before writing new code:
- `docs/architecture_for_jascha.md` — high-level rationale (start here)
- `docs/architecture_technical.md` — technical reference

**Core pattern:** All hardware is accessed through ABCs defined in `src/hardware/interfaces.py` (not yet written). Every hardware type has both a real driver and a simulator implementation. Control logic is written against interfaces only, never concrete drivers.

**Build order:**
1. `src/hardware/interfaces.py` (ABCs)
2. `src/hardware/simulator/` (fake hardware)
3. `src/safety/safety_monitor.py` ← **before any sequences run on real hardware**
4. Controllers, then sequences

---

## Safety Rules

**DO NOT:**
- Write code that directly controls heating elements without safety interlock checks
- Push to `main` without a PR review
- Test sequences on Pi 1 without verifying the safety monitor is running
- Leave heating elements enabled in any test script

**The safety system must be implemented before automated sequences run on real hardware.**
Current safety status: NOT IMPLEMENTED. Manual monitoring required.

---

## Known Issues (fix before writing control code)

**Pin conflicts in `config/hardware_config.yaml`** — several GPIO pins assigned to multiple devices:
- Pin 12: heating element_1 AND cip valve
- Pin 16: heating element_2 AND discharge pump
- Pins 7, 8, 25: also duplicated

Correct assignments must come from actual Pi 1 wiring. Do not write drivers until this is resolved with Jascha.

---

## Collaboration

- **Jascha** (owner): hardware expert, writes hardware drivers (`src/hardware/drivers/`), resolves pin assignments
- **Tgulden** (collaborator): writes interfaces, simulator, safety monitor, controllers, sequences

Branch strategy:
- `main` — deployed to Pi 1, protected (PRs required)
- `dev` — integration branch
- `feature/*` or `jascha/*` — feature branches

---

## Running / Testing

**Cannot run `src/` modules locally** — hardware libraries (`lib8mosind`, `sm_tc`, `hx711`) require Pi hardware.

Once simulator is built: all control logic should be runnable locally via:
```bash
python -m pytest tests/
python src/main.py --simulate
```

**To access Pi 1:**
```bash
ssh pi@distillery-pi.local
# or
ssh pi@192.168.0.31
```

---

## Docs & Session Notes

- `docs/architecture_for_jascha.md` — architecture overview in plain language
- `docs/architecture_technical.md` — technical architecture reference
- `docs/hardware_specs.md` — hardware details
- `docs/operational_manual.md` — operating instructions
- `SESSION_*.md` — session notes (these are AI chat transcripts; the useful info has been distilled into the docs above)
