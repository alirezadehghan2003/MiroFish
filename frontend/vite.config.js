import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@locales': path.resolve(__dirname, '../locales')
    }
  },
  server: {
    // 默认仅本机可访问；Docker 中通过 MIROFISH_FRONTEND_HOST=0.0.0.0 覆盖
    host: process.env.MIROFISH_FRONTEND_HOST || '127.0.0.1',
    port: 3000,
    open: process.env.MIROFISH_FRONTEND_OPEN !== 'false',
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
