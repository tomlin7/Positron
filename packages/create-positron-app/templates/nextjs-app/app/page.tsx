"use client";

import { useState, useEffect } from "react";
import Logo from "./components/Logo";
import "./globals.css";

export default function Home() {
  const [count, setCount] = useState(0);
  const [message, setMessage] = useState("");

  useEffect(() => {
    if ((window as any).positron) {
      (window as any).ipcRenderer.on(
        "message-from-main",
        (event: any, msg: string) => {
          setMessage(msg);
        },
      );
      (window as any).ipcRenderer.send("renderer-ready", "Hello from Next.js!");
    }
  }, []);

  const handleClick = () => {
    setCount(count + 1);
    if ((window as any).positron) {
      (window as any).ipcRenderer.send("button-clicked", count + 1);
    }
  };

  const handleInvoke = async () => {
    if ((window as any).positron) {
      try {
        const result = await (window as any).ipcRenderer.invoke(
          "get-data",
          "Hello from Next.js",
        );
        setMessage(result);
      } catch (error: any) {
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
        <p className="subtitle">Python + Next.js Desktop Apps</p>

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
          {typeof window !== "undefined" && (window as any).positron
            ? "Running in Positron"
            : "Browser mode"}
        </div>
      </div>
    </div>
  );
}
