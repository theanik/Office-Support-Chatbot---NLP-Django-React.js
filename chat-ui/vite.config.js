import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react({
    include: "**/*.jsx"
  })],
  server: {
    hmr : false,
    watch: {
      usePolling: true,
    },
    host: true,
    port: 5173,
  }
})
