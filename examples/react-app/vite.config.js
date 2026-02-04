import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Vite config for Positron React app
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true,
    cors: true,
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
  },
  base: "./",
});
