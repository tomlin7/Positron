"""
BrowserWindow class for Positron using pywebview
Provides actual React/modern web app support via WebView2/WebKit
"""

import sys
import threading
from pathlib import Path
from typing import Any, Callable, Dict, Optional

import webview

from ..ipc.main_webview import ipc_main
from ..ipc.renderer_webview import ipc_renderer
from .app_webview import app


class BrowserWindow:
    """
    Create and control browser windows using pywebview.
    Each window contains a real web browser engine (WebView2 on Windows).
    """

    # Track all windows
    _windows = []
    _webview_started = False

    def __init__(self, options: Optional[Dict[str, Any]] = None):
        """
        Create a new BrowserWindow.

        Args:
            options: Window configuration options
                - width (int): Window width in pixels (default: 800)
                - height (int): Window height in pixels (default: 600)
                - title (str): Window title (default: "Positron")
                - resizable (bool): Whether window is resizable (default: True)
                - frameless (bool): Frameless window (default: False)
                - fullscreen (bool): Start in fullscreen (default: False)
                - min_width (int): Minimum window width
                - min_height (int): Minimum window height
                - backgroundColor (str): Background color (default: "#FFFFFF")
                - show (bool): Show window immediately (default: True)
                - center (bool): Center window on screen (default: True)
                - webPreferences (dict): Web preferences (for compatibility)
        """
        options = options or {}

        # Window properties
        self._is_closed = False
        self._closed_callbacks = []
        self._dom_ready_callbacks = []
        self._url = None
        self._html_content = None

        # Extract options
        width = options.get("width", 800)
        height = options.get("height", 600)
        title = options.get("title", "Positron")
        resizable = options.get("resizable", True)
        frameless = options.get("frameless", False)
        fullscreen = options.get("fullscreen", False)
        min_size = (options.get("min_width", 200), options.get("min_height", 100))
        background_color = options.get("backgroundColor", "#FFFFFF")
        hidden = not options.get("show", True)

        # We need to create the window first to get a reference, then set up API
        # Create a placeholder - we'll set up IPC after window creation
        self.window = None

        # Create a temporary window to get reference
        temp_window = webview.create_window(
            title=title,
            url="about:blank",  # Start with blank page
            width=width,
            height=height,
            resizable=resizable,
            fullscreen=fullscreen,
            min_size=min_size,
            background_color=background_color,
            frameless=frameless,
            hidden=hidden,
        )

        # Now get the API with the window reference and expose it
        self.window = temp_window
        js_api = ipc_main.get_js_api(self.window)

        # Expose the API methods individually
        for method_name in ["ipc_send", "ipc_invoke"]:
            if hasattr(js_api, method_name):
                self.window.expose(getattr(js_api, method_name))

        # Set up event handlers
        self.window.events.closed += self._on_closed

        # Register window
        BrowserWindow._windows.append(self)
        app.register_window(self)

        print(f"Created BrowserWindow: {title} ({width}x{height})")

    def load_url(self, url: str):
        """
        Load a URL in the window.

        Args:
            url: URL to load (http://, https://, or file://)
        """
        print(f"Loading URL: {url}")
        self._url = url

        if self.window:
            # Inject IPC script after page loads
            def inject_ipc():
                try:
                    ipc_script = ipc_renderer.get_preload_script()
                    # Inject the IPC script
                    self.window.evaluate_js(ipc_script)
                    print("IPC script injected")

                    # Force initialization attempt
                    self.window.evaluate_js(
                        "if (typeof initPositronIPC === 'function') initPositronIPC();"
                    )
                except Exception as e:
                    print(f"Warning: Failed to inject IPC script: {e}")

            # Use loaded event to inject script
            self.window.events.loaded += inject_ipc

            # Load URL when window is shown (after webview.start())
            def load_when_shown():
                print(f"Window shown, now loading: {url}")
                self.window.load_url(url)

            self.window.events.shown += load_when_shown

    def load_file(self, file_path: str):
        """
        Load an HTML file in the window.

        Args:
            file_path: Path to HTML file
        """
        file_path = Path(file_path).resolve()
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        print(f"Loading file: {file_path}")

        # Convert to file:// URL and use load_url instead
        # This preserves relative paths and allows proper loading
        file_url = file_path.as_uri()
        self.load_url(file_url)

    def load_html(self, html: str, base_url: str = ""):
        """
        Load HTML content directly.

        Args:
            html: HTML content to load
            base_url: Base URL for resolving relative paths (optional)
        """
        print(f"Loading HTML content (base_url: {base_url})")

        # Inject IPC renderer script
        html = self._inject_ipc_script(html)

        self._html_content = html
        self.window.load_html(html)

    def _inject_ipc_script(self, html: str) -> str:
        """Internal: Inject IPC renderer script into HTML"""
        ipc_script = ipc_renderer.get_preload_script()

        # Inject script before </head> or at the beginning
        if "</head>" in html:
            script_tag = f"<script>{ipc_script}</script>"
            html = html.replace("</head>", f"{script_tag}</head>", 1)
        elif "<head>" in html:
            script_tag = f"<script>{ipc_script}</script>"
            html = html.replace("<head>", f"<head>{script_tag}", 1)
        else:
            # No head tag, create one
            script_tag = f"<html><head><script>{ipc_script}</script></head><body>"
            if "<html>" in html:
                html = html.replace("<html>", script_tag, 1)
                if "</html>" not in html:
                    html += "</body></html>"
            else:
                html = script_tag + html + "</body></html>"

        return html

    def _on_closed(self):
        """Internal: Handle window close event"""
        if self._is_closed:
            return

        self._is_closed = True
        print(f"Window closed: {self.window.title}")

        # Emit closed event
        for callback in self._closed_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in closed callback: {e}", file=sys.stderr)

        # Unregister from app
        if self in BrowserWindow._windows:
            BrowserWindow._windows.remove(self)
        app.unregister_window(self)

    def on(self, event: str, callback: Callable):
        """
        Register event listener.

        Events:
            - 'closed': Window has been closed
            - 'dom-ready': DOM is loaded and ready (placeholder for compatibility)
        """
        if event == "closed":
            self._closed_callbacks.append(callback)
        elif event == "dom-ready":
            self._dom_ready_callbacks.append(callback)
        else:
            print(f"Warning: Unknown event '{event}' (ignored)", file=sys.stderr)

    def show(self):
        """Show the window"""
        if self.window:
            self.window.show()

    def hide(self):
        """Hide the window"""
        if self.window:
            self.window.hide()

    def close(self):
        """Close the window"""
        if not self._is_closed and self.window:
            self.window.destroy()

    def set_title(self, title: str):
        """Set window title"""
        if self.window:
            self.window.title = title

    def get_title(self) -> str:
        """Get window title"""
        return self.window.title if self.window else ""

    def maximize(self):
        """Maximize the window"""
        if self.window:
            self.window.maximize()

    def minimize(self):
        """Minimize the window"""
        if self.window:
            self.window.minimize()

    def set_size(self, width: int, height: int):
        """Set window size"""
        if self.window:
            self.window.resize(width, height)

    def get_size(self) -> tuple:
        """Get window size as (width, height)"""
        if self.window:
            return (self.window.width, self.window.height)
        return (0, 0)

    def center(self):
        """Center the window on screen"""
        # pywebview doesn't have a built-in center method
        # This is handled by the 'center' option in constructor
        pass

    def evaluate_js(self, script: str):
        """
        Evaluate JavaScript in the window.

        Args:
            script: JavaScript code to execute

        Returns:
            Result of the JavaScript execution
        """
        if self.window:
            return self.window.evaluate_js(script)
        return None
