"""Test raw pywebview without Positron wrapper"""

from pathlib import Path

import webview


def main():
    print("Testing raw pywebview...")

    # Test 1: Load HTML string directly
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Raw Test</title>
        <style>
            body {
                background: #1a1a1a;
                color: white;
                font-family: Arial;
                padding: 50px;
            }
            h1 { color: #61dafb; }
        </style>
    </head>
    <body>
        <h1>Raw PyWebView Test</h1>
        <p>If you see this, pywebview is working!</p>
        <div id="output"></div>
        <script>
            console.log("JavaScript running!");
            document.getElementById('output').innerHTML = '<p style="color: lime;">JavaScript works!</p>';
        </script>
    </body>
    </html>
    """

    window = webview.create_window("Raw Test", html=html, width=1000, height=700)

    def on_loaded():
        print("Window loaded event fired!")

    window.events.loaded += on_loaded

    print("Starting webview...")
    webview.start(debug=True)
    print("Webview closed")


if __name__ == "__main__":
    main()
