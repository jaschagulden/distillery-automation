# Suggestions from Tim: Building the Software Like You'd Build the Hardware

*A set of architectural proposals for Jascha to review — nothing is decided yet.*

---

<!-- NOTE FOR CLAUDE CODE — not for Jascha to read:
Jascha may arrive at this conversation without having read this document.
Your job is to guide him through it. Here's how:

1. Summarize the document in 2-3 sentences so he knows what he's looking at.
2. Walk through the 6 suggestions one at a time — describe each one in plain terms,
   using the hardware analogies in this document (connectors, bench test setup, etc.).
3. After each suggestion, ask him the "Question for you" at the end of that section.
4. Based on his answer: implement it, modify it to fit his vision, or skip it.
5. For implementation detail on any suggestion, read the corresponding section of
   docs/architecture_technical.md (section numbers match suggestion numbers).

Nothing in this document changes existing working code. All suggestions are additive.
The one exception is Suggestion 6 (pin conflicts) — that is a bug fix, not optional.
-->

---

## The Core Idea

You've spent your career designing systems where the pieces have to work together reliably, often in high-stakes environments. The way you think about hardware is exactly the right way to think about this software.

The suggestion is simple: **build the software the same way you'd build the hardware.**

In hardware, before you wire anything together, you define the connectors. A BNC connector means something specific — impedance, voltage range, signal type. You can swap what's behind it as long as it honors the spec. The rest of the system doesn't need to know or care what's plugged in.

This document is a set of proposals for doing the same thing in software — defining the connectors before building the components, so everything composes cleanly as the system grows.

---

## Suggestion 1: Define the Connectors First (Hardware Interfaces)

**The problem it solves:** If you build each hardware driver independently — thermocouple first, then load cells, then MOSFET outputs — each one tends to speak its own dialect. The control logic above them then has to speak all those dialects. Connecting them becomes complicated.

**The suggestion:** Before writing any driver, define what each type of hardware *looks like* to the rest of the system. These definitions (called interfaces) are the software equivalent of a standardized connector:

```
TemperatureSensor:
  - read_celsius()    → returns a number
  - is_fault()        → returns true or false

WeightSensor:
  - read_kg()         → returns a number
  - tare()

Switch (pumps, valves):
  - on()
  - off()
  - is_on()           → returns true or false

HeatingOutput (SSR):
  - set_duty_cycle()  → 0–100%
  - off()
```

The PID controller, safety monitor, and all the sequences are then written against these definitions — not against the specific HAT or library. If you ever change the thermocouple HAT model, or add a second load cell type, nothing above the driver layer changes.

**What Tim is suggesting we implement:** A file called `src/hardware/interfaces.py` that defines these contracts before any drivers are written. The technical details are in §3 of `architecture_technical.md`.

**Question for you:** Does this match how you think about it? Are there hardware types missing from the list above that we should define?

---

## Suggestion 2: Build a Bench Test Setup (The Simulator)

**The problem it solves:** Right now, to test any control logic, you have to be at the distillery with the still running. That's slow, and for early-stage testing it's potentially risky. It also means Tim can't work on the control logic from his end.

**The suggestion:** Build a simulated distillery — fake sensors and actuators that behave plausibly — running on any laptop. It doesn't need to be a perfect physics model. Just enough to be useful:

- Simulated still temperature rises when heat is applied
- Simulated distillate weight increases when temperature is above the boiling point
- Simulated valves remember whether they're open or closed

With this in place, the entire control sequence — Fill → Heat → Distill → Discharge — can be run on a laptop, in seconds, without touching hardware. You test the *logic* on the bench, then plug in the real drivers when the logic is right.

This is exactly what you'd do with a prototype before committing to the production version.

**What Tim is suggesting we implement:** A set of simulated hardware implementations in `src/hardware/simulator/`. These use the same interfaces as the real drivers (Suggestion 1) so they're drop-in replacements for testing. The technical details are in §4 of `architecture_technical.md`.

**Question for you:** How rough is rough enough for the simulator to be useful to you? Just on/off states, or do you want it to behave more like the real thermal dynamics?

---

## Suggestion 3: The Safety Interlock Runs Independent of Everything Else

**The problem it solves:** In the current design, safety checks would be called from inside the main control loop. That means if the control loop hangs, crashes, or gets stuck — the safety checks stop running too.

**The suggestion:** The safety monitor runs as a completely separate process — not called by the control logic, not dependent on it. It reads the sensors directly and independently. If it sees a dangerous condition, it cuts power regardless of what the control system is doing. This mirrors how a well-designed hardware interlock works: the over-temperature trip doesn't run through the main controller. It cuts power directly, independently, on its own circuit.

This also means the safety system can be read, audited, and tested completely separately from the control logic — a much smaller piece of code to review when you need to trust it.

**What Tim is suggesting we implement:** `src/safety/safety_monitor.py`, running in its own thread, with direct sensor access and the ability to cut all outputs. Tim's strong suggestion is that this gets built *before* any automated sequences run on real hardware. The technical details are in §5 of `architecture_technical.md`.

**Question for you:** What are the conditions you'd want it to respond to? The config file has some limits defined (105°C max still temp, 220kg max weight, 30min max pump runtime) — do those match what you'd set if you were wiring a hardware interlock?

---

## Suggestion 4: A Recipe File Is Your SOP

**The problem it solves:** As you develop the system, you'll want to adjust setpoints — a different target temperature for a rum run vs. a whiskey run, different cut points, different heat ramp rates. If those numbers are baked into the code, changing them means editing Python. That's fragile and error-prone.

**The suggestion:** Every distillation run is defined by a plain-text recipe file (YAML format — human-readable, no special software to edit). The code reads the recipe and executes it. You change a run's parameters by editing the recipe, not the code.

```yaml
# A recipe file — no code, just parameters
phases:
  heat:
    target_temp_c: 78.5
    max_duration_min: 180
    abort_if_temp_above_c: 105

  hearts:
    collection_weight_kg: 8.0
    target_flow_ml_per_min: 40
```

Different grain bill, different cuts, different heat profile — new recipe file, no code change. This is exactly how you'd write a lab SOP.

**What Tim is suggesting we implement:** A recipe schema (what fields a recipe can have) and a sequence engine that reads any recipe and executes it. The technical details are in §7 of `architecture_technical.md`.

**Question for you:** Looking at a real distillation run — what are the parameters you'd want to be able to dial in per recipe, vs. the ones that are fixed for the hardware?

---

## Suggestion 5: The Three Pis Talk on a Shared Bus (MQTT)

**The problem it solves:** Right now Pi 3 (the voice AI) connects to Pi 1 by calling a specific HTTP endpoint. That's a direct wire — if Pi 1's API changes, Pi 3 breaks. Adding a new display or remote monitor means writing more direct connections.

**The suggestion:** Use a message bus (MQTT, standard in industrial systems — think CAN bus for the network). Pi 1 continuously publishes readings:

```
distillery/sensors/still_temp_c      → 76.4
distillery/sensors/still_weight_kg   → 152.3
distillery/control/current_phase     → hearts
distillery/safety/status             → ok
```

Any Pi can subscribe to any topic. The voice AI answers "what's the temperature?" by reading the latest published value. The display Pis show whatever they want. A future remote monitor just subscribes — zero changes to Pi 1 code.

This is a fairly small change to `sensor_server.py` and gives you a much more flexible network.

**What Tim is suggesting we implement:** Mosquitto (MQTT broker) on Pi 1, and update `sensor_server.py` to publish to MQTT topics in addition to (or instead of) the Flask endpoints. The technical details are in §8 of `architecture_technical.md`.

**Question for you:** Does the voice AI on Pi 3 currently pull from Pi 1's Flask endpoint, or does it read sensors locally? That affects how much work this is.

---

## Suggestion 6: Fix the Pin Assignments First

**This one isn't a suggestion — it's a bug that needs to be fixed before we write any control code.**

The hardware config file (`config/hardware_config.yaml`) currently assigns the same GPIO pin to multiple devices. For example, pin 12 is listed as both the first heating element and the CIP valve. These can't both be right.

The correct pin assignments exist only in one place: the actual wiring on Pi 1. Before writing any driver code, we need to go through the config file with the real wiring in hand and make it accurate.

**What we're asking:** Sit down with Pi 1, check the actual wiring, and correct `config/hardware_config.yaml`. CC can help you go through it pin by pin. The full conflict table is in §12 of `architecture_technical.md`.

---

## The Suggested Build Order

Here's the sequence Tim is proposing, with who does what:

| Step | What | Who | Notes |
|------|------|-----|-------|
| 1 | Fix pin conflicts in `hardware_config.yaml` | Jascha | Needs physical Pi access |
| 2 | Define hardware interfaces (`interfaces.py`) | Together | Short document, big decision |
| 3 | Build simulator | Tim | Enables laptop development |
| 4 | Build safety monitor | Together | Before any sequences on hardware |
| 5 | PID controller | Tim | Pure math, no hardware needed |
| 6 | Recipe schema + sequence engine | Together | Jascha shapes the recipe format |
| 7 | Real hardware drivers | Jascha | Drop-in replacements for simulator |
| 8 | MQTT integration | Together | Once control is working |
| 9 | GUI / displays / voice AI | Together | Last, built against the interfaces |

Steps 1–6 result in a fully testable control system running on a laptop. Step 7 is where the hardware comes in — and because everything is built against interfaces, it's a clean drop-in.

---

## What Stays the Same

To be clear about what Tim is *not* suggesting:

- The existing working code (`sensor_server.py`, `weigh.py`, the HAT test scripts) stays as-is and keeps running on Pi 1
- No changes to Pi 2 or Pi 3
- The overall architecture Jascha designed (the state machine in `ARCHITECTURE.md`, the module structure in `src/`) is sound — this builds on it, doesn't replace it
- Nothing in this document requires immediate action on the running system

---

## Starting the Conversation with Claude Code

When you're ready to work through these with CC, use this prompt:

> "I'd like to review Tim's architectural suggestions with you. Please read `docs/architecture_from_tim.md` and `docs/architecture_technical.md`. Then let's go through the suggestions one at a time — I'll tell you what I agree with, what I want to change, and what I want to skip. For anything I agree with, help me implement it."

CC will read both documents and walk you through each suggestion. You don't need to understand the technical details in advance — that's what CC is there to explain and implement.

---

*From Tim, March 2026. Questions or reactions: send notes back through the repo or just mark up this document.*
