# Palmeri Distillery Automation — Claude Code Context

**Owner:** Jascha Gulden | **Collaborator:** Tim Gulden
**Status:** ~70% complete (March 2026) | Hardware working, control software in progress

---

## What This System Does

Automates a complete distillation cycle on a small commercial distillery. The still runs a batch process:

**IDLE → FILL → HEAT → DISTILL (Heads / Hearts / Tails) → DISCHARGE → CIP → IDLE**

Key hardware: 200L pot still, 1050L mash tank, 1050L discharge tank, 11kW heating (2× 5.5kW elements), 4 pumps, 6 valves, thermocouple and weight sensors throughout.

Full process and operational detail: `docs/operational_manual.md`

---

## The Three Pis

| Pi | Hostname | IP | Role |
|----|----------|----|------|
| Pi 1 | `distillery-pi` | 192.168.0.31 | Main controller — sensors, HATs, this repo |
| Pi 2 | — | — | Portrait display kiosks (slideshow) |
| Pi 3 | `palmeri-ai` | 192.168.0.33 | RPi 5 + Hailo-8L — voice AI avatar kiosk |

**This repo is Pi 1 only.** Pi 3 code lives at `~/palmeri-ai/` on Pi 3.

---

## Hardware on Pi 1

**HAT stack (bottom to top):**
1. Raspberry Pi 4B
2. Sequent 8-MOSFET HAT (Stack 0) — controls pumps, valves, heating SSRs via `lib8mosind`
3. Sequent 8-Thermocouple HAT (Stack 0) — reads K-type thermocouples via `sm_tc`
4. Breakout HAT — HX711 load cell amplifier on GPIO 5 (data) / GPIO 6 (clock)

**Sensors:**
- 4× load cells (HX711) — mash tank, still, discharge tank, distillate collection
- 8× thermocouple inputs — channels 1 & 2 active (K-type), 6 available
- Calibration values in `calibration_data.txt` (TARE: −241007.50, CAL: −25651.61)

**Actuators:**
- 2× 5.5kW heating elements via SSR (PWM control) — HIGH VOLTAGE, 240V
- 4 pumps: mash transfer, condenser cooling, discharge, CIP
- 6 valves: mash inlet, heads, hearts, tails, discharge, CIP

**All libraries installed system-wide (no virtualenv).** Hardware specs detail: `docs/hardware_specs.md`

---

## Pi 3 — Voice AI Kiosk (for context, not in this repo)

- Two "American Gothic" avatars: Amy (farm/agave) and Norman (distillery)
- Stack: faster-whisper (STT) → Ollama/gemma2:2b → piper-tts (TTS)
- Voices: `~/piper-voices/en_US-amy-medium.onnx` and `en_US-norman-medium.onnx`
- Pipeline: `~/palmeri-ai/voice_pipeline.py` | Display: `~/palmeri-ai/avatar_display.py`
- Currently connects to Pi 1 via Flask endpoint — MQTT integration is planned

---

## Current Software State

### Working (runs on Pi 1 today)
- `sensor_server.py` — Flask server at `http://192.168.0.31:5000`; `/sensors` returns weight + temps as JSON, `/status` returns online check
- `weigh.py` — real-time weight display
- `calibrate_hx711.py` — load cell calibration utility
- `test_hx711.py` — load cell test
- `src/hardware/mosfet_hat.py` — cycles all 8 MOSFET channels (test script)
- `src/hardware/thermocouple_hat.py` — reads all 8 thermocouple channels (test script)

### Stubs only (not yet implemented)
- `src/main.py` — skeleton with TODOs
- `src/controllers/` `src/safety/` `src/sequences/` `src/gui/` — empty `__init__.py` files
- `tests/hardware_test_suite.py` — all test functions return `False` (not implemented)

---

## Common Operations

**Connect to Pi 1:**
```bash
ssh pi@distillery-pi.local    # or ssh pi@192.168.0.31
cd ~/distillery-automation
```

**Pull latest code onto Pi:**
```bash
git pull
```

**Run hardware tests:**
```bash
python3 weigh.py                          # live weight
python3 src/hardware/mosfet_hat.py        # cycle MOSFET channels
python3 src/hardware/thermocouple_hat.py  # read temperatures
sudo i2cdetect -y 1                       # verify HATs detected on I2C
```

**Reinstall libraries if broken:**
```bash
cd ~/hx711py && sudo python3 setup.py install          # load cells
cd ~/8mosind-rpi/python && sudo python3 setup.py install  # MOSFET HAT
cd ~/smtc-rpi && sudo make install                     # thermocouple HAT
```

---

## Safety Rules — Non-Negotiable

**DO NOT:**
- Write code that enables heating elements without safety interlock checks
- Push to `main` without checking with the other collaborator
- Leave heating elements enabled in any test script
- Run automated sequences on real hardware until the safety monitor is implemented

**Current safety status: NOT IMPLEMENTED.** Manual monitoring required. Do not leave system unattended during operation.

Safety system implementation is the top priority before any automated sequences run. See `docs/architecture_from_tim.md` Suggestion 3.

Safety limits (from `config/hardware_config.yaml`):
- Max still temp: 105°C | Emergency shutdown: 110°C
- Max still weight: 220kg | Watchdog timeout: 10s

---

## Architecture Direction

**Status: proposals under review — not yet agreed.**

Tim has prepared architectural suggestions covering hardware interfaces, a simulator, safety monitor, recipe system, and MQTT integration. Jascha is reviewing these.

- `docs/architecture_from_tim.md` — Tim's proposals in plain language; CC can guide Jascha through these
- `docs/architecture_from_tim_detail.md` — implementation detail for each proposal

**After the review is complete, update this section** to replace the above with the agreed architecture, build order, and any hard rules for new code.

---

## Known Issues

**Pin conflicts in `config/hardware_config.yaml`** — must be resolved before writing any drivers:

| Pin | Device 1 | Device 2 |
|-----|----------|----------|
| 12 | heating/element_1 | valves/cip |
| 16 | heating/element_2 | pumps/discharge |
| 25 | thermocouples/ambient | valves/heads |
| 8 | thermocouples/still_mash | valves/hearts |
| 7 | thermocouples/condenser | valves/tails |

Correct assignments must come from the actual Pi 1 wiring. Jascha to resolve.

---

## Collaboration

- **Jascha** — owner, hardware expert, works directly with Claude Code on Pi 1 implementation
- **Tim** — collaborator, proposes changes via PRs for Jascha to review and decide on

Both collaborators push to `main` carefully. PRs used for anything structural.

---

## Keeping This Document Current

CLAUDE.md is the starting context for every CC session — keep it accurate. Update it when:

| Trigger | What to update |
|---------|----------------|
| Architecture review complete (Tim's suggestions reviewed with Jascha) | Replace "Architecture Direction" section with agreed decisions; update Collaboration work split; delete `docs/architecture_from_tim.md` and `docs/architecture_from_tim_detail.md` |
| Pin conflicts resolved in `hardware_config.yaml` | Remove the Known Issues pin conflict table |
| Something moves from "stubs only" to working | Move it from the stubs list to the working list in Current Software State |
| A new Pi or major piece of hardware is added | Add it to The Three Pis / Hardware section |

---

## Key Documentation

| File | What it is |
|------|-----------|
| `README.md` | Project overview and hardware setup |
| `ARCHITECTURE.md` | System design and state machine diagram |
| `docs/architecture_from_tim.md` | Tim's architectural proposals |
| `docs/architecture_from_tim_detail.md` | Implementation detail for proposals |
| `docs/hardware_specs.md` | Hardware specifications and wiring |
| `docs/operational_manual.md` | Operating procedures |
| `QUICK_START.md` | Fast reference for common commands |
| `config/hardware_config.yaml` | GPIO pin assignments and safety limits |
| `SESSION_*.md` | Historical AI chat transcripts (context only) |
