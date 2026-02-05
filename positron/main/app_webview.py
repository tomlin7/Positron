"""
Main application class for Positron using pywebview
Similar to Electron's app module - manages application lifecycle
"""

import sys
from typing import Callable

import webview


class App:
    """
    Main application instance managing the app lifecycle.
    Singleton pattern - only one App instance per application.
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self.windows = []
        self._ready_callbacks = []
        self._window_all_closed_callbacks = []
        self._before_quit_callbacks = []
        self._quit_callbacks = []
        self._is_ready = False
        self._is_quitting = False
        self._webview_started = False

    def on(self, event: str, callback: Callable):
        """
        Register event listeners for app lifecycle events.

        Events:
            - 'ready': Emitted when app is ready to create windows
            - 'window-all-closed': Emitted when all windows are closed
            - 'before-quit': Emitted before app quits
            - 'quit': Emitted when app quits
        """
        event_map = {
            "ready": self._ready_callbacks,
            "window-all-closed": self._window_all_closed_callbacks,
            "before-quit": self._before_quit_callbacks,
            "quit": self._quit_callbacks,
        }

        if event in event_map:
            event_map[event].append(callback)
        else:
            raise ValueError(f"Unknown event: {event}")

    def when_ready(self, callback: Callable):
        """
        Execute callback when app is ready.
        Similar to Electron's app.whenReady()
        """
        if self._is_ready:
            callback()
        else:
            self._ready_callbacks.append(callback)

    def _emit_ready(self):
        """Internal: Emit ready event"""
        self._is_ready = True
        for callback in self._ready_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in ready callback: {e}", file=sys.stderr)

    def _emit_window_all_closed(self):
        """Internal: Emit window-all-closed event"""
        for callback in self._window_all_closed_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in window-all-closed callback: {e}", file=sys.stderr)

        # Default behavior: quit on all windows closed
        if not self._window_all_closed_callbacks:
            self.quit()

    def _emit_before_quit(self):
        """Internal: Emit before-quit event"""
        for callback in self._before_quit_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in before-quit callback: {e}", file=sys.stderr)

    def _emit_quit(self):
        """Internal: Emit quit event"""
        for callback in self._quit_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in quit callback: {e}", file=sys.stderr)

    def register_window(self, window):
        """Internal: Register a window with the app"""
        if window not in self.windows:
            self.windows.append(window)
            print(f"Registered window. Total windows: {len(self.windows)}")

    def unregister_window(self, window):
        """Internal: Unregister a window from the app"""
        if window in self.windows:
            self.windows.remove(window)
            print(f"Unregistered window. Remaining windows: {len(self.windows)}")

        if len(self.windows) == 0:
            print("All windows closed")
            self._emit_window_all_closed()

    def quit(self):
        """Quit the application"""
        if self._is_quitting:
            return

        print("App quitting...")
        self._is_quitting = True
        self._emit_before_quit()

        # Close all windows
        for window in self.windows[:]:
            window.close()

        self._emit_quit()

        # Exit the application
        try:
            # pywebview doesn't have a destroy method, just exit
            sys.exit(0)
        except Exception as e:
            print(f"[pywebview] {e}")

    def run(self):
        """
        Start the application main loop.
        This should be called after setting up all windows and event handlers.
        """
        print("Starting Positron app with pywebview...")

        # Emit ready event
        self._emit_ready()

        # Start pywebview event loop
        # pywebview.start() will block until all windows are closed
        try:
            if len(self.windows) > 0:
                self._webview_started = True
                print(f"Starting webview with {len(self.windows)} window(s)")
                webview.start(debug=True)
            else:
                print("Warning: No windows created before app.run()")
        except KeyboardInterrupt:
            self.quit()
        except Exception as e:
            print(f"Error in webview loop: {e}", file=sys.stderr)
            self.quit()

    def get_name(self) -> str:
        """Get application name"""
        return getattr(sys.modules["__main__"], "__name__", "Positron App")

    def get_version(self) -> str:
        """Get application version"""
        return getattr(sys.modules["__main__"], "__version__", "0.1.0")


# Singleton instance
app = App()
