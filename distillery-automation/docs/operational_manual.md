# Operational Manual

## System Overview
The distillery automation system controls a complete distillation cycle from mash transfer through cleanup, with minimal operator intervention.

**Capacity:** 200L still, 1050L mash tank, 1050L discharge tank  
**Power:** 11kW heating (2x 5.5kW elements)  
**Control:** Raspberry Pi 4B with custom automation software  

---

## Pre-Operation Checklist

### Daily Startup
- [ ] Verify all tanks are in proper condition
- [ ] Check that discharge tank has sufficient capacity
- [ ] Verify distillate collection vessels are clean and ready
- [ ] Inspect all valve and pump connections for leaks
- [ ] Confirm water supply for condenser and CIP is available
- [ ] Check that emergency stop is functional
- [ ] Verify proper ventilation
- [ ] Review recipe parameters for today's run

### System Startup
```bash
# SSH into Raspberry Pi (if remote) or use local terminal
ssh pi@distillery-pi

# Navigate to project directory
cd ~/distillery-automation

# Activate virtual environment
source venv/bin/activate

# Start the system
python src/main.py
```

### Visual Inspection
- All indicator lights functioning
- No unusual sounds from pumps or valves
- Temperature readings are reasonable (near ambient)
- Weight readings are stable and reasonable

---

## Standard Operating Procedure

### 1. Fill Mash Tank
**Manual Step:**
1. Fill the 1050L mash tank with fermented mash
2. Verify fill level visually and on system display
3. Ensure tank is properly sealed

### 2. Select Recipe
**In GUI:**
1. Click "Select Recipe"
2. Choose appropriate recipe for the mash type
3. Review parameters:
   - Target still fill: ___ kg
   - Heating setpoint: ___ °C
   - Flow rate target: ___ ml/min
   - Heads cut: ___ kg
   - Hearts cut: ___ kg
   - Tails cut: ___ kg
4. Confirm selection

### 3. Start Automated Run
1. Click "START" button
2. System will display "RUNNING - Fill Sequence"
3. Monitor the process on main display

### 4. Automated Sequence (Monitor Only)

#### Phase 1: Fill Still
- System opens mash valve
- Mash pump starts
- Still weight increases
- Pump stops at target weight
- Valve closes
- **Expected duration:** 5-10 minutes

#### Phase 2: Heat to Setpoint
- Heating elements activate
- Temperature rises gradually
- PID controller maintains heating rate
- **Expected duration:** 60-90 minutes

#### Phase 3: Distillation
- Condenser cooling starts when approaching setpoint
- Vapor temperature stabilizes
- Distillate begins to flow
- **Heads collection** begins (first fraction)
  - Lighter alcohols, undesirable compounds
  - Collected to "heads" vessel
- Automatic transition to **Hearts**
  - Prime product
  - Collected to "hearts" vessel
- Automatic transition to **Tails**
  - Heavier compounds
  - Collected to "tails" vessel
- **Expected duration:** 2-4 hours

#### Phase 4: Discharge
- Heating stops
- System waits for cool-down (optional, based on recipe)
- Discharge pump starts
- Spent mash pumped to discharge tank
- System monitors for stable weight (still empty)
- **Expected duration:** 10-20 minutes

#### Phase 5: Clean-In-Place (CIP)
- CIP valve opens
- Fresh water flushes through still
- Runs for programmed duration
- Drains to discharge tank
- **Expected duration:** 2-5 minutes

#### Phase 6: Complete
- System returns to IDLE state
- Ready for next cycle
- Notification shown

### 5. Post-Run Tasks
**Manual:**
1. Collect distillate fractions from vessels
2. Label and store appropriately
3. Empty discharge tank as needed
4. Inspect still interior (periodic, not every run)
5. Record run data if doing manual logging

---

## Monitoring During Operation

### Normal Indications
- Temperatures rising smoothly during heating
- Weight readings stable or changing as expected
- Flow rate steady during distillation
- No alarm indicators

### Watch For
- Temperature overshoot or oscillation
- Unexpected weight changes
- Flow rate too high or too low
- Unusual pump or valve sounds

### Critical Alarms
If any alarm triggers:
1. System may pause automatically
2. Follow alarm-specific instructions
3. Do not manually override safety interlocks
4. Contact maintenance if needed

---

## Manual Override Procedures

### When to Use Manual Control
- Testing and commissioning
- Troubleshooting
- Emergency situations
- Maintenance activities

### Manual Controls Available
(Details depend on GUI implementation)
- Individual pump on/off
- Individual valve on/off
- Heating power adjustment
- Manual sequence step advancement

### ⚠️ Safety Note
Manual overrides bypass some automated safety checks. Use with caution and full understanding of system state.

---

## Emergency Procedures

### Emergency Stop
**Red emergency stop button (if installed):**
1. Press immediately if:
   - Fire or smoke
   - Major leak
   - Equipment malfunction
   - Unsafe condition
2. System will:
   - Cut all power to heating
   - Stop all pumps
   - Close all valves
   - Log emergency stop event
3. Do not reset until situation is resolved

### Fire
1. Activate emergency stop
2. Use fire extinguisher if safe to do so
3. Evacuate if necessary
4. Call emergency services if needed

### Leak or Spill
1. Stop affected pumps
2. Close affected valves
3. Contain spill
4. Ventilate area
5. Clean up following safety procedures

### Power Failure
1. System will shut down
2. Heating elements fail-safe (off)
3. When power restored:
   - Do not restart immediately
   - Inspect system state
   - Determine if run can continue or must be aborted
   - Consult troubleshooting guide

### Overheating
If temperature exceeds safe limits:
1. System should automatically shut down heating
2. Cooling continues
3. If manual intervention needed:
   - Turn off heating manually
   - Increase cooling
   - Monitor until temperature drops

---

## Routine Maintenance

### Daily
- Visual inspection
- Check log for any warnings or errors
- Verify calibration dates are current

### Weekly
- Check all connections for tightness
- Inspect pumps for unusual wear or noise
- Clean exterior of equipment
- Backup data logs

### Monthly
- Calibrate load cells
- Test all safety interlocks
- Inspect heating element connections
- Clean still interior thoroughly
- Update software if needed

### Quarterly
- Verify thermocouple calibration
- Inspect and clean condenser
- Check all electrical connections
- Review and tune PID parameters if needed

---

## Troubleshooting Guide

### System Won't Start
- Check power connections
- Verify Raspberry Pi is booted
- Check log files for errors
- Ensure emergency stop is reset

### Fill Sequence Doesn't Complete
- Verify mash tank has sufficient product
- Check pump operation
- Inspect mash valve
- Check load cell readings

### Temperature Won't Reach Setpoint
- Verify heating elements are functioning
- Check SSR operation
- Review PID tuning
- Check for heat loss (insulation)

### Poor Distillate Flow
- Check condenser cooling
- Verify heating power is adequate
- Inspect condenser for fouling
- Check for air leaks

### Erratic Sensor Readings
- Check sensor connections
- Verify calibration
- Look for environmental interference
- Replace sensor if faulty

### Alarm Conditions
Refer to alarm code reference (to be developed)

---

## Data and Logging

### Where Data is Stored
```
/home/pi/distillery-automation/logs/
- distillery.log         # System events
- run_YYYYMMDD_HHMMSS.csv  # Run data

/home/pi/distillery-automation/data/
- historical runs
- calibration records
```

### Reviewing Run Data
```bash
# View recent log entries
tail -f ~/distillery-automation/logs/distillery.log

# View specific run data
cat ~/distillery-automation/data/run_20250211_083000.csv
```

### Backup Recommendations
- Daily: Automatic backup to external storage
- Weekly: Manual verification of backups
- Monthly: Offsite backup copy

---

## Shutdown Procedures

### Normal Shutdown
1. Complete current run or stop at safe point
2. Ensure all valves closed
3. Ensure all pumps off
4. Verify heating is off
5. In software, click "Shutdown System"
6. Wait for confirmation
7. Power off Raspberry Pi properly
8. Secure facility

### Extended Shutdown (Multiple Days)
1. Complete normal shutdown
2. Empty all vessels
3. Run extended CIP cycle
4. Disconnect power to heating elements
5. Document shutdown date and condition

---

## Contact Information

**System Operator:** [Your name]  
**Phone:** [Your number]  
**Email:** [Your email]  

**Technical Support:** [Details]  
**Emergency Contact:** [Details]  

**Last Updated:** 2025-02-11  
**Manual Version:** 1.0  

---

## Notes
This manual will be updated as the system is developed and commissioned. Operators should review changes and updates regularly.
