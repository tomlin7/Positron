# Positron Quick Start Guide

Get up and running with Positron in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Installation

### 1. Clone/Download Positron

```bash
git clone https://github.com/yourusername/positron.git
cd positron
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or manually install TkinterWeb with full features (including JavaScript):
```bash
pip install tkinterweb[full]
```

**Note:** 
- The `[full]` extra includes JavaScript support via PythonMonkey, which is required for React apps
- The `TkinterWeb/` folder in the repo is for reference only. Positron uses the TkinterWeb package from pip.

## Run the Example App

```bash
# Navigate to the example app
cd examples/react-app

# Install Node.js dependencies
npm install

# Run the app
python main.py
```

You should see a window open with a beautiful React UI!

## Create Your Own App

### Method 1: Copy the Example

```bash
# Copy the example app
cp -r examples/react-app my-app
cd my-app

# Install dependencies
npm install

# Edit main.py and src/App.jsx
# Run your app
python main.py
```

### Method 2: Start From Scratch

**1. Create project directory:**
```bash
mkdir my-positron-app
cd my-positron-app
```

**2. Initialize React with Vite:**
```bash
npm create vite@latest . -- --template react
npm install
```

**3. Create main.py:**
```python
from positron import App, BrowserWindow
from positron.renderer import DevServer
from pathlib import Path
import sys

# Add positron to path
sys.path.insert(0, str(Path(__file__).parent.parent))

app = App()

def create_window():
    win = BrowserWindow({
        'width': 1000,
        'height': 700,
        'title': 'My App'
    })
    
    dev_server = DevServer(
        cwd=str(Path(__file__).parent),
        command='npm run dev',
        port=5173
    )
    dev_server.start()
    win.load_url(dev_server.get_url())

app.when_ready(create_window)
app.run()
```

**4. Run your app:**
```bash
python main.py
```

## Next Steps

### Add IPC Communication

**In main.py:**
```python
from positron.ipc import ipc_main

@ipc_main.handle('my-channel')
def handler(event, data):
    # Process data in Python
    return f"Processed: {data}"
```

**In React (src/App.jsx):**
```jsx
const result = await window.ipcRenderer.invoke('my-channel', 'hello')
console.log(result)  // "Processed: hello"
```

### Customize Window

```python
win = BrowserWindow({
    'width': 1200,
    'height': 800,
    'title': 'My Custom App',
    'resizable': True,
    'center': True,
    'backgroundColor': '#282c34',
    'min_width': 800,
    'min_height': 600,
})
```

### Access Python Libraries

Use any Python library in your IPC handlers:

```python
import requests
import pandas as pd
from PIL import Image

@ipc_main.handle('fetch-data')
def fetch_data(event, url):
    response = requests.get(url)
    return response.json()

@ipc_main.handle('process-csv')
def process_csv(event, filepath):
    df = pd.read_csv(filepath)
    return df.to_dict('records')
```

## Common Issues

### Dev Server Not Starting

**Problem:** `Error starting dev server`

**Solution:**
1. Make sure Node.js is installed: `node --version`
2. Install dependencies: `npm install`
3. Check if port 5173 is available

### TkinterWeb Not Found

**Problem:** `ImportError: tkinterweb`

**Solution:**
```bash
pip install tkinterweb[recommended]
```

### Window Not Showing

**Problem:** Window opens but is blank

**Solution:**
1. Check console for errors
2. Make sure dev server started successfully
3. Try loading a simple HTML: `win.load_html('<h1>Test</h1>')`

## Development Tips

### Hot Reload

React changes auto-reload thanks to Vite. Python changes require app restart.

### Debugging

**Python side:**
```python
import pdb; pdb.set_trace()  # Breakpoint
print("Debug:", data)  # Print to console
```

**JavaScript side:**
```javascript
console.log("Debug:", data)  // Shows in Python console
```

### Production Build

Build React for production:
```bash
npm run build
```

Then load built files instead of dev server:
```python
# In main.py
win.load_file('dist/index.html')
```

## Learn More

- [Full Documentation](README.md)
- [API Reference](README.md#api-reference)
- [Examples](examples/)

## Need Help?

- [GitHub Issues](https://github.com/yourusername/positron/issues)
- [Discussions](https://github.com/yourusername/positron/discussions)

Happy coding with Positron! 🚀
