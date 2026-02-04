"""
Simple test to check if webview can load the dev server
"""

import time

import webview


def main():
    print("Creating window...")
    window = webview.create_window(
        "Test", "http://localhost:5173/", width=1000, height=700
    )

    def on_loaded():
        print("Page loaded!")
        # Try to get page content
        time.sleep(1)
        result = window.evaluate_js("document.body.innerHTML")
        print(f"Body content: {result[:200] if result else 'None'}")

    window.events.loaded += on_loaded

    print("Starting webview with debug=True...")
    webview.start(debug=True)


if __name__ == "__main__":
    main()
