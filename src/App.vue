<template>
  <el-container class="layout-container">
    
    <el-header class="header-box">
      <el-menu
        :default-active="activeIndex"
        mode="horizontal"
        :ellipsis="false" 
        router
        class="custom-menu"
      >
        <el-menu-item index="/">
          <span style="font-size: 20px; font-weight: bold; margin-right: 10px;">🦾</span>
          <span style="font-weight: bold;">陆合枪汇</span>
        </el-menu-item>
        <div class="flex-grow" /> 
        <el-menu-item index="/">主页</el-menu-item>
        <el-menu-item index="/rank">排行榜</el-menu-item>
        <el-menu-item index="/activity">活动记录</el-menu-item>

        <div class="theme-switch-box">
          <el-switch
            v-model="isDark"
            inline-prompt
            :active-icon="Moon"
            :inactive-icon="Sunny"
            style="--el-switch-on-color: #4C4D4F; --el-switch-off-color: #dcdfe6"
          />
        </div>

      </el-menu>
    </el-header>

    <el-main class="main-box">
      <router-view v-slot="{ Component }">
        <transition name="el-fade-in-linear">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>

    <el-footer class="footer-box">
      <p>
        © 2026 JWanli Engineering. Powered by 
        <el-link type="primary" href="https://vuejs.org/" target="_blank">Vue 3</el-link> 
        & 
        <el-link type="success" href="https://element-plus.org/" target="_blank">Element Plus</el-link>
      </p>
      <p style="font-size: 12px; color: #999;">
        本站源码托管于 GitHub Pages | 传统武术
      </p>
    </el-footer>

  </el-container>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useDark } from '@vueuse/core'

import { Moon, Sunny } from '@element-plus/icons-vue'

const route = useRoute()
const activeIndex = ref('/')

const isDark = useDark()

watch(() => route.path, (newPath) => {
  activeIndex.value = newPath
})
</script>

<style>
/* 1. 全局重置 */
* {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  background-color: var(--el-bg-color-page); 
  color: var(--el-text-color-primary);
  /* 防止不同浏览器滚动条宽度不一致导致的抖动 */
  overflow-y: scroll; 
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.layout-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header */
.header-box {
  padding: 0;
  /* 背景色改用 var(--el-bg-color)，这样深色模式下它和 body 颜色一致，
     看起来就像没有缝隙了 
  */
  background-color: var(--el-bg-color);
  
  /* 如果你不想要标题栏下面那条灰色的线（看起来像缝隙），把下面这行删掉 */
  /* border-bottom: 1px solid var(--el-border-color); */
  
  position: relative;
  z-index: 100;
}

/* 这里的样式是为了让 Menu 背景透明，直接透出 header 的颜色 */
.custom-menu {
  border-bottom: none !important;
  background-color: transparent !important;
}

.theme-switch-box {
  display: flex;
  align-items: center;
  margin-left: 20px;
  height: 60px; /* 和 menu 高度一致 */
}

/* Main 内容区 */
.main-box {
  flex-grow: 1; 
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: var(--el-bg-color-page);
  overflow-x: hidden; 
}

/* Footer 底部栏 */
.footer-box {
  text-align: center;
  /* 使用 overlay 颜色，稍微比背景深一点点 */
  background-color: var(--el-bg-color-overlay);
  color: var(--el-text-color-regular);
  padding: 30px 20px; 
  width: 100%;
  /* 顶部留一条淡淡的线 */
  border-top: 1px solid var(--el-border-color-light);
}

.footer-box p {
  margin: 5px 0;
  line-height: 1.5;
}

.flex-grow {
  flex-grow: 1;
}
</style>