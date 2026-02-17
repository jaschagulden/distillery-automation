# Session 5 Complete - February 17, 2026

## Status: Two-Pi Network System Operational

---

## What We Accomplished Today

### Second Raspberry Pi 4B Setup
- Flashed fresh Raspberry Pi OS
- Connected 5" touchscreen (HDMI + touch working)
- Connected 1.28" round GC9A01 display (SPI)
- Installed all required libraries
- Configured SSH keepalive

### Network Communication
- Both Pis communicating over local network
- Static IPs assigned and locked in:
  - Pi #1 (distillery-pi): 192.168.0.31
  - Pi #2 (distillery-pi-2): 192.168.0.32
- Pi #1 serves live sensor data via Flask
- Pi #2 pulls and displays data on round screen
- 0% packet loss, <1ms latency

### Auto-Start Services
- Pi #1: sensor-server.service starts on boot
- Pi #2: distillery-display.service starts on boot
- Both Pis fully autonomous on power-up
- No manual intervention needed

---

## Current Hardware

### Pi #1 (distillery-pi - 192.168.0.31) - Main Controller
- 8-MOSFET HAT (Stack 0, I2C)
- 8-Thermocouple HAT (Stack 0, I2C)
- Breakout HAT
- HX711 load cells (GPIO 5, 6)
- GC9A01 1.28" round display (SPI)
- HDMI1: HAMTYSAN 10.1" touchscreen

### Pi #2 (distillery-pi-2 - 192.168.0.32) - Display Node
- GC9A01 1.28" round display (SPI)
- 5" touchscreen (HDMI)
- GPIO pins free for future HATs
- Ready for expansion

---

## Network Architecture
```
Pi #1 (192.168.0.31)          Pi #2 (192.168.0.32)
┌─────────────────────┐        ┌─────────────────────┐
│ Sensors & HATs      │        │ Display Node        │
│ - Load cells        │        │ - Round display     │
│ - Thermocouples     │◄──────►│ - 5" touchscreen    │
│ - MOSFET control    │  HTTP  │ - Future I/O        │
│ - sensor_server.py  │        │ - display_pi2.py    │
│   port 5000         │        │                     │
└─────────────────────┘        └─────────────────────┘
```

## API Endpoints (Pi #1)

**Base URL:** http://192.168.0.31:5000

- `GET /sensors` - Returns all live sensor data:
  - temp1_c, temp1_f
  - temp2_c, temp2_f
  - weight_kg, weight_lb
  - timestamp

- `GET /status` - Returns server status

---

## Auto-Start Services

### Pi #1: sensor-server.service
```bash
# Check status
sudo systemctl status sensor-server.service

# Start/Stop/Restart
sudo systemctl start sensor-server.service
sudo systemctl stop sensor-server.service
sudo systemctl restart sensor-server.service

# View logs
journalctl -u sensor-server.service -f
```

### Pi #2: distillery-display.service
```bash
# Check status
sudo systemctl status distillery-display.service

# Start/Stop/Restart
sudo systemctl start distillery-display.service
sudo systemctl stop distillery-display.service
sudo systemctl restart distillery-display.service

# View logs
journalctl -u distillery-display.service -f
```

---

## Files

### Pi #1 (in ~/distillery-automation/)
- `sensor_server.py` - Flask server sharing sensor data
- `distillery_display_pi2.py` - Pi #2 display script (backup copy)
- `palmeri_cycling_display.py` - Pi #1 round display script
- `palmeri_logo.png` - Company logo

### Pi #2 (in ~/)
- `distillery_display_pi2.py` - Main display script

---

## SSH Quick Reference
```bash
# Connect to Pi #1
ssh pi@192.168.0.31

# Connect to Pi #2
ssh pi@192.168.0.32

# Or use hostnames
ssh pi@distillery-pi.local
ssh pi@distillery-pi-2.local
```

---

## Troubleshooting

### Pi #2 showing "NO DATA" or "Pi #1 offline?"
```bash
# Check Pi #1 sensor server is running
sudo systemctl status sensor-server.service

# Restart if needed
sudo systemctl restart sensor-server.service

# Test from Pi #2
curl http://192.168.0.31:5000/sensors
```

### Display not updating on Pi #2
```bash
# Check display service
sudo systemctl status distillery-display.service

# Restart display service
sudo systemctl restart distillery-display.service
```

### SSH disconnecting
- SSH keepalive configured on both Pis
- Settings in /etc/ssh/sshd_config
- ClientAliveInterval 60, ClientAliveCountMax 10

---

## Next Steps

### Immediate
1. Set up auto-start for Pi #1 round display (palmeri_cycling_display.py)
2. Build custom touchscreen control interface (10.1" on Pi #1)
3. Wire actual distillery equipment to MOSFET channels
4. Add more sensor endpoints to sensor_server.py

### Short Term
1. Add MOSFET control via network (Pi #2 can control Pi #1 equipment)
2. Data logging to file/database
3. Web dashboard accessible from any device
4. Safety interlocks

### Future
1. Deploy solar wireless Pico 2W thermocouple nodes
2. Add more Pi nodes as distillery grows
3. Historical data graphs on touchscreen
4. Remote monitoring via internet

---

## For Next Session

**Reconnect:**
```bash
ssh pi@192.168.0.31   # Pi #1
ssh pi@192.168.0.32   # Pi #2
```

**Say to Claude:**
```
Claude - distillery project at github.com/jaschagulden/distillery-automation.
Read SESSION_5_COMPLETE.md. Ready to [describe next task].
```

---

**Project Owner:** Jascha Gulden
**Date:** February 17, 2026
**Current Status:** Two-Pi network system operational, auto-start configured
**Project Progress: ~55% complete**
**Next Major Milestone:** Custom touchscreen control interface
