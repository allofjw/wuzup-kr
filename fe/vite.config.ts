import { defineConfig } from "vite";
import { resolve } from "jsr:@std/path";
import deno from "@deno/vite-plugin";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [deno(), react()],
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, "index.html"),
        credits: resolve(__dirname, "credits/index.html"),
      },
    },
  },
});
