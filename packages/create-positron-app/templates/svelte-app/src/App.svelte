<script lang="ts">
  import { onMount } from 'svelte'
  import Logo from './lib/Logo.svelte'

  let count = 0
  let message = ''
  let isPositron = false

  onMount(() => {
    // Check for positron object with retry mechanism
    const checkPositron = () => {
      if ((window as any).positron) {
        isPositron = true
        ;(window as any).ipcRenderer.on('message-from-main', (event: any, msg: string) => {
          message = msg
        })
        ;(window as any).ipcRenderer.send('renderer-ready', 'Hello from Svelte!')
      } else {
        // Retry after a short delay to ensure script injection
        setTimeout(checkPositron, 100)
      }
    }

    checkPositron()
  })

  function handleClick() {
    count++
    if ((window as any).positron) {
      ;(window as any).ipcRenderer.send('button-clicked', count)
    }
  }

  async function handleInvoke() {
    if ((window as any).positron) {
      try {
        const result = await (window as any).ipcRenderer.invoke('get-data', 'Hello from Svelte')
        message = result
      } catch (error: any) {
        message = `Error: ${error.message}`
      }
    } else {
      message = 'IPC not available in browser mode'
    }
  }
</script>

<div class="app">
  <div class="container">
    <Logo />
    <h1>Positron</h1>
    <p class="subtitle">Python + Svelte Desktop Apps</p>

    <div class="actions">
      <button class="btn" on:click={handleClick}>
        Count: {count}
      </button>
      <button class="btn btn-primary" on:click={handleInvoke}>
        Call Python
      </button>
    </div>

    {#if message}
      <div class="message">{message}</div>
    {/if}

    <div class="status">
      {isPositron ? 'Running in Positron' : 'Browser mode'}
    </div>
  </div>
</div>

<style>
  :global(*) {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  .app {
    min-height: 100vh;
    width: 100%;
    background: #0a0a0a;
    color: #e0e0e0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  }

  .container {
    text-align: center;
    width: 100%;
    padding: 4rem 2rem;
  }

  h1 {
    font-size: 3rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
  }

  .subtitle {
    font-size: 1rem;
    color: #666;
    margin-bottom: 3rem;
    font-weight: 400;
  }

  .actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-bottom: 2rem;
  }

  .btn {
    padding: 0.75rem 1.5rem;
    font-size: 0.95rem;
    font-weight: 500;
    border: 1px solid #333;
    background: #1a1a1a;
    color: #e0e0e0;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
  }

  .btn:hover {
    background: #252525;
    border-color: #444;
  }

  .btn:active {
    transform: scale(0.98);
  }

  .btn-primary {
    background: #ffffff;
    color: #0a0a0a;
    border-color: #ffffff;
  }

  .btn-primary:hover {
    background: #e0e0e0;
    border-color: #e0e0e0;
  }

  .message {
    padding: 1rem;
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 8px;
    margin-bottom: 2rem;
    font-size: 0.9rem;
    color: #e0e0e0;
    line-height: 1.5;
  }

  .status {
    font-size: 0.85rem;
    color: #666;
    padding: 0.5rem;
    border-top: 1px solid #222;
    margin-top: 2rem;
    padding-top: 2rem;
  }
</style>
