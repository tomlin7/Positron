"""
Positron - Electron-like framework for Python
Build cross-platform desktop apps with React and Python
"""

from .common.utilities import __author__, __title__, __version__

# Use webview-based implementations
from .ipc.main_webview import ipc_main
from .main.app_webview import App
from .main.browser_window_webview import BrowserWindow

__all__ = ["App", "BrowserWindow", "ipc_main"]
__version__ = "0.1.0"
__title__ = "Positron"
__author__ = "Positron Contributors"
