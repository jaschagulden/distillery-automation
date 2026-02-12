# QUICK START GUIDE

## What You Just Downloaded

This is the complete initial project structure for the Distillery Automation System!

## What's Inside

```
distillery-automation/
├── README.md                  # Project overview
├── ARCHITECTURE.md            # System design documentation
├── CHANGELOG.md               # Version history
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
│
├── config/                   # Configuration files
│   ├── hardware_config.yaml  # Pin assignments & specs
│   ├── recipes/              # Recipe templates
│   └── calibration/          # Sensor calibration data
│
├── src/                      # Source code
│   ├── main.py              # Main application
│   ├── hardware/            # Hardware interfaces (to be built)
│   ├── controllers/         # Control algorithms (to be built)
│   ├── sequences/           # Process sequences (to be built)
│   ├── safety/              # Safety systems (to be built)
│   ├── gui/                 # User interface (to be built)
│   └── utils/               # Utilities (to be built)
│
├── tests/                    # Test scripts
│   └── hardware_test_suite.py
│
├── docs/                     # Documentation
│   ├── GIT_SETUP.md         # How to use Git/GitHub
│   ├── hardware_specs.md    # Hardware specifications
│   ├── calibration_procedures.md
│   └── operational_manual.md
│
├── logs/                     # Runtime logs (created)
└── data/                     # Data storage (created)
```

## Next Steps

### 1. Extract the Archive

**On Raspberry Pi / Linux:**
```bash
tar -xzf distillery-automation.tar.gz
cd distillery-automation
```

**On Windows:**
- Right-click the .tar.gz file
- Extract using 7-Zip or similar
- Navigate to the folder in Command Prompt or PowerShell

**On macOS:**
- Double-click the .tar.gz file (or use Terminal: `tar -xzf distillery-automation.tar.gz`)
- Navigate to the folder in Terminal

### 2. Set Up Git & Push to GitHub

Follow the detailed instructions in: `docs/GIT_SETUP.md`

**Quick version:**
```bash
cd distillery-automation

# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: Project structure and documentation"

# Add your GitHub repository (replace YOUR_REPO_URL)
git remote add origin YOUR_REPO_URL

# Push to GitHub
git push -u origin main
```

### 3. Set Up Python Environment (on Raspberry Pi)

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and pip if needed
sudo apt-get install python3-pip python3-venv -y

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Test the Basic Setup

```bash
# Activate virtual environment
source venv/bin/activate

# Run main (won't do much yet, but verifies setup)
python src/main.py

# Run test suite (shows what needs to be built)
python tests/hardware_test_suite.py
```

### 5. Start Building Hardware Modules

**We'll build these together in order:**
1. Load cell interface (`src/hardware/load_cell.py`)
2. Thermocouple interface (`src/hardware/thermocouple.py`)
3. Relay control (`src/hardware/relay.py`)
4. Pump control (`src/hardware/pump.py`)
5. Valve control (`src/hardware/valve.py`)
6. PID controller (`src/controllers/pid_controller.py`)
7. Heating controller (`src/controllers/heating_controller.py`)
8. Process sequences (`src/sequences/...`)
9. Safety monitor (`src/safety/safety_monitor.py`)
10. GUI (`src/gui/...`)

## Important Files to Review

1. **README.md** - Overall project description
2. **ARCHITECTURE.md** - How everything fits together
3. **docs/GIT_SETUP.md** - Git and GitHub instructions
4. **config/hardware_config.yaml** - Pin assignments (update as you wire things)
5. **docs/hardware_specs.md** - Shopping list and specs

## Collaboration

When your collaborator joins:
1. Add them to your GitHub repository
2. They run: `git clone YOUR_REPO_URL`
3. They follow step 3 above to set up Python environment
4. Ready to code together!

## Daily Workflow

```bash
# Before starting work
git pull

# Make changes to files...

# Commit and push
git add .
git commit -m "Description of what you did"
git push
```

## Questions or Issues?

- Check the documentation in `docs/`
- Review `ARCHITECTURE.md` for system design
- Look at `CHANGELOG.md` to see what's been done
- Create GitHub issues to track tasks

## What's Next?

Let's decide which hardware component to build first! 

I recommend starting with:
1. **Load cell** - Easy to test, fundamental for operation
2. **Thermocouple** - Important for safety
3. **Relay** - Needed to control everything else

Let me know what hardware you have on hand or what you'd like to start with!

---

**Created:** 2025-02-11  
**Team:** Distillery Automation Project  
**Status:** Initial Setup Complete ✓
