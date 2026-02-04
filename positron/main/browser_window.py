"""
BrowserWindow class for Positron
Similar to Electron's BrowserWindow - creates and manages application windows
"""

import os
import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from typing import Any, Callable, Dict, Optional

# Import TkinterWeb
try:
    from tkinterweb import HtmlFrame
except ImportError:
    raise ImportError(
        "TkinterWeb is required. Please install it with: pip install tkinterweb[recommended]"
    )

from ..ipc.renderer import ipc_renderer
from .app import app


class BrowserWindow:
    """
    Create and control browser windows.
    Each window contains a TkinterWeb HtmlFrame for rendering HTML/CSS/React apps.
    """

    def __init__(self, options: Optional[Dict[str, Any]] = None):
        """
        Create a new BrowserWindow.

        Args:
            options: Window configuration options
                - width (int): Window width in pixels (default: 800)
                - height (int): Window height in pixels (default: 600)
                - title (str): Window title (default: "Positron")
                - resizable (bool): Whether window is resizable (default: True)
                - frame (bool): Whether to show window frame (default: True)
                - show (bool): Whether to show window on creation (default: True)
                - center (bool): Whether to center window on screen (default: True)
                - min_width (int): Minimum window width
                - min_height (int): Minimum window height
                - max_width (int): Maximum window width
                - max_height (int): Maximum window height
                - backgroundColor (str): Background color (default: "#FFFFFF")
                - webPreferences (dict): Web preferences
                    - nodeIntegration (bool): Enable Node.js integration (not applicable)
                    - contextIsolation (bool): Enable context isolation (default: True)
                    - preload (str): Path to preload script
        """
        options = options or {}

        # Create Tk window
        self.window = tk.Toplevel(app.root) if app.root else tk.Tk()
        if not app.root:
            app.root = self.window

        # Window properties
        self._is_closed = False
        self._ready_callbacks = []
        self._closed_callbacks = []
        self._dom_ready_callbacks = []

        # Configure window
        width = options.get("width", 800)
        height = options.get("height", 600)
        title = options.get("title", "Positron")
        resizable = options.get("resizable", True)
        show = options.get("show", True)
        center = options.get("center", True)
        bg_color = options.get("backgroundColor", "#FFFFFF")

        self.window.title(title)
        self.window.geometry(f"{width}x{height}")
        self.window.resizable(resizable, resizable)

        # Set minimum/maximum sizes
        if "min_width" in options or "min_height" in options:
            min_w = options.get("min_width", 0)
            min_h = options.get("min_height", 0)
            self.window.minsize(min_w, min_h)

        if "max_width" in options or "max_height" in options:
            max_w = options.get("max_width", 0)
            max_h = options.get("max_height", 0)
            if max_w > 0 or max_h > 0:
                self.window.maxsize(max_w, max_h)

        # Center window
        if center:
            self.center()

        # Web preferences
        web_prefs = options.get("webPreferences", {})
        preload_script = web_prefs.get("preload", None)

        # Create HtmlFrame for rendering content
        self.web_contents = HtmlFrame(
            self.window,
            messages_enabled=True,
            horizontal_scrollbar="auto",
            vertical_scrollbar="auto",
        )
        self.web_contents.pack(fill="both", expand=True)
        self.window.configure(bg=bg_color)

        # Bind events
        self.web_contents.bind("<<DOMContentLoaded>>", self._on_dom_ready)
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        # Store preload script path
        self._preload_script = preload_script

        # Register window with app
        app.register_window(self)

        # Show/hide window
        if not show:
            self.hide()

    def load_url(self, url: str):
        """
        Load a URL in the window.

        Args:
            url: URL to load (http://, https://, or file://)
        """
        if url.startswith("file://"):
            # Handle file:// URLs
            file_path = url[7:]  # Remove 'file://'
            self.load_file(file_path)
        else:
            # For http/https URLs, we need to fetch and inject IPC
            try:
                import requests

                response = requests.get(url, timeout=10)
                response.raise_for_status()
                html = response.text

                # Inject IPC renderer script
                html = self._inject_ipc_script(html)

                if self._preload_script:
                    html = self._inject_preload_script(html)

                self.web_contents.load_html(html, base_url=url)
            except Exception as e:
                print(f"Error loading URL {url}: {e}", file=sys.stderr)
                # Fallback to direct load
                self.web_contents.load_url(url)

    def load_file(self, file_path: str):
        """
        Load an HTML file in the window.

        Args:
            file_path: Path to HTML file
        """
        file_path = Path(file_path).resolve()
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Execute preload script if specified
        if self._preload_script:
            html_content = self._inject_preload_script(html_content)

        self.web_contents.load_html(
            html_content, base_url=file_path.parent.as_uri() + "/"
        )

    def load_html(self, html: str, base_url: str = ""):
        """
        Load HTML content directly.

        Args:
            html: HTML content to load
            base_url: Base URL for resolving relative paths
        """
        # Inject IPC renderer script
        html = self._inject_ipc_script(html)

        if self._preload_script:
            html = self._inject_preload_script(html)

        self.web_contents.load_html(html, base_url=base_url)

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

    def _inject_preload_script(self, html: str) -> str:
        """Internal: Inject preload script into HTML"""
        preload_path = Path(self._preload_script).resolve()
        if not preload_path.exists():
            print(f"Warning: Preload script not found: {preload_path}", file=sys.stderr)
            return html

        with open(preload_path, "r", encoding="utf-8") as f:
            preload_code = f.read()

        # Inject script before </head> or at the beginning
        if "<head>" in html:
            script_tag = f"<script>{preload_code}</script>"
            html = html.replace("<head>", f"<head>{script_tag}", 1)
        else:
            script_tag = f"<html><head><script>{preload_code}</script></head><body>"
            if "<html>" not in html:
                html = script_tag + html + "</body></html>"

        return html

    def _on_dom_ready(self, event):
        """Internal: Handle DOM ready event"""
        for callback in self._dom_ready_callbacks:
            try:
                callback(event)
            except Exception as e:
                print(f"Error in dom-ready callback: {e}", file=sys.stderr)

    def on(self, event: str, callback: Callable):
        """
        Register event listener.

        Events:
            - 'ready-to-show': Window is ready to be shown
            - 'closed': Window has been closed
            - 'dom-ready': DOM is loaded and ready
        """
        if event == "ready-to-show":
            self._ready_callbacks.append(callback)
        elif event == "closed":
            self._closed_callbacks.append(callback)
        elif event == "dom-ready":
            self._dom_ready_callbacks.append(callback)
        else:
            raise ValueError(f"Unknown event: {event}")

    def show(self):
        """Show the window"""
        self.window.deiconify()

    def hide(self):
        """Hide the window"""
        self.window.withdraw()

    def close(self):
        """Close the window"""
        if self._is_closed:
            return

        self._is_closed = True

        # Emit closed event
        for callback in self._closed_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in closed callback: {e}", file=sys.stderr)

        # Unregister from app
        app.unregister_window(self)

        # Destroy window
        self.window.destroy()

    def center(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def set_title(self, title: str):
        """Set window title"""
        self.window.title(title)

    def get_title(self) -> str:
        """Get window title"""
        return self.window.title()

    def maximize(self):
        """Maximize the window"""
        self.window.state("zoomed")

    def minimize(self):
        """Minimize the window"""
        self.window.iconify()

    def set_size(self, width: int, height: int):
        """Set window size"""
        self.window.geometry(f"{width}x{height}")

    def get_size(self) -> tuple:
        """Get window size as (width, height)"""
        return (self.window.winfo_width(), self.window.winfo_height())
