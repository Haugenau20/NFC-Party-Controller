# Initial Prompt for Claude Code

Hi Claude Code! I'm working on an exciting home automation project and need your help structuring and coding it properly for my portfolio.

## Context

Please read the `PROJECT.md` file in this directory - it contains the complete project overview, technical stack, current state, and architecture decisions.

**Quick summary**: I'm building an NFC-based party controller using ESP32, ESPHome, Home Assistant, and Bang & Olufsen speakers. Physical cards will trigger music, lighting, and coordinated home automation experiences.

## Current Situation

- ✅ ESPHome CLI installed locally
- ✅ ESP32 hardware configured (buttons, potentiometer, buzzer, NFC reader)
- ✅ Home Assistant running with B&O speakers integrated
- ✅ SSH access to Home Assistant configured
- ⏳ Need to structure this as a proper Git repository
- ⏳ Need to copy existing configs from Home Assistant
- ⏳ Waiting for printer toner to print physical NFC cards

## What I Need Help With

### 1. Repository Structure Setup
Help me create the proper folder structure as outlined in PROJECT.md:
```
nfc-party-controller/
├── README.md
├── PROJECT.md
├── LICENSE
├── .gitignore
├── hardware/
├── esphome/
├── home-assistant/
├── cards/
└── docs/
```

### 2. Essential Files First
I need these created with appropriate content:
- `.gitignore` - What should be excluded for ESPHome + Home Assistant
- `LICENSE` - MIT license
- `README.md` - Compelling portfolio-ready documentation
- `esphome/secrets.yaml.example` - Template for credentials
- `home-assistant/configuration.yaml.example` - Package configuration example

### 3. ESPHome Configuration
Help me create a clean, well-documented `esphome/nfc_controller.yaml` with:
- PN532 NFC reader (I2C) with event-based tag handling
- Existing components: buttons, potentiometer, buzzer (GPIO23 with note about 5V MOSFET circuit)
- Proper substitutions and comments
- Reference to secrets.yaml for WiFi credentials

### 4. Home Assistant Package Structure
Set up the packages system with initial templates for:
- `packages/nfc_tags.yaml` - Event handling framework
- `packages/party_mode.yaml` - Input helpers and party mode logic
- `packages/audio_control.yaml` - B&O speaker automation templates
- Package loading in configuration.yaml

### 5. Documentation Templates
Create the documentation structure:
- `docs/SETUP.md` - Step-by-step setup guide
- `docs/ARCHITECTURE.md` - System design explanation
- `hardware/README.md` - Hardware documentation guide
- `cards/tag_mapping.csv` - Template CSV for 100 tags

## My Technical Preferences

- **Clean, commented code** - This is for my portfolio
- **Modular design** - Each file should have a clear, single purpose
- **Best practices** - Show proper Git workflow, YAML structure, etc.
- **Documentation-first** - Assume someone else will try to reproduce this
- **Event-driven** - NFC tags send events, Home Assistant maps them to actions

## Development Environment

- **ESPHome**: Installed locally, will compile/upload via CLI
- **Home Assistant**: Remote access via SSH (homeassistant.local:22222)
- **Editor**: VSCode with Remote-SSH extension
- **OS**: [your OS - Linux/Mac/Windows]

## First Tasks

Can you help me with these in order:

1. **Create complete repository structure** with all folders
2. **Generate `.gitignore`** appropriate for this project
3. **Create skeleton ESPHome YAML** with my hardware configuration
4. **Set up Home Assistant packages** structure with initial examples
5. **Write compelling README.md** for my portfolio
6. **Create tag mapping CSV template** for 100 NFC tags
7. **Document the architecture** decisions from PROJECT.md

## Style Guide

- YAML: 2-space indentation, comments explaining non-obvious config
- Markdown: Use headers properly, include code examples
- Commits: Descriptive messages in present tense ("Add NFC configuration")
- Comments: Explain *why*, not just *what*

## Questions for You

As we work through this:
- Are there better ways to structure anything?
- Am I missing important files or documentation?
- Any security concerns I should address?
- Suggestions for making this more portfolio-worthy?

Let's build something impressive! 🚀

---

**Note**: I have the current ESPHome config and Home Assistant setup running already - I just need help extracting it into a clean, version-controlled repository structure. Some configs are in the HA web interface right now.