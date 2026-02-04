"""Test simple HTML loading"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from positron import App, BrowserWindow

app = App()


def create_window():
    win = BrowserWindow(
        {
            "width": 1000,
            "height": 700,
            "title": "Test Simple HTML",
        }
    )

    # Load the test HTML file
    test_file = Path(__file__).parent / "test.html"
    print(f"Loading: {test_file}")
    win.load_file(str(test_file))

    return win


def main():
    print("Testing simple HTML...")

    window = None

    def on_ready():
        nonlocal window
        window = create_window()

    app.when_ready(on_ready)
    app.run()


if __name__ == "__main__":
    main()
