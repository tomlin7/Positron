# POSITRON

**High-performance desktop applications with Python and modern web frameworks.** Fast by design. Minimal by choice.

React • Vue • Svelte • Next.js • Vanilla JS


---

### QUICK START

```bash
npx create-positron-app@latest
```

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

- **Runtime**: Python 3.9+ / No Node.js dependency
- **Renderer**: OS Native WebView (WebView2 / WebKit)
- **UI**: React • Vue • Svelte • Next.js • Vanilla JS
- **Build Tools**: Vite / Next.js / Webpack
- **IPC**: Bidirectional bridge (Electron-compatible)
- **Size**: ~5-10MB (Native system renderer)
- **Support**: Windows / macOS / Linux

---

### STATUS / PIPELINE

**01. FINISHED**
- Core architecture
- Window management
- IPC communication
- Multi-framework support (React, Vue, Svelte, Next.js, Vanilla JS)
- Dev server integration (Vite, Next.js, Webpack)
- CLI scaffolding

**02. BUILDING**
- Documentation (80%)
- Additional examples

**03. PIPELINE**
- Menu API
- Dialog API
- System tray
- Auto-updater
- Build tools

---

### FRAMEWORK EXAMPLES

Positron includes complete examples for multiple frameworks:

- **React** - `examples/react-app` - Vite + React 18
- **Next.js** - `examples/nextjs-app` - Next.js 16 with SSR
- **Vue** - `examples/vue-app` - Vue 3 + Vite
- **Svelte** - `examples/svelte-app` - Svelte 5 + Vite
- **Vanilla** - `examples/vanilla-app` - Pure HTML/CSS/JS

All examples feature the same dark minimalist UI and full IPC support.

---

### RESOURCES / LINKS

- **Documentation**: [positron.tomlin7.com](https://positron.tomlin7.com)
- **Source**: [github.com/tomlin7/positron](https://github.com/tomlin7/positron)
- **License**: MIT

---

POSITRON CORE ALPHA

© 2026 POSITRON DEVELOPERS
