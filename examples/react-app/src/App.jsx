import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [message, setMessage] = useState('')

  useEffect(() => {
    // Check if we're running in Positron
    if (window.positron) {
      console.log('Running in Positron!')

      // Example: Listen for messages from main process
      window.ipcRenderer.on('message-from-main', (event, msg) => {
        setMessage(msg)
      })

      // Example: Send message to main process
      window.ipcRenderer.send('renderer-ready', 'Hello from React!')
    } else {
      console.log('Running in browser (development mode)')
    }
  }, [])

  const handleClick = () => {
    setCount(count + 1)

    // Send message to main process if in Positron
    if (window.positron) {
      window.ipcRenderer.send('button-clicked', count + 1)
    }
  }

  const handleInvoke = async () => {
    if (window.positron) {
      try {
        const result = await window.ipcRenderer.invoke('get-data', 'some-argument')
        setMessage(`Response from Python: ${result}`)
      } catch (error) {
        setMessage(`Error: ${error.message}`)
      }
    } else {
      setMessage('IPC not available in browser mode')
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to Positron</h1>
        <p className="subtitle">Electron-like framework for Python + React</p>

        <div className="card">
          <button onClick={handleClick}>
            Count is {count}
          </button>
          <button onClick={handleInvoke} style={{ marginLeft: '10px' }}>
            Call Python IPC
          </button>
        </div>

        {message && (
          <div className="message-box">
            <p>{message}</p>
          </div>
        )}

        <div className="info">
          <p>
            {window.positron
              ? '✅ Running in Positron (Python + TkinterWeb)'
              : '🌐 Running in browser (dev mode)'}
          </p>
        </div>

        <div className="features">
          <h2>Features</h2>
          <ul>
            <li>✨ React + Vite for fast development</li>
            <li>🐍 Python backend with full system access</li>
            <li>🔗 IPC communication between React and Python</li>
            <li>🖼️ Native window management</li>
            <li>📦 Familiar Electron-like API</li>
          </ul>
        </div>

        <p className="code-example">
          Edit <code>src/App.jsx</code> and save to reload
        </p>
      </header>
    </div>
  )
}

export default App
