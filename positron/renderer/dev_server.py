"""
Development server utilities for React apps
Helps integrate with Vite, Webpack, or other dev servers
"""

import socket
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Optional


class DevServer:
    """
    Manages a development server (Vite, Webpack, etc.) for React apps.
    Automatically starts the dev server and provides the URL to load.
    """

    def __init__(
        self,
        cwd: str,
        command: str = "npm run dev",
        port: int = 5173,
        host: str = "localhost",
        wait_timeout: int = 30,
    ):
        """
        Initialize dev server manager.

        Args:
            cwd: Working directory for the dev server (where package.json is)
            command: Command to start the dev server (default: "npm run dev")
            port: Port the dev server runs on (default: 5173 for Vite)
            host: Host address (default: localhost)
            wait_timeout: Seconds to wait for server to be ready (default: 30)
        """
        self.cwd = Path(cwd).resolve()
        self.command = command
        self.port = port
        self.original_port = port
        self.host = host
        self.wait_timeout = wait_timeout
        self.process: Optional[subprocess.Popen] = None
        self._is_running = False
        self._server_ready = False

    def start(self):
        """Start the dev server"""
        if self._is_running:
            print("Dev server is already running")
            return

        print(f"Starting dev server: {self.command}")
        print(f"Working directory: {self.cwd}")

        # Start the dev server process
        try:
            self.process = subprocess.Popen(
                self.command,
                shell=True,
                cwd=str(self.cwd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Start threads to capture output
            threading.Thread(
                target=self._read_output, args=(self.process.stdout,), daemon=True
            ).start()
            threading.Thread(
                target=self._read_output, args=(self.process.stderr,), daemon=True
            ).start()

            self._is_running = True

            # Wait for server to be ready
            if not self.wait_for_ready():
                raise RuntimeError(
                    f"Dev server failed to start within {self.wait_timeout} seconds"
                )

            print(f"Dev server is ready at {self.get_url()}")

        except Exception as e:
            print(f"Failed to start dev server: {e}", file=sys.stderr)
            self.stop()
            raise

    def _read_output(self, pipe):
        """Read and print output from the dev server process"""
        import re

        try:
            for line in iter(pipe.readline, ""):
                if line:
                    print(f"[DevServer] {line.rstrip()}")

                    # Check if Vite is ready
                    if "ready in" in line.lower() or "local:" in line.lower():
                        self._server_ready = True

                    # Detect Next.js port (e.g., "- Local:         http://localhost:3001")
                    if "local:" in line.lower():
                        match = re.search(r"localhost:(\d+)", line)
                        if match:
                            detected_port = int(match.group(1))
                            if detected_port != self.original_port:
                                print(
                                    f"[DevServer] Detected port changed from {self.original_port} to {detected_port}"
                                )
                                self.port = detected_port
                        self._server_ready = True
        except Exception:
            pass

    def wait_for_ready(self) -> bool:
        """
        Wait for the dev server to be ready by checking output and port.

        Returns:
            True if server is ready, False if timeout
        """
        start_time = time.time()

        while time.time() - start_time < self.wait_timeout:
            # Check if we saw the ready message
            if self._server_ready:
                # Give it a moment to fully start
                time.sleep(1)
                return True

            # Also check if the current port is open (in case port changed)
            if self._is_port_open():
                # Give it a moment to fully start
                time.sleep(1)
                return True

            time.sleep(0.5)

        return False

    def _is_port_open(self) -> bool:
        """Check if the dev server port is open"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            result = sock.connect_ex((self.host, self.port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def stop(self):
        """Stop the dev server"""
        if not self._is_running:
            return

        print("Stopping dev server...")

        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

        self._is_running = False
        print("Dev server stopped")

    def get_url(self) -> str:
        """Get the dev server URL"""
        return f"http://{self.host}:{self.port}"

    def is_running(self) -> bool:
        """Check if dev server is running"""
        return self._is_running and self.process and self.process.poll() is None

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()
