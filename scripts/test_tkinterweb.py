"""Direct test of TkinterWeb without Positron wrapper"""

import tkinter as tk

from tkinterweb import HtmlFrame

root = tk.Tk()
root.title("TkinterWeb Test")
root.geometry("800x600")

frame = HtmlFrame(root, messages_enabled=True)
frame.pack(fill="both", expand=True)

html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
        }
        h1 { font-size: 3em; }
        button {
            background: white;
            color: #667eea;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 8px;
            cursor: pointer;
            margin: 10px;
        }
    </style>
</head>
<body>
    <h1>TkinterWeb Direct Test</h1>
    <p>If you see this, TkinterWeb is working!</p>
    <button onclick="alert('JS works')">Test JavaScript</button>
    <button onclick="document.body.style.background='red'">Change Color</button>
</body>
</html>
"""

frame.load_html(html)

root.mainloop()
