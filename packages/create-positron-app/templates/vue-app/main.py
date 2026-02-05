from pathlib import Path

from positron import App, BrowserWindow
from positron.ipc import ipc_main
from positron.renderer.dev_server import DevServer

app = App()


# IPC Handlers
@ipc_main.on("renderer-ready")
def handle_renderer_ready(event, message):
    print(f"Renderer ready: {message}")


@ipc_main.on("button-clicked")
def handle_button_click(event, count):
    print(f"Button clicked {count} times!")
    event.sender.send("message-from-main", f"Python received click count: {count}")


@ipc_main.handle("get-data")
def handle_get_data(event, message):
    print(f"Received from Vue: {message}")
    return f"Python says hello to Vue! You sent: {message}"


def create_window():
    # Start Vite dev server
    dev_server = DevServer(
        cwd=str(Path(__file__).parent), command="npm run dev", port=5173
    )

    try:
        dev_server.start()
    except Exception as e:
        print(f"Error starting dev server: {e}")
        return None, None

    # Create browser window
    win = BrowserWindow({"width": 1200, "height": 800, "title": "Positron + Vue"})

    win.load_url(dev_server.get_url())

    return win, dev_server


if __name__ == "__main__":
    app.when_ready(create_window)
    app.run()
