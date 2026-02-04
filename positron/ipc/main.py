"""
IPC Main Process Module
Handles communication from renderer (JavaScript) to main (Python)
"""

import json
import sys
from typing import Any, Callable, Dict, Optional


class IPCMain:
    """
    Main process IPC handler.
    Listens for messages from renderer processes and can send replies.
    """

    def __init__(self):
        self._handlers: Dict[str, Callable] = {}
        self._once_handlers: Dict[str, Callable] = {}

    def on(self, channel: str, handler: Callable):
        """
        Register a handler for a channel.
        Handler receives (event, *args) where event contains sender information.

        Args:
            channel: Channel name to listen on
            handler: Callback function(event, *args)
        """
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
        Register a handler that can send a reply using event.reply()
        Similar to Electron's ipcMain.handle()

        Can be used as a decorator:
            @ipc_main.handle('channel')
            def handler(event, *args):
                return result

        Or called directly:
            ipc_main.handle('channel', handler_function)

        Args:
            channel: Channel name to handle
            handler: Callback function(event, *args) -> result (optional if used as decorator)
        """

        def decorator(func):
            def wrapper(event, *args):
                try:
                    result = func(event, *args)
                    return result
                except Exception as e:
                    print(f"Error in IPC handler for '{channel}': {e}", file=sys.stderr)
                    raise

            self._handlers[channel] = wrapper
            return func

        # Support both decorator and direct call
        if handler is None:
            # Used as decorator: @ipc_main.handle('channel')
            return decorator
        else:
            # Direct call: ipc_main.handle('channel', handler)
            decorator(handler)
            return handler

    def _dispatch(self, channel: str, sender, *args):
        """
        Internal: Dispatch a message to the appropriate handler.

        Args:
            channel: Channel name
            sender: The BrowserWindow that sent the message
            *args: Arguments passed from renderer
        """
        event = IPCMainEvent(sender, channel)

        # Check once handlers first
        if channel in self._once_handlers:
            handler = self._once_handlers.pop(channel)
            try:
                return handler(event, *args)
            except Exception as e:
                print(
                    f"Error in IPC once handler for '{channel}': {e}", file=sys.stderr
                )
                raise

        # Check regular handlers
        if channel in self._handlers:
            handler = self._handlers[channel]
            try:
                return handler(event, *args)
            except Exception as e:
                print(f"Error in IPC handler for '{channel}': {e}", file=sys.stderr)
                raise

        print(
            f"Warning: No IPC handler registered for channel '{channel}'",
            file=sys.stderr,
        )
        return None


class IPCMainEvent:
    """
    Event object passed to IPC handlers.
    Contains information about the sender and provides reply mechanism.
    """

    def __init__(self, sender, channel: str):
        """
        Args:
            sender: The BrowserWindow that sent the message
            channel: The channel name
        """
        self.sender = sender
        self.channel = channel
        self._reply_channel = f"{channel}-reply"

    def reply(self, channel: str, *args):
        """
        Send a reply back to the renderer process.

        Args:
            channel: Channel to send reply on
            *args: Arguments to send
        """
        # This will be implemented when we add JavaScript bridge
        # For now, we'll store it for the renderer to retrieve
        if hasattr(self.sender, "_ipc_send_to_renderer"):
            self.sender._ipc_send_to_renderer(channel, *args)


# Singleton instance
ipc_main = IPCMain()
