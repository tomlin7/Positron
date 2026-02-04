# Positron React Example App

This is an example application built with Positron, demonstrating how to create desktop apps using Python and React.

## Project Structure

```
react-app/
├── main.py              # Python main process (backend)
├── package.json         # Node.js dependencies
├── vite.config.js       # Vite configuration
├── index.html          # HTML entry point
└── src/
    ├── main.jsx        # React entry point
    ├── App.jsx         # Main React component
    ├── App.css         # App styles
    └── index.css       # Global styles
```

## Getting Started

### 1. Install Node.js Dependencies

```bash
cd examples/react-app
npm install
```

### 2. Install Python Dependencies

Make sure TkinterWeb is available:

```bash
pip install tkinterweb[recommended]
```

### 3. Run the App

```bash
python main.py
```

The app will:
1. Start a Vite dev server for React
2. Create a Positron window
3. Load the React app in the window

## Features Demonstrated

### IPC Communication

The example shows bidirectional communication between Python and React:

**From React to Python:**
```javascript
// Send one-way message
window.ipcRenderer.send('button-clicked', count)

// Send and wait for response
const result = await window.ipcRenderer.invoke('get-data', 'argument')
```

**From Python to React:**
```python
# Register handler
@ipc_main.handle('get-data')
def handle_get_data(event, arg):
    return f"Response: {arg}"

# Send message to renderer
event.reply('message-from-main', 'Hello from Python!')
```

### Window Management

```python
win = BrowserWindow({
    'width': 1000,
    'height': 700,
    'title': 'My App',
    'resizable': True,
})
```

### Dev Server Integration

```python
dev_server = DevServer(
    cwd=str(Path(__file__).parent),
    command='npm run dev',
    port=5173
)
dev_server.start()
win.load_url(dev_server.get_url())
```

## Building for Production

To build the React app for production:

```bash
npm run build
```

Then modify `main.py` to load the built files:

```python
# Instead of dev server
win.load_file('dist/index.html')
```

## Development

- Hot reload is enabled via Vite
- Edit `src/App.jsx` and see changes instantly
- Python changes require restarting the app

## Comparison to Electron

| Electron | Positron |
|----------|----------|
| Node.js backend | Python backend |
| Chromium renderer | TkinterWeb (Tkhtml3) renderer |
| `ipcMain`/`ipcRenderer` | Same API in Positron |
| `BrowserWindow` | Same API in Positron |
| `app.whenReady()` | Same API in Positron |

## Notes

- The renderer uses TkinterWeb which supports HTML 4.01 and CSS 2.1
- Modern React features work, but some advanced CSS may not be supported
- JavaScript support is partial (basic DOM manipulation works)
