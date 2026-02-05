let count = 0;

// Update runtime status
const runtimeEl = document.getElementById('runtime');
runtimeEl.textContent = window.positron ? 'Positron Desktop' : 'Browser';

// Counter button
const counterBtn = document.getElementById('counterBtn');
counterBtn.addEventListener('click', () => {
    count++;
    counterBtn.textContent = `Count: ${count}`;
});

// Invoke Python button
const invokeBtn = document.getElementById('invokeBtn');
const messageEl = document.getElementById('message');

invokeBtn.addEventListener('click', async () => {
    if (!window.positron) {
        messageEl.textContent = 'Not running in Positron - Python IPC unavailable';
        return;
    }

    try {
        const result = await window.positron.ipcInvoke('greet', { name: 'Vanilla JS' });
        messageEl.textContent = result.message;
    } catch (error) {
        messageEl.textContent = `Error: ${error.message}`;
    }
});
