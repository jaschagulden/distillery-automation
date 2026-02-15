# Distillery Automation System

**Raspberry Pi-based automation and monitoring system for small-scale distillation operations**

---

## Project Status: In Development (35% Complete)

This system automates temperature monitoring, weight measurement, and equipment control for a distillation setup using a Raspberry Pi 4B with multiple stackable HAT modules.

**Latest Update:** February 14, 2025 - All hardware installed and tested successfully

---

## Hardware Components

### Raspberry Pi Setup
- **Main Computer:** Raspberry Pi 4B (fresh SD card, Raspberry Pi OS)
- **Network:** Accessible at `distillery-pi.local`
- **I2C Communication:** Enabled for HAT communication

### Installed Hardware (Stacked Bottom to Top)
1. **Raspberry Pi 4B** - Main controller
2. **Sequent 8-MOSFET HAT** (Stack 0)
   - Controls 8 solid-state switches
   - Used for pumps, valves, heaters
   - Test load on channel 5 verified working
3. **Sequent 8-Thermocouple HAT** (Stack 0)
   - Reads 8 thermocouple temperature sensors
   - K-type thermocouples on channels 1 & 2
   - Accurate temperature readings confirmed
4. **Breakout HAT**
   - Provides access to GPIO pins
   - HX711 load cell amplifier connected here

### Sensors
- **4x Load Cells** - Weight measurement platform
  - Connected via HX711 amplifier
  - GPIO 5 (Data), GPIO 6 (Clock)
  - Calibrated and accurate
  - Calibration data stored in `calibration_data.txt`
- **K-Type Thermocouples** (2 installed, capacity for 6 more)
  - Channels 1 & 2 active
  - Temperature monitoring for distillation column

---

## Quick Start Guide

### Connecting to the Raspberry Pi

**From another computer on the same network:**
```bash
ssh pi@distillery-pi.local
```
Enter password when prompted.

**Navigate to project:**
```bash
cd ~/distillery-automation
```

### Testing Hardware

**Test Weight Scale:**
```bash
python3 weigh.py
```
- Shows real-time weight readings
- Press Ctrl+C to stop

**Test MOSFET HAT (Switches/Relays):**
```bash
python3 src/hardware/mosfet_hat.py
```
- Cycles through all 8 channels
- Watch test load on channel 5

**Test Thermocouple HAT (Temperature Sensors):**
```bash
python3 src/hardware/thermocouple_hat.py
```
- Shows temperatures from all channels
- Channels 1 & 2 display K-type readings

**Recalibrate Load Cells (if needed):**
```bash
python3 calibrate_hx711.py
```
- Follow on-screen instructions
- Use known weight for calibration

---

## Project Structure
```
distillery-automation/
├── README.md                    # This file
├── SESSION_3_COMPLETE.md        # Latest session notes
├── ARCHITECTURE.md              # System design details
├── QUICK_START.md              # Quick reference guide
├── CHANGELOG.md                # Version history
│
├── src/                        # Source code
│   ├── hardware/               # Hardware interface modules
│   │   ├── mosfet_hat.py      # MOSFET HAT test/control
│   │   └── thermocouple_hat.py # Thermocouple HAT test/control
│   ├── controllers/            # Control logic (future)
│   ├── safety/                 # Safety systems (future)
│   └── sequences/              # Automation sequences (future)
│
├── config/                     # Configuration files
├── data/                       # Data logging
├── logs/                       # System logs
├── tests/                      # Test scripts
│
├── weigh.py                    # Real-time weight monitor
├── test_hx711.py              # Load cell test script
├── calibrate_hx711.py         # Calibration utility
├── calibration_data.txt       # Load cell calibration values
└── requirements.txt            # Python dependencies
```

---

## Software Installation

All libraries are installed system-wide for long-term stability (no virtual environment needed for hardware control).

### Installed Libraries

**Load Cell Control:**
- HX711 library (tatobari version)
- Source: https://github.com/tatobari/hx711py

**Sequent Microsystems HATs:**
- lib8mosind: 8-MOSFET HAT control
- sm_tc: 8-Thermocouple HAT control
- Sources: https://github.com/SequentMicrosystems/

**Supporting Libraries:**
- RPi.GPIO: Raspberry Pi GPIO control
- smbus2: I2C communication
- Other dependencies in requirements.txt

### System Configuration
- I2C enabled via `sudo raspi-config`
- SSH enabled for remote access
- Git configured with GitHub access

---

## Current Capabilities

✅ **Weight Measurement**
- Real-time weight monitoring
- Calibrated 4-cell load platform
- Accurate to within grams

✅ **Temperature Monitoring**  
- 8 thermocouple inputs available
- 2 K-type sensors currently installed
- Real-time temperature readings

✅ **Equipment Control**
- 8 MOSFET channels for switching
- Solid-state control for pumps, valves, heaters
- All channels tested and operational

✅ **Data Logging** (framework in place)
- Ready for temperature/weight logging
- File structure established

---

## Safety Features (In Development)

🔨 **Planned Safety Systems:**
- Over-temperature shutdown
- Emergency stop functionality  
- Watchdog timer for system monitoring
- Automated alerts for dangerous conditions

⚠️ **Current Status:**
- Manual monitoring required
- Safety systems not yet implemented
- DO NOT leave system unattended

---

## Documentation

- **SESSION_3_COMPLETE.md** - Latest session notes, detailed hardware status
- **SESSION_2_COMPLETE.md** - Previous session (SD card replacement, recalibration)
- **ARCHITECTURE.md** - System architecture and design decisions
- **QUICK_START.md** - Fast reference for common tasks
- **CHANGELOG.md** - Version history and updates

---

## Troubleshooting

**Load cells not responding?**
```bash
python3 weigh.py
```
If error, reinstall HX711:
```bash
cd ~/hx711py
sudo python3 setup.py install
```

**HATs not working after reboot?**
Check I2C is enabled:
```bash
sudo raspi-config
# Interface Options > I2C > Enable
```

**Verify HAT detection:**
```bash
sudo i2cdetect -y 1
```
Should show I2C addresses for installed HATs.

**Complete reinstall needed?**
See SESSION_3_COMPLETE.md troubleshooting section for detailed library reinstall commands.

---

## Development Roadmap

### Phase 1: Hardware Setup ✅ (COMPLETE)
- [x] Raspberry Pi installation
- [x] Load cell calibration
- [x] MOSFET HAT installation
- [x] Thermocouple HAT installation
- [x] All hardware tested and verified

### Phase 2: Equipment Integration (IN PROGRESS)
- [ ] Wire pumps to MOSFET channels
- [ ] Install thermocouples in distillation column
- [ ] Connect valves and heating elements
- [ ] Test all equipment under power

### Phase 3: Safety Systems (NEXT)
- [ ] Over-temperature monitoring
- [ ] Emergency shutdown procedures
- [ ] Watchdog implementation
- [ ] Alert system

### Phase 4: Control Logic
- [ ] Automated temperature control
- [ ] Pump sequencing
- [ ] Cut automation
- [ ] User interface

### Phase 5: Data & Monitoring
- [ ] Real-time data logging
- [ ] Historical data analysis
- [ ] Remote monitoring
- [ ] Performance optimization

---

## Important Notes

**For Non-Programmers:**
- All commands are documented with explanations
- Step-by-step instructions provided
- No coding experience required to operate
- Ask for clarification on anything unclear

**Long-Term Stability:**
- System-wide library installations
- No virtual environment for hardware control
- Proper documentation for all changes
- Regular GitHub backups

**Working with Claude AI:**
- Start sessions with: "Claude - distillery project at github.com/jaschagulden/distillery-automation"
- Reference latest SESSION_X_COMPLETE.md for context
- All sessions documented for continuity

---

## Contributing

This is a personal project, but documentation and code are maintained for:
- Future reference
- Troubleshooting
- Potential sharing with other hobbyist distillers
- Learning and education

---

## License

Personal project - all rights reserved by owner.

---

## Credits

**Project Owner:** Jascha Gulden  
**AI Assistant:** Claude (Anthropic)  
**Hardware:** Sequent Microsystems HATs  
**Platform:** Raspberry Pi Foundation  

---

## Contact & Support

**For next session:**
```bash
ssh pi@distillery-pi.local
cd ~/distillery-automation
```

Read SESSION_3_COMPLETE.md for current status and next steps.

---

**Last Updated:** February 14, 2025  
**Version:** 0.35 (35% complete)  
**Status:** Hardware installation complete, moving to equipment integration
