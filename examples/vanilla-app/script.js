let count = 0;

// Update runtime status after DOM loads
const runtimeEl = document.getElementById("runtime");

// Check for Positron after a short delay to ensure IPC is injected
setTimeout(() => {
  runtimeEl.textContent = window.positron ? "Positron Desktop" : "Browser";
}, 100);

// Counter button
const counterBtn = document.getElementById("counterBtn");
counterBtn.addEventListener("click", () => {
  count++;
  counterBtn.textContent = `Count: ${count}`;

  // Send count to Python
  if (window.positron) {
    window.ipcRenderer.send("button-clicked", count);
  }
});

// Invoke Python button
const invokeBtn = document.getElementById("invokeBtn");
const messageEl = document.getElementById("message");

invokeBtn.addEventListener("click", async () => {
  if (!window.positron) {
    messageEl.textContent = "Not running in Positron - Python IPC unavailable";
    return;
  }

  try {
    const result = await window.ipcRenderer.invoke("greet", {
      name: "Vanilla JS",
    });
    messageEl.textContent = result.message;
  } catch (error) {
    messageEl.textContent = `Error: ${error.message}`;
  }
});
