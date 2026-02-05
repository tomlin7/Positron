# Positron React Example App

This is a **full React application** built with Positron, demonstrating how to create desktop apps using Python and React.

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

Make sure pywebview is installed:

```bash
pip install pywebview
```

### 3. Run the App

```bash
python main.py
```

The app will:
1. Start a Vite dev server for React
2. Create a Positron window with **real browser engine**
3. Load the React app in the window

## ✨ Full React Support

This is a **real React application** with:

✅ **Modern React** - hooks, context, everything!  
✅ **ES6+ JavaScript** - modules, async/await, all modern features  
✅ **Hot Module Replacement** - changes appear instantly  
✅ **Vite dev server** - fast builds and updates  
✅ **Real browser engine** - WebView2 (Windows), WebKit (macOS/Linux)  
✅ **Full CSS3** - Grid, Flexbox, animations  
✅ **IPC communication** - Python ↔ React  
✅ **All browser APIs** - Fetch, WebSockets, LocalStorage  

## Features Demonstrated

### IPC Communication

Bidirectional communication between Python and React:

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

Build the React app for production:

```bash
npm run build
```

Then modify `main.py` to load the built files:

```python
# Instead of dev server
win.load_file('dist/index.html')
```

## Development

- ✅ **Hot reload enabled** - changes appear instantly!
- ✅ **Edit `src/App.jsx`** - see updates in real-time
- ✅ **React DevTools** may work (platform-dependent)
- Python changes require restarting the app

## Comparison to Electron

| Feature | Electron | Positron |
|---------|----------|----------|
| Backend | Node.js | **Python** |
| Renderer | Chromium (bundled) | **System WebView** |
| React Support | ✅ | ✅ |
| Modern JS | ✅ | ✅ |
| `ipcMain`/`ipcRenderer` | ✅ | ✅ **Same API** |
| `BrowserWindow` | ✅ | ✅ **Same API** |
| Bundle Size | ~150MB | **~5-10MB** |

## Platform Support

### Windows
- **Microsoft Edge WebView2** (Chromium-based)
- Usually pre-installed on Windows 10/11
- Full modern web support

### macOS
- **System WebKit**
- Built into macOS
- Native performance

### Linux
- **GTK WebKit2**
- Install: `sudo apt-get install python3-gi gir1.2-webkit2-4.0`
- Full compatibility

## Troubleshooting

### React app shows blank screen

1. Check dev server is running (see terminal output)
2. Try: `npm run dev` separately to verify Vite starts
3. Check port 5173 isn't blocked by firewall

### Import errors

```bash
# Install pywebview
pip install pywebview

# Linux: Install system dependencies
sudo apt-get install python3-gi gir1.2-webkit2-4.0
```

### WebView2 missing (Windows)

If you get WebView2 errors on Windows:
- Download: https://developer.microsoft.com/microsoft-edge/webview2/
- Usually pre-installed on Windows 10/11

## Learn More

- [Main Documentation](../../docs)
- [API Reference](../../docs/content/docs/api)
- [Architecture Guide](../../docs/content/docs/architecture.mdx)
