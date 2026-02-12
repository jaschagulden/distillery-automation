# Distillery Automation System

## Project Overview
This project automates a 200-liter distillery system using a Raspberry Pi 4B. The system controls the entire distillation process from mash transfer through distillate collection and cleanup, requiring minimal human intervention.

## System Capabilities
- Automated mash transfer from 1050L tank to 200L still (weight-based)
- PID-controlled heating with 2x 5.5kW electric elements
- Automated distillate collection with separation into heads, hearts, and tails
- Flow rate control via heating modulation
- Automated discharge and Clean-In-Place (CIP) system
- Multi-cycle operation capability

## Current Status
🟡 **In Development** - Initial project structure created

### Completed
- [x] Project structure and documentation framework
- [ ] Hardware interface modules
- [ ] Control logic implementation
- [ ] Sequence automation
- [ ] User interface
- [ ] Safety systems
- [ ] Testing and calibration

## Hardware Components

### Sensors
- 4x Load cells with amplifiers (mash tank, still, discharge tank, distillate collection)
- Multiple thermocouples (still, condenser, ambient)

### Actuators
- 2x 5.5kW heating elements (SSR controlled)
- Mash transfer pump
- Condenser cooling pump
- Discharge pump
- CIP pump
- Valves: mash inlet, heads, hearts, tails, discharge, CIP

### Controller
- Raspberry Pi 4B running Raspberry Pi OS

## Quick Start

### Prerequisites
```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python dependencies
sudo apt-get install python3-pip python3-venv -y

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Installation
```bash
# Clone the repository
git clone [your-repo-url]
cd distillery-automation

# Activate virtual environment
source venv/bin/activate

# Run hardware tests
python tests/hardware_test_suite.py
```

### Running the System
```bash
# Activate virtual environment
source venv/bin/activate

# Run main application
python src/main.py
```

## Configuration
- Hardware pin assignments: `config/hardware_config.yaml`
- Distillation recipes: `config/recipes/`
- Calibration data: `config/calibration/`

## Documentation
- [Architecture Overview](ARCHITECTURE.md)
- [Hardware Specifications](docs/hardware_specs.md)
- [Calibration Procedures](docs/calibration_procedures.md)
- [Operational Manual](docs/operational_manual.md)

## Safety
⚠️ **Important**: This system controls high-power heating elements and flammable distillates. Always:
- Test all safety interlocks before production use
- Monitor initial runs closely
- Ensure proper ventilation
- Have fire suppression equipment available
- Follow all local regulations and safety codes

## Contributing
This is a collaborative project. When adding features:
1. Create a new branch for your feature
2. Test thoroughly with hardware test scripts
3. Update documentation
4. Update CHANGELOG.md
5. Submit for review

## License
[Your chosen license]

## Team
- Project Lead: [Your name]
- Collaborators: [Team members]

## Changelog
See [CHANGELOG.md](CHANGELOG.md) for detailed version history.
