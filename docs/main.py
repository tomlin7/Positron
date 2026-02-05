"""
Positron Documentation Desktop App
Wraps the Next.js docs in a desktop window
"""

import subprocess
import sys
import time
from pathlib import Path

# Add positron to path (parent directory)
sys.path.insert(0, str(Path(__file__).parent.parent))

from positron import App, BrowserWindow

app = App()

# Track the Next.js dev server process
dev_server = None


def start_next_server():
    """Start the Next.js development server"""
    global dev_server

    docs_dir = Path(__file__).parent
    print(f"Starting Next.js dev server in: {docs_dir}")

    try:
        dev_server = subprocess.Popen(
            ["bun", "run", "dev"],
            cwd=str(docs_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )

        # Wait for server to be ready
        print("Waiting for Next.js server to start...")
        time.sleep(3)

        print("Next.js dev server is ready at http://localhost:3000")
        return True

    except Exception as e:
        print(f"Error starting Next.js server: {e}")
        return False


def create_window():
    """Create the documentation window"""
    win = BrowserWindow(
        {
            "width": 1200,
            "height": 800,
            "title": "Positron Documentation",
            "resizable": True,
            "center": True,
        }
    )

    # Load the Next.js app
    win.load_url("http://localhost:3000")

    # Handle window close
    def on_closed():
        print("Window closed")
        if dev_server:
            print("Stopping Next.js dev server...")
            dev_server.terminate()
            try:
                dev_server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                dev_server.kill()

    win.on("closed", on_closed)

    return win


def main():
    """Main application entry point"""
    print("Starting Positron Documentation App...")

    # Start Next.js server first
    if not start_next_server():
        print("Failed to start Next.js server. Exiting...")
        return

    window = None

    def on_ready():
        nonlocal window
        try:
            window = create_window()
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
            print("Stopping Next.js dev server...")
            dev_server.terminate()
            try:
                dev_server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                dev_server.kill()

    app.on("quit", on_quit)

    # Run the app
    app.run()


if __name__ == "__main__":
    main()
