# Quick Start Guide - Distillery Automation

**Fast reference for common tasks - detailed info in README.md and session docs**

---

## Connecting to the Pi
```bash
ssh pi@distillery-pi.local
cd ~/distillery-automation
```

---

## Testing Hardware

### Test Load Cells (Weight Platform)
```bash
python3 weigh.py
```
- Shows real-time weight
- Press **Ctrl+C** to stop

### Test MOSFET HAT (Switches/Relays)
```bash
python3 src/hardware/mosfet_hat.py
```
- Cycles all 8 channels
- Watch channel 5 test load

### Test Thermocouple HAT (Temperature Sensors)
```bash
python3 src/hardware/thermocouple_hat.py
```
- Shows all 8 channels
- Channels 1 & 2 are K-type

### Recalibrate Load Cells
```bash
python3 calibrate_hx711.py
```
- Follow prompts
- Need known weight

---

## Checking System Status

### Verify HATs Detected
```bash
sudo i2cdetect -y 1
```
- Should show I2C addresses (like 0x30)

### Check I2C Enabled
```bash
sudo raspi-config
```
- Interface Options > I2C > Enable

### View Calibration Data
```bash
cat calibration_data.txt
```

---

## Common Tasks

### Update from GitHub
```bash
cd ~/distillery-automation
git pull
```

### Save Changes to GitHub
```bash
git add .
git commit -m "Description of changes"
git push
```

### Reboot Pi
```bash
sudo reboot
```

### Shutdown Pi Safely
```bash
sudo shutdown -h now
```
Wait for green LED to stop blinking before unplugging power

---

## File Locations

**Test Scripts:**
- `weigh.py` - Weight monitor
- `test_hx711.py` - Load cell test
- `calibrate_hx711.py` - Calibration tool
- `src/hardware/mosfet_hat.py` - MOSFET test
- `src/hardware/thermocouple_hat.py` - Thermocouple test

**Data Files:**
- `calibration_data.txt` - Load cell calibration
- `data/` - Data logging (future)
- `logs/` - System logs (future)

**Documentation:**
- `README.md` - Main project documentation
- `SESSION_3_COMPLETE.md` - Latest session notes
- `ARCHITECTURE.md` - System design
- `CHANGELOG.md` - Version history

---

## Hardware Configuration

**Current Stack (Bottom to Top):**
1. Raspberry Pi 4B
2. 8-MOSFET HAT (Stack 0)
3. 8-Thermocouple HAT (Stack 0)
4. Breakout HAT (HX711 connected)

**Load Cells:**
- GPIO 5 = DT (Data)
- GPIO 6 = SCK (Clock)

**DIP Switches:**
- Both Sequent HATs: Stack 0
- Don't change unless adding more HATs

---

## Troubleshooting Quick Fixes

**Load cells not working:**
```bash
cd ~/hx711py
sudo python3 setup.py install
```

**MOSFET HAT not working:**
```bash
cd ~/8mosind-rpi/python
sudo python3 setup.py install
```

**Thermocouple HAT not working:**
```bash
cd ~/smtc-rpi
sudo make install
```

**Enable I2C if HATs not detected:**
```bash
sudo raspi-config
# Interface Options > I2C > Enable
sudo reboot
```

---

## Starting a New Session with Claude

Say this to Claude:
```
Claude - distillery project at github.com/jaschagulden/distillery-automation. 
Read SESSION_3_COMPLETE.md. Ready to [describe your task].
```

Example:
```
Claude - distillery project at github.com/jaschagulden/distillery-automation. 
Read SESSION_3_COMPLETE.md. Ready to wire the pumps to the MOSFET HAT.
```

---

## Safety Reminders

⚠️ **Current System:**
- Manual monitoring REQUIRED
- Safety systems NOT yet implemented
- DO NOT leave unattended
- Temperature limits not automatic

🔨 **In Development:**
- Automatic over-temperature shutdown
- Emergency stop system
- Watchdog monitoring
- Alert notifications

---

## Getting Help

**Within a Session:**
- Ask Claude to explain any command before running it
- Request step-by-step breakdowns
- Say "I don't understand" - Claude will clarify

**Between Sessions:**
- Read SESSION_3_COMPLETE.md for full context
- Check README.md for overview
- Review this QUICK_START.md for commands

**Remember:**
- No coding experience needed
- All steps explained clearly
- Ask questions anytime
- We do things correctly, not quickly

---

**Last Updated:** February 14, 2025  
**Current Status:** All hardware installed and tested  
**Next Steps:** Equipment integration (pumps, valves, heaters)
