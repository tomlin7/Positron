"""Simple test to see if TkinterWeb works"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from positron import App, BrowserWindow

app = App()


def create_window():
    win = BrowserWindow({"width": 800, "height": 600, "title": "Simple Test"})

    # Test with simple HTML
    win.load_html("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test</title>
        <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            h1 { font-size: 3em; }
        </style>
    </head>
    <body>
        <div>
            <h1>Positron Works!</h1>
            <p>If you see this, TkinterWeb is rendering correctly.</p>
            <button onclick="alert('JavaScript works!')">Test JS</button>
        </div>
    </body>
    </html>
    """)


app.when_ready(create_window)
app.run()
