import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-vue': ['vue', 'vue-router'],
          // Element Plus 改为按需引入后，这个 chunk 可能会显著变小
          'vendor-element-plus': ['element-plus', '@element-plus/icons-vue'],
          'vendor-supabase': ['@supabase/supabase-js'],
          // Profile 页面会用到 ECharts；配合路由懒加载可进一步避免进首屏 chunk
          'vendor-echarts': ['echarts', 'vue-echarts'],
        },
      },
    },
  },
})
