import { defineConfig } from "vite";
import preact from "@preact/preset-vite";

export default defineConfig({
  plugins: [preact()],
  build: {
    outDir: "../frontend",
    emptyOutDir: true,
    assetsDir: "__assets__",
  },
  server: {
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
