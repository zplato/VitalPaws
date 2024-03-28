import { fileURLToPath, URL } from 'node:url'


import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),

    // https://vite-pwa-org.netlify.app/guide/
    VitePWA({ 
      strategies: 'generateSW',
      registerType: 'autoUpdate',
      injectRegister: 'auto',
      devOptions: {
        enabled: true,
        suppressWarnings: true,
        navigateFallback: '/',
        navigateFallbackAllowlist: [/^\/$/],
        type: 'module',
      },
      includeAssets: [
        'icons/*', 
        'images/*', 
        'https://placedog.net/1000?id=2'
      ],
      workbox: {
        globPatterns: [
          '**/*.{js,css,html,ico,png,svg,jpg,jpeg,json,ttf,eot,woff,woff2,webp}', 
          'icons/*', 
          'images/*', 
          'https://placedog.net/1000?id=2'
        ],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/placedog\.net\/.*/i,
            handler: 'CacheFirst',
            options: {
              cacheName: 'external-images',
              expiration: {
                maxEntries: 10,
                maxAgeSeconds: 60 * 60 * 24 * 365 // <== 365 days
              },
              cacheableResponse: {
                statuses: [0, 200]
              }
            }
          },
          {
            urlPattern: /^https:\/\/.*/i, 
            handler: 'StaleWhileRevalidate',
          },
        ]
      },
      client: {
        installPrompt: true,
        // you don't need to include this: only for testing purposes
        // if enabling periodic sync for update use 1 hour or so (periodicSyncForUpdates: 3600)
        periodicSyncForUpdates: 3600,
      },      
      manifest: {
        name: 'VitalPaws',
        short_name: 'VitalPaws',
        description: 'Leveraging the power of the web to keep your pets safe and healthy',
        theme_color: '#000',
        background_color: '#fff',
        icons: [
          {
            src: 'icons/any/android-launchericon-192-192.png',
            sizes: '192x192',
            type: 'image/png',
            purpose: 'any'
          },
          {
            src: 'icons/any/android-launchericon-512-512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any'
          },
          {
            src: 'icons/maskable/android-launchericon-192-192.png',
            sizes: '192x192',
            type: 'image/png',
            purpose: 'maskable'
          },
          {
            src: 'icons/maskable/android-launchericon-512-512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable'
          }          
        ]
      }      
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
