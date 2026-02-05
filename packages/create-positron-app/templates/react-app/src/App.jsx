import { useState, useEffect } from "react";
import "./App.css";
import Logo from "./Logo";

function App() {
  const [count, setCount] = useState(0);
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (window.positron) {
      window.ipcRenderer.on("message-from-main", (event, msg) => {
        setMessage(msg);
      });
      window.ipcRenderer.send("renderer-ready", "Hello from React!");
    }
  }, []);

  const handleClick = () => {
    setCount(count + 1);
    if (window.positron) {
      window.ipcRenderer.send("button-clicked", count + 1);
    }
  };

  const handleInvoke = async () => {
    if (window.positron) {
      try {
        const result = await window.ipcRenderer.invoke(
          "get-data",
          "Hello from React",
        );
        setMessage(result);
      } catch (error) {
        setMessage(`Error: ${error.message}`);
      }
    } else {
      setMessage("IPC not available in browser mode");
    }
  };

  return (
    <div className="app">
      <div className="container">
        <Logo />
        <h1>Positron</h1>
        <p className="subtitle">Python + React Desktop Apps</p>

        <div className="actions">
          <button className="btn" onClick={handleClick}>
            Count: {count}
          </button>
          <button className="btn btn-primary" onClick={handleInvoke}>
            Call Python
          </button>
        </div>

        {message && <div className="message">{message}</div>}

        <div className="status">
          {window.positron ? "Running in Positron" : "Browser mode"}
        </div>
      </div>
    </div>
  );
}

export default App;
