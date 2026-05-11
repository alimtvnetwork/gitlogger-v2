import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Builds a single index.js + index.css into ./dist/, enqueued by class-admin-page.php.
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "dist",
    emptyOutDir: true,
    rollupOptions: {
      input: "src/main.tsx",
      output: {
        entryFileNames: "index.js",
        assetFileNames: (info) =>
          info.name && info.name.endsWith(".css") ? "index.css" : "[name][extname]",
      },
    },
  },
});
