from pathlib import Path

from positron import App, BrowserWindow
from positron.renderer.dev_server import DevServer

app = App()


def create_window():
    # Start Vite dev server
    dev_server = DevServer(
        cwd=str(Path(__file__).parent), command="bun run dev", port=5173
    )

    try:
        dev_server.start()
    except Exception as e:
        print(f"Error starting dev server: {e}")
        return None, None

    # Create browser window
    win = BrowserWindow({"width": 1200, "height": 800, "title": "Positron + Svelte"})

    win.load_url(dev_server.get_url())

    return win, dev_server


if __name__ == "__main__":
    app.when_ready(create_window)
    app.run()
