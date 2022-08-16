import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  build: { manifest: true },
  // eslint-disable-next-line no-undef
  base: process.env.mode === "production" ? "/static/" : "/",
  root: "./src",
  plugins: [react()],
});
