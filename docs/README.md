# Positron

**Build cross-platform desktop apps with React and Python**

Positron is an Electron-like framework that lets you create desktop applications using React for the UI and Python for the backend. It uses TkinterWeb to render your React apps in native windows.

```python
from positron import App, BrowserWindow

app = App()

def create_window():
    win = BrowserWindow({'width': 800, 'height': 600})
    win.load_url('http://localhost:5173')

app.when_ready(create_window)
app.run()
```

## Features

- **Familiar API**: If you know Electron, you know Positron
- **React Support**: Full support for modern React with Vite
- **Python Backend**: Access to the entire Python ecosystem
- **IPC Communication**: Bidirectional messaging between React and Python
- **Native Windows**: Real native window management with Tkinter
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Why Positron?

**Use Python Instead of Node.js**
- Leverage Python's rich ecosystem (AI/ML, data science, automation)
- Write backend logic in Python instead of JavaScript
- Access native system APIs through Python

**Electron-like Developer Experience**
- Same API structure as Electron
- Hot reload during development
- Familiar project structure

**Lightweight Alternative**
- Uses TkinterWeb instead of Chromium
- Smaller bundle sizes
- Lower memory footprint

## Quick Start

### Installation

#### Option 1: Install from source (recommended for now)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/positron.git
cd positron
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install TkinterWeb directly with full features (including JavaScript):
```bash
pip install tkinterweb[full]
```

3. Try the example app:
```bash
cd examples/react-app
npm install
python main.py
```

#### Option 2: Install as package (future)

Once published to PyPI:
```bash
pip install positron-framework
```

### Note on TkinterWeb Folder

The `TkinterWeb/` folder in this repository is for reference only. Positron uses the TkinterWeb package installed via pip, not this local folder.

### Create Your First App

**1. Project Structure** (similar to Electron)
```
my-app/
├── main.py              # Python main process
├── package.json         # Node.js dependencies
├── vite.config.js       # Vite config
├── index.html
└── src/
    ├── main.jsx
    └── App.jsx
```

**2. Main Process (main.py)**
```python
from positron import App, BrowserWindow
from positron.ipc import ipc_main
from positron.renderer import DevServer
from pathlib import Path

app = App()

def create_window():
    win = BrowserWindow({
        'width': 1000,
        'height': 700,
        'title': 'My Positron App'
    })
    
    # Development mode with Vite
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

**3. React App (src/App.jsx)**
```jsx
import { useState } from 'react'

function App() {
  const [message, setMessage] = useState('')
  
  const handleClick = async () => {
    // Call Python backend
    const result = await window.ipcRenderer.invoke('get-data', 'hello')
    setMessage(result)
  }
  
  return (
    <div>
      <h1>My Positron App</h1>
      <button onClick={handleClick}>Call Python</button>
      <p>{message}</p>
    </div>
  )
}

export default App
```

**4. IPC Handler (main.py)**
```python
@ipc_main.handle('get-data')
def handle_get_data(event, arg):
    return f"Python received: {arg}"
```

## API Reference

### Main Process

#### App

```python
from positron import App

app = App()

# Lifecycle events
app.on('ready', callback)
app.on('window-all-closed', callback)
app.on('before-quit', callback)
app.on('quit', callback)

# Run the app
app.when_ready(create_window)
app.run()

# Quit
app.quit()
```

#### BrowserWindow

```python
from positron import BrowserWindow

win = BrowserWindow({
    'width': 800,
    'height': 600,
    'title': 'My App',
    'resizable': True,
    'center': True,
    'backgroundColor': '#FFFFFF',
    'webPreferences': {
        'contextIsolation': True,
        'preload': 'path/to/preload.js'
    }
})

# Load content
win.load_url('http://localhost:5173')
win.load_file('index.html')
win.load_html('<h1>Hello</h1>')

# Window controls
win.show()
win.hide()
win.close()
win.maximize()
win.minimize()
win.center()

# Window properties
win.set_title('New Title')
win.set_size(1024, 768)
size = win.get_size()  # (width, height)

# Events
win.on('closed', callback)
win.on('ready-to-show', callback)
win.on('dom-ready', callback)
```

#### IPC Main

```python
from positron.ipc import ipc_main

# Listen for messages
@ipc_main.on('channel-name')
def handler(event, *args):
    print(f"Received: {args}")
    event.reply('reply-channel', 'response')

# Handle invoke (promise-based)
@ipc_main.handle('get-data')
def handler(event, arg):
    return "some data"

# One-time listener
ipc_main.once('channel', handler)

# Remove listeners
ipc_main.remove_listener('channel')
ipc_main.remove_all_listeners()
```

### Renderer Process (JavaScript)

```javascript
// Available in all pages
const { ipcRenderer } = window

// Send one-way message
ipcRenderer.send('channel', arg1, arg2)

// Send and wait for response (promise)
const result = await ipcRenderer.invoke('channel', arg)

// Listen for messages
ipcRenderer.on('channel', (event, ...args) => {
  console.log('Received:', args)
})

// One-time listener
ipcRenderer.once('channel', callback)

// Remove listeners
ipcRenderer.removeListener('channel', callback)
ipcRenderer.removeAllListeners('channel')
```

### Dev Server

```python
from positron.renderer import DevServer

dev_server = DevServer(
    cwd='path/to/react/app',
    command='npm run dev',
    port=5173,
    host='localhost',
    wait_timeout=30
)

dev_server.start()
url = dev_server.get_url()
dev_server.stop()

# Context manager
with DevServer(cwd='.', command='npm run dev') as server:
    win.load_url(server.get_url())
```

## Architecture

Positron follows Electron's process model:

```
┌─────────────────────────────────────┐
│       Main Process (Python)         │
│  - App lifecycle management         │
│  - Window creation                  │
│  - IPC handlers                     │
│  - System access                    │
└─────────────┬───────────────────────┘
              │
              │ IPC
              │
┌─────────────▼───────────────────────┐
│   Renderer Process (TkinterWeb)     │
│  - React UI rendering               │
│  - HTML/CSS/JavaScript              │
│  - IPC communication                │
└─────────────────────────────────────┘
```

**Main Process (Python)**
- Manages application lifecycle
- Creates and controls BrowserWindows
- Handles IPC from renderer
- Full access to Python libraries and system APIs

**Renderer Process (TkinterWeb)**
- Renders your React application
- Displays HTML, CSS, and executes JavaScript
- Sends IPC messages to main process
- Isolated from main process for security

## Comparison with Electron

| Feature | Electron | Positron |
|---------|----------|----------|
| Backend Language | Node.js | Python |
| Renderer | Chromium | TkinterWeb (Tkhtml3) |
| HTML/CSS Support | HTML5, CSS3 | HTML 4.01, CSS 2.1 |
| JavaScript | Full V8 | Partial (basic DOM) |
| IPC API | ✅ Same | ✅ Same |
| Window API | ✅ Same | ✅ Same |
| App Lifecycle | ✅ Same | ✅ Same |
| Bundle Size | Large (~150MB) | Small (~10MB) |
| Memory Usage | High | Low |

## Supported Technologies

**Frontend**
- ✅ React (with Vite or Webpack)
- ✅ HTML 4.01
- ✅ CSS 2.1 (+ border-radius on 64-bit)
- ✅ JavaScript (via PythonMonkey - included with [full] installation)
- ✅ Images (PNG, JPG, SVG)

**Backend (Python)**
- ✅ Any Python library
- ✅ Machine Learning (TensorFlow, PyTorch)
- ✅ Data Science (NumPy, Pandas)
- ✅ Web Scraping (Requests, BeautifulSoup)
- ✅ Automation (Selenium, PyAutoGUI)
- ✅ Database (SQLite, PostgreSQL, MongoDB)

## JavaScript Support

Positron includes full JavaScript support via PythonMonkey (included with `[full]` installation).

- ✅ React and modern JavaScript (ES6+)
- ✅ DOM manipulation and event handling
- ✅ Component lifecycle and hooks
- ✅ Console logging to terminal

**For details, see [JAVASCRIPT.md](JAVASCRIPT.md)**

## Examples

Check out the `examples/` directory:

- **react-app**: Full React app with Vite and IPC
- More examples coming soon!

## Roadmap

- [x] Core architecture (Main + Renderer processes)
- [x] BrowserWindow API
- [x] App lifecycle management
- [x] IPC communication
- [x] React/Vite integration
- [ ] Menu API
- [ ] Dialog API
- [ ] Tray API
- [ ] Notifications
- [ ] Auto-updater
- [ ] Application packaging
- [ ] More examples

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Credits

Built on top of:
- [TkinterWeb](https://github.com/Andereoo/TkinterWeb) - HTML rendering widget
- [Tkhtml3](http://tkhtml.tcl.tk/) - HTML/CSS engine
- Inspired by [Electron](https://www.electronjs.org/)

## Documentation

- **[README.md](README.md)** - This file, full API reference
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[INSTALL.md](INSTALL.md)** - Detailed installation instructions
- **[DEPENDENCIES.md](DEPENDENCIES.md)** - Dependency information
- **[JAVASCRIPT.md](JAVASCRIPT.md)** - JavaScript support details
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Technical architecture

## Support

- Report issues: [GitHub Issues](https://github.com/yourusername/positron/issues)
- Documentation: [Wiki](https://github.com/yourusername/positron/wiki)

---

**Made with ❤️ for Python and React developers**
