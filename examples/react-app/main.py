"""
Example Positron app with React
This demonstrates how to build a desktop app using Positron with React
"""

import sys
from pathlib import Path

# Add positron to path (for development when not installed via pip)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from positron import App, BrowserWindow
from positron.ipc import ipc_main
from positron.renderer import DevServer

# Create app instance
app = App()


# IPC Handlers - Communication between React and Python
@ipc_main.handle("get-data")
def handle_get_data(event, arg):
    """Handle data request from renderer"""
    print(f"Received data request with arg: {arg}")
    return f"Hello from Python! You sent: {arg}"


def on_renderer_ready(event, message):
    """Handle renderer ready event"""
    print(f"Renderer is ready! Message: {message}")
    # Send a message back to the renderer
    event.reply("message-from-main", "Welcome from Python main process!")


def on_button_clicked(event, count):
    """Handle button click from renderer"""
    print(f"Button clicked! Count: {count}")


# Register IPC handlers
ipc_main.on("renderer-ready", on_renderer_ready)
ipc_main.on("button-clicked", on_button_clicked)

# Debug: Print registered handlers
print(f"Registered IPC handlers: {list(ipc_main._handlers.keys())}")


def create_window():
    """Create the main application window"""
    # Start dev server first (in background)
    dev_server = DevServer(
        cwd=str(Path(__file__).parent), command="npm run dev", port=5173
    )

    try:
        dev_server.start()
    except Exception as e:
        print(f"Error starting dev server: {e}")
        print("Make sure to run 'npm install' first!")
        return None, None

    # Create browser window
    win = BrowserWindow(
        {
            "width": 1000,
            "height": 700,
            "title": "Positron React App",
            "resizable": True,
            "center": True,
            "webPreferences": {
                "contextIsolation": True,
            },
        }
    )

    # Load the dev server URL
    win.load_url(dev_server.get_url())

    # Handle window events
    def on_window_closed():
        print("Window closed")
        if dev_server:
            dev_server.stop()

    win.on("closed", on_window_closed)

    return win, dev_server


def main():
    """Main application entry point"""
    print("Starting Positron React App...")

    # Create window when app is ready
    window = None
    dev_server = None

    def on_ready():
        nonlocal window, dev_server
        try:
            result = create_window()
            if result is None or result == (None, None):
                print("Failed to create window, quitting...")
                app.quit()
                return
            window, dev_server = result
        except Exception as e:
            print(f"Error creating window: {e}")
            import traceback

            traceback.print_exc()
            app.quit()

    app.when_ready(on_ready)

    # Handle app quit
    def on_quit():
        print("Application quitting...")
        if dev_server:
            dev_server.stop()

    app.on("quit", on_quit)

    # Run the app
    app.run()


if __name__ == "__main__":
    main()
