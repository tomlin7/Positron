# Positron

**Build cross-platform desktop apps with React and Python**

Positron is an Electron-like framework that lets you create desktop applications using React for the UI and Python for the backend. It uses real browser engines (WebView2/WebKit) to render your React apps.

```python
from positron import App, BrowserWindow

app = App()

def create_window():
    win = BrowserWindow({'width': 800, 'height': 600})
    win.load_url('http://localhost:5173')  # Your Vite dev server

app.when_ready(create_window)
app.run()
```

## ✨ Features

- ✅ **Full React Support** - Modern React with hooks, ES modules, everything!
- ✅ **Real Browser Engine** - WebView2 (Windows), WebKit (macOS/Linux)
- ✅ **Python Backend** - Access to the entire Python ecosystem
- ✅ **IPC Communication** - Bidirectional messaging between React and Python
- ✅ **Electron-like API** - If you know Electron, you know Positron
- ✅ **Lightweight** - ~5-10MB vs Electron's ~150MB
- ✅ **Cross-Platform** - Windows, macOS, and Linux

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/positron.git
cd positron

# Install Python dependencies
pip install pywebview

# Try the example app
cd examples/react-app
npm install
python main.py
```

### Create Your First App

```python
from positron import App, BrowserWindow
from positron.ipc import ipc_main

app = App()

@ipc_main.handle('greet')
def greet(event, name):
    return f"Hello {name} from Python!"

def create_window():
    win = BrowserWindow({'width': 1000, 'height': 700})
    win.load_url('http://localhost:5173')

app.when_ready(create_window)
app.run()
```

**In React:**

```jsx
function App() {
  const handleClick = async () => {
    const msg = await window.ipcRenderer.invoke('greet', 'World')
    console.log(msg)  // "Hello World from Python!"
  }
  
  return <button onClick={handleClick}>Greet</button>
}
```

## 📦 What's Included

- **Modern Web Support**: HTML5, CSS3, ES6+ JavaScript
- **Full React**: Hooks, Context, Suspense - everything works!
- **Browser APIs**: Fetch, WebSockets, LocalStorage, etc.
- **Python Integration**: Use any Python library in your backend
- **Hot Reload**: Vite dev server with HMR
- **IPC Bridge**: Electron-compatible communication API

## 🆚 Comparison with Electron

| Feature | Electron | Positron |
|---------|----------|----------|
| Backend | Node.js | **Python** |
| Renderer | Chromium (bundled) | System WebView |
| React Support | ✅ | ✅ |
| Bundle Size | ~150MB | **~5-10MB** |
| Memory Usage | High | **Lower** |
| Python Ecosystem | ❌ | **✅** |

## 💻 Platform Support

- **Windows 10/11**: Microsoft Edge WebView2
- **macOS 10.14+**: System WebKit
- **Linux**: GTK WebKit

## 📚 Documentation

Visit our [documentation site](./docs) for:

- [Getting Started Guide](./docs/content/docs/getting-started.mdx)
- [Installation Instructions](./docs/content/docs/installation.mdx)
- [API Reference](./docs/content/docs/api)
- [Architecture Overview](./docs/content/docs/architecture.mdx)

## 🎯 Use Cases

Perfect for:

- **Data Science Dashboards** - Pandas/NumPy backend, React UI
- **ML Tools** - TensorFlow/PyTorch with modern interface
- **Automation** - Python scripts with beautiful GUI
- **Internal Tools** - Enterprise apps with Python + React
- **Desktop Apps** - Native-feeling apps with web tech

## 🛠️ Tech Stack

- **pywebview** - Cross-platform webview wrapper
- **Python 3.8+** - Backend runtime
- **React 18** - UI framework
- **Vite 5** - Build tool and dev server

## 📖 Examples

Check out the `examples/` directory:

- **react-app** - Full React app with Vite and IPC

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Credits

Built with:
- [pywebview](https://github.com/r0x0r/pywebview) - Cross-platform webview
- [React](https://react.dev/) - UI framework
- Inspired by [Electron](https://www.electronjs.org/)

---

**Made for Python and React developers** 🐍 ⚛️
