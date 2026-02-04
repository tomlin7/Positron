"""IPC (Inter-Process Communication) modules for Positron"""

from .main_webview import ipc_main
from .renderer_webview import ipc_renderer

__all__ = ["ipc_main", "ipc_renderer"]
