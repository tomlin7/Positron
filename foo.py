from nicegui import ui

ui.label("My Custom Tauri-like App")
ui.button("Click Me", on_click=lambda: ui.notify("Python Power!"))

# native=True uses pywebview/WebView2 under the hood
ui.run(native=True, window_size=(800, 600), title="My App")
