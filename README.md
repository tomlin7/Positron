# POSITRON

**High-performance desktop applications with Python and React.**
No Node.js. Pure speed.

---

### CORE / INITIALIZE

```python
from positron import App, BrowserWindow, ipc_main

app = App()

@ipc_main.handle('core:compute')
def handle_compute(event, data):
    # Heavy Python logic here
    result = {"status": "success", "payload": data}
    return result

def init():
    win = BrowserWindow({
        'title': 'Positron App',
        'width': 1200,
        'height': 800,
        'frame': False
    })
    win.load_url('http://localhost:5173')

app.when_ready(init)
app.run()
```

---

### SPECS / ARCHITECTURE

- **Runtime**: Python 3.8+ / No Node.js dependency
- **Renderer**: OS Native WebView (WebView2 / WebKit)
- **UI**: React 18 / Vite 5
- **IPC**: Bidirectional bridge (Electron-compatible)
- **Size**: ~5-10MB (Native system renderer)
- **Support**: Windows / macOS / Linux

---

### STATUS / PIPELINE

**01. FINISHED**
- Core architecture
- Window management
- IPC communication
- React + Vite integration

**02. BUILDING**
- Documentation (75%)
- Examples (60%)

**03. PIPELINE**
- Menu API
- Dialog API
- System tray
- Auto-updater
- Build tools
- CLI scaffolding

---

### QUICK START

```bash
git clone https://github.com/tomlin7/positron.git
cd positron
pip install -r requirements.txt
cd examples/react-app
npm install
python main.py
```

---

### RESOURCES / LINKS

- **Documentation**: [positron.tomlin7.com](https://positron.tomlin7.com)
- **Source**: [github.com/tomlin7/positron](https://github.com/tomlin7/positron)
- **License**: MIT

---

© 2026 POSITRON CORE v0.1.0-ALPHA
