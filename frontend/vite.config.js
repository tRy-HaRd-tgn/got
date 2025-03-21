import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://194.59.186.20:8000',  // Адрес вашего FastAPI
        changeOrigin: true,
        secure: false,
      },
    },
  },
});