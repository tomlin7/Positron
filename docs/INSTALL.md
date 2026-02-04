# Positron Installation Guide

Complete installation instructions for Positron framework.

## Prerequisites

Before installing Positron, ensure you have:

- **Python 3.8+** (3.11+ recommended)
- **Node.js 16+** (18+ LTS recommended)
- **npm** or **yarn** package manager
- **Tkinter** (usually included with Python)

### Check Prerequisites

```bash
# Check Python version
python --version  # Should be 3.8 or higher

# Check Node.js version
node --version    # Should be 16 or higher

# Check npm
npm --version

# Test Tkinter installation
python -c "import tkinter; print('Tkinter OK')"
```

### Installing Tkinter (if needed)

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**Arch Linux:**
```bash
sudo pacman -S tk
```

**macOS/Windows:**
Tkinter is usually pre-installed with Python.

## Installation Steps

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/positron.git
cd positron
```

### Step 2: Install Python Dependencies

**Option A: Using requirements.txt (Recommended)**
```bash
pip install -r requirements.txt
```

This installs:
- TkinterWeb with **ALL** features ([full] installation)
- **PythonMonkey for JavaScript support (REQUIRED for React)**
- PIL for image support
- Brotli for compression
- CairoSVG for SVG support
- requests for HTTP support

**Option B: Direct Installation**
```bash
pip install tkinterweb[full]
```

Installs TkinterWeb with all features including JavaScript support.

**⚠️ Important:** The `[full]` installation is **required** for React apps because they need JavaScript support via PythonMonkey.

**Option C: Development Installation**
```bash
pip install -e .
```

Installs Positron in editable mode for development.

### Step 3: Verify Installation

```bash
python -c "from positron import App, BrowserWindow; from positron.ipc import ipc_main; print('✓ Positron installed successfully!')"
```

Expected output:
```
✓ Positron installed successfully!
```

## Running the Example App

### Step 1: Navigate to Example

```bash
cd examples/react-app
```

### Step 2: Install Node.js Dependencies

```bash
npm install
```

This installs:
- React and ReactDOM
- Vite and its plugins
- Development dependencies

### Step 3: Run the App

```bash
python main.py
```

You should see:
1. Dev server starting
2. Window opening with React app
3. Beautiful gradient UI

## Project Structure After Installation

```
positron/
├── positron/           # Installed Positron framework
├── examples/
│   └── react-app/
│       ├── node_modules/   # Created by npm install
│       └── ...
├── TkinterWeb/         # Reference only (not used)
└── ...
```

## Troubleshooting

### Problem: TkinterWeb not found

**Error:**
```
ImportError: No module named 'tkinterweb'
```

**Solution:**
```bash
pip install tkinterweb[full]
```

### Problem: JavaScript not working in React app

**Symptoms:**
- React app doesn't render
- Console shows JavaScript errors
- Blank page in window

**Solution:**
Make sure you installed the `[full]` version with JavaScript support:
```bash
pip install tkinterweb[full]
```

Verify PythonMonkey is installed:
```bash
python -c "import pythonmonkey; print('✓ JavaScript support available')"
```

### Problem: Tkinter not found

**Error:**
```
ModuleNotFoundError: No module named 'tkinter'
```

**Solution:**
Install Tkinter for your platform (see Prerequisites section).

### Problem: npm command not found

**Error:**
```
npm: command not found
```

**Solution:**
Install Node.js from https://nodejs.org/

### Problem: Dev server won't start

**Error:**
```
Error starting dev server
```

**Solutions:**
1. Make sure you ran `npm install` in the example directory
2. Check if port 5173 is available
3. Try a different port in `vite.config.js`

### Problem: Window shows but is blank

**Possible causes:**
1. Dev server didn't start properly
2. React build errors
3. Port mismatch

**Debug:**
```bash
# Check console for errors
# Dev server output shows in terminal

# Test with simple HTML
python -c "
from positron import App, BrowserWindow
app = App()
def test():
    win = BrowserWindow()
    win.load_html('<h1>Test</h1>')
app.when_ready(test)
app.run()
"
```

### Problem: Python path issues

If you get import errors when running examples:

**Solution 1:** Install in development mode
```bash
cd /path/to/positron
pip install -e .
```

**Solution 2:** Use the sys.path trick (already in examples)
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
```

## Virtual Environment (Recommended)

Use a virtual environment to avoid conflicts:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install Positron
pip install -r requirements.txt

# Later: Deactivate
deactivate
```

## Platform-Specific Notes

### Windows

- Use PowerShell or Command Prompt
- Paths use backslashes: `C:\Users\...`
- TkinterWeb fully supported on 64-bit Windows

### macOS

- Both Intel and Apple Silicon supported
- Use Terminal or iTerm2
- May need to install Python from python.org (not system Python)

### Linux

- Tkinter might need separate installation
- TkinterWeb binaries available for 64-bit Linux
- Use your distribution's package manager for dependencies

## Next Steps

After installation:

1. **Try the example:**
   ```bash
   cd examples/react-app
   npm install
   python main.py
   ```

2. **Read the docs:**
   - [README.md](README.md) - Full API reference
   - [QUICKSTART.md](QUICKSTART.md) - Quick start guide
   - [DEPENDENCIES.md](DEPENDENCIES.md) - Dependency details

3. **Create your app:**
   - Copy the example app as a template
   - Or start from scratch following QUICKSTART.md

## Updating

To update Positron and dependencies:

```bash
# Update Positron (pull latest changes)
cd /path/to/positron
git pull

# Update Python dependencies
pip install -r requirements.txt --upgrade

# Update Node.js dependencies (in example app)
cd examples/react-app
npm update
```

## Uninstalling

To uninstall Positron:

```bash
# Uninstall Python packages
pip uninstall tkinterweb

# Remove repository
cd ..
rm -rf positron
```

## Getting Help

If you encounter issues:

1. Check [DEPENDENCIES.md](DEPENDENCIES.md) for version requirements
2. Search [GitHub Issues](https://github.com/yourusername/positron/issues)
3. Create a new issue with:
   - Your OS and Python version
   - Full error message
   - Steps to reproduce

## Success!

If you see the example React app running in a native window, you've successfully installed Positron! 🎉

Now you're ready to build cross-platform desktop apps with Python and React.
