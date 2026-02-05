# Positron Documentation Desktop App

This is a Positron desktop app that wraps the documentation website.

## Run as Desktop App

```bash
# Make sure dependencies are installed
npm install

# Run as desktop app
python main.py
```

The app will:
1. Start the Next.js dev server (http://localhost:3000)
2. Open a native desktop window
3. Load the docs inside the window
4. Clean up the dev server when you close the window

## Run as Web App (normal)

```bash
npm run dev
# Open http://localhost:3000 in browser
```

## Features

- Native window with full docs
- Same as web version but in a desktop app
- Auto-manages Next.js dev server
- Clean shutdown handling
