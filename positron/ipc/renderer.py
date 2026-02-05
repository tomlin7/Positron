"""
IPC Renderer Module for pywebview
Uses pywebview's JS API for Python-JavaScript communication
"""


def get_ipc_renderer_script() -> str:
    """
    Generate the JavaScript ipcRenderer API for pywebview.
    Uses pywebview's built-in JS-Python bridge.
    """
    return """
// Positron IPC Renderer for pywebview
(function() {
    'use strict';

    // Storage for IPC callbacks
    const _ipcCallbacks = {};
    const _ipcOnceCallbacks = {};
    let _ipcMessageId = 0;

    // Wait for pywebview API to be ready
    window.addEventListener('pywebviewready', function() {
        console.log('Pywebview API ready event fired, initializing Positron IPC');
        initPositronIPC();
    });

    function initPositronIPC() {
        // Check if pywebview API is available
        if (!window.pywebview || !window.pywebview.api) {
            console.log('Pywebview API not available yet, retrying...');
            setTimeout(initPositronIPC, 100);
            return;
        }

        // If already initialized, don't reinitialize
        if (window.positron && window.positron.ipcRenderer) {
            console.log('Positron IPC already initialized');
            return;
        }

        // IPC Renderer API
        window.positron = window.positron || {};

        window.positron.ipcRenderer = {
            /**
             * Send a one-way message to the main process
             * @param {string} channel - Channel name
             * @param {...any} args - Arguments to send
             */
            send: function(channel, ...args) {
                if (window.pywebview && window.pywebview.api && window.pywebview.api.ipc_send) {
                    window.pywebview.api.ipc_send(channel, args).catch(err => {
                        console.error('IPC send error:', err);
                    });
                } else {
                    console.error('Pywebview API not ready for send');
                }
            },

            /**
             * Send a message and wait for reply (promise-based)
             * @param {string} channel - Channel name
             * @param {...any} args - Arguments to send
             * @returns {Promise} - Promise that resolves with the response
             */
            invoke: async function(channel, ...args) {
                if (window.pywebview && window.pywebview.api && window.pywebview.api.ipc_invoke) {
                    try {
                        const result = await window.pywebview.api.ipc_invoke(channel, args);
                        return result;
                    } catch (err) {
                        console.error('IPC invoke error:', err);
                        throw err;
                    }
                } else {
                    throw new Error('Pywebview API not ready for invoke');
                }
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
                const onceWrapper = function(event, ...args) {
                    this.removeListener(channel, onceWrapper);
                    callback(event, ...args);
                }.bind(this);
                this.on(channel, onceWrapper);
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
                } else {
                    Object.keys(_ipcCallbacks).forEach(key => delete _ipcCallbacks[key]);
                }
            },

            /**
             * Internal: Receive message from main process
             * This is called by Python via evaluate_js
             */
            _receive: function(channel, ...args) {
                const event = { sender: window.positron };

                // Handle regular callbacks
                if (_ipcCallbacks[channel]) {
                    _ipcCallbacks[channel].forEach(callback => {
                        try {
                            callback(event, ...args);
                        } catch (err) {
                            console.error('Error in IPC callback:', err);
                        }
                    });
                }
            }
        };

        // Alias for convenience (Electron-compatible)
        window.ipcRenderer = window.positron.ipcRenderer;

        console.log('Positron IPC Renderer initialized with pywebview');
    }

    // Try to initialize immediately in case pywebview is already ready
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        setTimeout(initPositronIPC, 0);
    }

    // Also try immediately (for when injected after page load)
    initPositronIPC();
})();
"""


class IPCRenderer:
    """
    Renderer-side IPC handler for pywebview.
    Provides utilities for working with the renderer's IPC.
    """

    @staticmethod
    def get_preload_script() -> str:
        """Get the IPC renderer JavaScript to inject into pages"""
        return get_ipc_renderer_script()


ipc_renderer = IPCRenderer()
