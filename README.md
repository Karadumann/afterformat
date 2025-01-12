# Program Installer

A modern and user-friendly program installation tool designed for Windows systems.

## Features

- 🚀 Multi-program download support
- 📦 Automatic installation launch
- 🔄 Download progress tracking
- 🌍 Turkish/English language support
- 📊 Detailed download status and speed indicators
- 🎯 Categorized program list
- 💫 Modern and user-friendly interface


## Installation

1. Download the latest release from the [Releases](https://github.com/yourusername/program-installer/releases) page
2. Run the downloaded `program_installer.exe` file
3. Select the programs you want to install and click the "Download" button

## Developer Notes

### Requirements
```
python >= 3.12
tkinter
requests
pillow
```

### Development Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Building
```bash
# Create executable with PyInstaller
pyinstaller program_installer.spec
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 