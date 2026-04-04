import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/moods': 'http://localhost:42001',
      '/users': 'http://localhost:42001',
      '/analytics': 'http://localhost:42001',
      '/health': 'http://localhost:42001',
    },
  },
});
