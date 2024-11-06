import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default ({ command, mode }) => {
  if (command === 'build') {
    return defineConfig({
      base: '/static',
      plugins: [vue()],
      resolve: {
        alias: {
          '@': fileURLToPath(new URL('./src', import.meta.url))
        }
      },
      build: {
        chunkSizeWarningLimit:1500,
        outDir: "../static/"
      }
    })
  }else {
    return defineConfig({
      plugins: [vue()],
      resolve: {
        alias: {
          '@': fileURLToPath(new URL('./src', import.meta.url))
        }
      },
      server: {
        host: true,
        proxy: {
          '/api': {
            target: 'http://127.0.0.1:9000/',
            changeOrigin: true,
            // rewrite: (path) => path.replace(/^\/api/, ''),
          }
        }
      }
    })
  }

}
