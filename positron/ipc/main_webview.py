"""
IPC Main Process Module for pywebview
Handles communication from renderer (JavaScript) to main (Python)
Uses pywebview's JS API to expose Python functions
"""

import sys
from typing import Any, Callable, Dict, Optional


class IPCEvent:
    """
    IPC Event object passed to handlers.
    Allows sending replies back to the renderer.
    """

    def __init__(self, window=None):
        self.window = window
        # Create a sender object with send method
        self.sender = type(
            "Sender",
            (),
            {"send": lambda channel, *args: self._send_to_renderer(channel, *args)},
        )()

    def _send_to_renderer(self, channel: str, *args):
        """
        Internal method to send messages to renderer.

        Args:
            channel: Channel name
            *args: Arguments to send
        """
        if self.window:
            # Call JavaScript function to trigger callbacks
            import json

            js_args = json.dumps(args[0] if len(args) == 1 else args)
            js_code = f"window.positron.ipcRenderer._receive('{channel}', {js_args})"
            try:
                self.window.evaluate_js(js_code)
            except Exception as e:
                print(f"Error sending to channel '{channel}': {e}", file=sys.stderr)

    def reply(self, channel: str, *args):
        """
        Send a reply to the renderer process.

        Args:
            channel: Reply channel name
            *args: Arguments to send
        """
        self._send_to_renderer(channel, *args)


class IPCMain:
    """
    Main process IPC handler for pywebview.
    Exposes Python functions to JavaScript via pywebview's API.
    """

    def __init__(self):
        self._handlers: Dict[str, Callable] = {}
        self._once_handlers: Dict[str, Callable] = {}
        self._current_window = None  # Set by BrowserWindow when exposing API

    def set_current_window(self, window):
        """Set the current window for API exposure"""
        self._current_window = window

    def on(self, channel: str, handler: Optional[Callable] = None):
        """
        Register a handler for a channel.
        Handler receives (event, *args) where event contains sender information.

        Can be used as a decorator:
            @ipc_main.on('channel')
            def handler(event, *args):
                # Handle message

        Or called directly:
            ipc_main.on('channel', handler_function)

        Args:
            channel: Channel name to listen on
            handler: Callback function(event, *args) (optional if used as decorator)
        """

        def decorator(func):
            self._handlers[channel] = func
            return func

        if handler is None:
            return decorator
        else:
            self._handlers[channel] = handler

    def once(self, channel: str, handler: Callable):
        """
        Register a one-time handler for a channel.

        Args:
            channel: Channel name to listen on
            handler: Callback function(event, *args)
        """
        self._once_handlers[channel] = handler

    def remove_listener(self, channel: str):
        """
        Remove a handler for a channel.

        Args:
            channel: Channel name
        """
        if channel in self._handlers:
            del self._handlers[channel]
        if channel in self._once_handlers:
            del self._once_handlers[channel]

    def remove_all_listeners(self, channel: Optional[str] = None):
        """
        Remove all listeners for a channel, or all listeners if no channel specified.

        Args:
            channel: Channel name (optional)
        """
        if channel:
            self.remove_listener(channel)
        else:
            self._handlers.clear()
            self._once_handlers.clear()

    def handle(self, channel: str, handler: Optional[Callable] = None):
        """
        Register a handler that returns a value (for invoke/handle pattern).
        Similar to Electron's ipcMain.handle()

        Can be used as a decorator:
            @ipc_main.handle('get-data')
            def handler(event, *args):
                return {"data": "value"}

        Or called directly:
            ipc_main.handle('get-data', handler_function)

        Args:
            channel: Channel name to handle
            handler: Callback function(event, *args) -> result (optional if used as decorator)
        """

        def decorator(func):
            self._handlers[channel] = func
            return func

        if handler is None:
            return decorator
        else:
            self._handlers[channel] = handler

    def _dispatch(self, channel: str, window, *args):
        """
        Internal: Dispatch a message to the appropriate handler.

        Args:
            channel: Channel name
            window: The window that sent the message
            *args: Message arguments

        Returns:
            Handler result (for invoke pattern)
        """
        event = IPCEvent(window)

        # Check once handlers first
        if channel in self._once_handlers:
            handler = self._once_handlers.pop(channel)
            try:
                return handler(event, *args)
            except Exception as e:
                print(f"Error in once handler for '{channel}': {e}", file=sys.stderr)
                raise

        # Check regular handlers
        if channel in self._handlers:
            handler = self._handlers[channel]
            try:
                return handler(event, *args)
            except Exception as e:
                print(f"Error in handler for '{channel}': {e}", file=sys.stderr)
                raise

        print(
            f"Warning: No handler registered for channel '{channel}'", file=sys.stderr
        )
        return None

    def get_js_api(self, window):
        """
        Get the JavaScript API object to expose via pywebview.

        Args:
            window: The BrowserWindow instance

        Returns:
            API class with methods for JavaScript
        """

        # Create API object with methods
        # Note: We use a simple object, not a class, for pywebview compatibility
        api = type("JSApi", (), {})()

        def ipc_send(channel, args):
            """
            Handle send() calls from JavaScript.

            Args:
                channel: Channel name
                args: List of arguments
            """
            try:
                # Unpack args list
                unpacked_args = args if isinstance(args, (list, tuple)) else [args]
                ipc_main._dispatch(channel, window, *unpacked_args)
                return {"success": True}
            except Exception as e:
                print(f"IPC send error: {e}", file=sys.stderr)
                return {"success": False, "error": str(e)}

        def ipc_invoke(channel, args):
            """
            Handle invoke() calls from JavaScript.

            Args:
                channel: Channel name
                args: List of arguments

            Returns:
                Result from handler
            """
            try:
                # Unpack args list
                unpacked_args = args if isinstance(args, (list, tuple)) else [args]
                result = ipc_main._dispatch(channel, window, *unpacked_args)
                return result
            except Exception as e:
                print(f"IPC invoke error: {e}", file=sys.stderr)
                raise

        # Attach methods to the API object
        api.ipc_send = ipc_send
        api.ipc_invoke = ipc_invoke

        return api

    def send_to_window(self, window, channel: str, *args):
        """
        Send a message to a renderer window.

        Args:
            window: The BrowserWindow to send to
            channel: Channel name
            *args: Arguments to send
        """
        if window and hasattr(window, "evaluate_js"):
            js_args = ", ".join([repr(arg) for arg in args])
            js_code = f"window.positron.ipcRenderer._receive('{channel}', {js_args})"
            try:
                window.evaluate_js(js_code)
            except Exception as e:
                print(
                    f"Error sending to window on channel '{channel}': {e}",
                    file=sys.stderr,
                )


# Singleton instance
ipc_main = IPCMain()
