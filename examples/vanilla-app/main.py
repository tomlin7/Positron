from pathlib import Path

from positron import App, BrowserWindow
from positron.ipc import ipc_main

app = App()


@ipc_main.handle("greet")
def handle_greet(event, data):
    name = data.get("name", "World")
    return {"message": f"Hello from Python, {name}!"}


def create_window():
    # Create browser window
    win = BrowserWindow({"width": 800, "height": 600, "title": "Positron + Vanilla JS"})

    # Load local HTML file
    html_path = Path(__file__).parent / "index.html"
    win.load_url(f"file:///{html_path}")

    return win


if __name__ == "__main__":
    app.when_ready(create_window)
    app.run()
