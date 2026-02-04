"""
IPC Renderer Process Module
This provides the JavaScript API for renderer processes to communicate with main process.
This file generates JavaScript code that gets injected into the renderer.
"""


def get_ipc_renderer_script() -> str:
    """
    Generate the JavaScript ipcRenderer API that gets injected into the page.
    This provides a bridge between JavaScript and Python.
    """
    return """
// Positron IPC Renderer
(function() {
    'use strict';

    // Storage for IPC callbacks
    const _ipcCallbacks = {};
    const _ipcOnceCallbacks = {};
    let _ipcMessageId = 0;

    // IPC Renderer API
    window.positron = window.positron || {};

    window.positron.ipcRenderer = {
        /**
         * Send a message to the main process
         * @param {string} channel - Channel name
         * @param {...any} args - Arguments to send
         */
        send: function(channel, ...args) {
            // Communicate with Python through a custom protocol
            const message = {
                type: 'ipc-message',
                channel: channel,
                args: args
            };

            // Send to Python via title hack or custom URL scheme
            // This is a workaround until we implement proper Python-JS bridge
            window._positronIPCSend = window._positronIPCSend || [];
            window._positronIPCSend.push(message);

            // Trigger a custom event that Python can intercept
            document.title = 'ipc:' + JSON.stringify(message);
        },

        /**
         * Send a message and wait for reply (promise-based)
         * @param {string} channel - Channel name
         * @param {...any} args - Arguments to send
         * @returns {Promise} - Promise that resolves with the response
         */
        invoke: function(channel, ...args) {
            return new Promise((resolve, reject) => {
                const messageId = _ipcMessageId++;
                const replyChannel = `${channel}-reply-${messageId}`;

                // Register one-time reply handler
                _ipcOnceCallbacks[replyChannel] = function(event, result) {
                    resolve(result);
                };

                // Send message with reply channel
                const message = {
                    type: 'ipc-invoke',
                    channel: channel,
                    replyChannel: replyChannel,
                    messageId: messageId,
                    args: args
                };

                window._positronIPCSend = window._positronIPCSend || [];
                window._positronIPCSend.push(message);
                document.title = 'ipc:' + JSON.stringify(message);
            });
        },

        /**
         * Listen for messages from main process
         * @param {string} channel - Channel name
         * @param {function} callback - Callback function(event, ...args)
         */
        on: function(channel, callback) {
            if (!_ipcCallbacks[channel]) {
                _ipcCallbacks[channel] = [];
            }
            _ipcCallbacks[channel].push(callback);
        },

        /**
         * Listen for a single message from main process
         * @param {string} channel - Channel name
         * @param {function} callback - Callback function(event, ...args)
         */
        once: function(channel, callback) {
            if (!_ipcOnceCallbacks[channel]) {
                _ipcOnceCallbacks[channel] = [];
            }
            _ipcOnceCallbacks[channel].push(callback);
        },

        /**
         * Remove listener for a channel
         * @param {string} channel - Channel name
         * @param {function} callback - Callback to remove
         */
        removeListener: function(channel, callback) {
            if (_ipcCallbacks[channel]) {
                _ipcCallbacks[channel] = _ipcCallbacks[channel].filter(cb => cb !== callback);
            }
        },

        /**
         * Remove all listeners for a channel
         * @param {string} channel - Channel name
         */
        removeAllListeners: function(channel) {
            if (channel) {
                delete _ipcCallbacks[channel];
                delete _ipcOnceCallbacks[channel];
            } else {
                Object.keys(_ipcCallbacks).forEach(key => delete _ipcCallbacks[key]);
                Object.keys(_ipcOnceCallbacks).forEach(key => delete _ipcOnceCallbacks[key]);
            }
        },

        /**
         * Internal: Receive message from main process
         * This is called by the Python side
         */
        _receive: function(channel, ...args) {
            const event = { sender: window.positron };

            // Handle once callbacks
            if (_ipcOnceCallbacks[channel]) {
                const callbacks = _ipcOnceCallbacks[channel];
                delete _ipcOnceCallbacks[channel];
                callbacks.forEach(callback => callback(event, ...args));
            }

            // Handle regular callbacks
            if (_ipcCallbacks[channel]) {
                _ipcCallbacks[channel].forEach(callback => callback(event, ...args));
            }
        }
    };

    // Alias for convenience
    window.ipcRenderer = window.positron.ipcRenderer;

    console.log('Positron IPC Renderer initialized');
})();
"""


class IPCRenderer:
    """
    Renderer-side IPC handler (Python side).
    This class provides utilities for working with the renderer's IPC.
    """

    @staticmethod
    def get_preload_script() -> str:
        """Get the IPC renderer JavaScript to inject into pages"""
        return get_ipc_renderer_script()


ipc_renderer = IPCRenderer()
