import { mount } from "svelte";
// import './app.css'  // Removed - using component-scoped styles instead
import App from "./App.svelte";

const app = mount(App, {
  target: document.getElementById("app")!,
});

export default app;
