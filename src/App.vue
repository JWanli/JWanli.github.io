<template>
  <el-container class="layout-container">
    
    <el-header class="header-box glass-header">
      
      <!-- 1. 左侧 Logo (独立区域，点击回主页) -->
      <div class="logo-wrapper absolute-left" @click="$router.push('/')">
        <img :src="logoUrl" class="header-logo" alt="Logo" />
        <span class="logo-text">大枪等级分</span>
      </div>

      <!-- 2. 中间 导航菜单 -->
      <el-menu
        :default-active="activeIndex"
        mode="horizontal"
        :ellipsis="false" 
        router
        class="custom-menu"
      >
        <div class="center-nav">
          <el-menu-item index="/">主页</el-menu-item>
          <el-menu-item index="/rank">排行榜</el-menu-item>
          <el-menu-item index="/info">信息</el-menu-item>
        </div>
      </el-menu>

      <!-- 3. 右侧 开关 (独立区域) -->
      <div class="right-actions absolute-right">
        <div class="theme-switch-wrapper">
          <el-switch
            v-model="isDark"
            inline-prompt
            :active-icon="Moon"
            :inactive-icon="Sunny"
            class="premium-switch"
          />
        </div>
      </div>

    </el-header>

    <el-main class="main-box">
      <router-view v-slot="{ Component }">
        <transition name="slide-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>

    <el-footer class="footer-box">
      <p>
        © 2026 JWanli Engineering.
        <br class="mobile-break"> 
        Powered by 
        <el-link type="primary" :underline="false" href="https://vuejs.org/" target="_blank">Vue 3</el-link> 
        & 
        <el-link type="success" :underline="false" href="https://element-plus.org/" target="_blank">Element Plus</el-link>
      </p>
      <p class="footer-sub">
        本站源码托管于 GitHub Pages | 大枪对抗
      </p>
    </el-footer>

  </el-container>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDark } from '@vueuse/core'
import logoUrl from './assets/logo.jpg' // 引入图片

import { Moon, Sunny } from '@element-plus/icons-vue'

const route = useRoute()
const activeIndex = ref('/')

const isDark = useDark()

watch(() => route.path, (newPath) => {
  activeIndex.value = newPath
})
</script>

<style>
/* === 1. 全局配置 === */
:root {
  --header-height: 64px;
  --glass-bg-light: rgba(255, 255, 255, 0.9); /* 稍微增加不透明度，提升质感 */
  --glass-bg-dark: rgba(28, 28, 30, 0.9);
  --border-light: rgba(0, 0, 0, 0.05);
  --border-dark: rgba(255, 255, 255, 0.1);
}

* {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Helvetica, sans-serif;
  background-color: var(--el-bg-color-page);
  color: var(--el-text-color-primary);
  /* 修复：只保留 html 的滚动能力，防止滚动冲突 */
  overflow-y: auto; 
}

/* 补充：确保 body 不产生额外的滚动条容器，而是随内容撑开 */
body {
  overflow-y: visible;
}

#app, .layout-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* === 2. Header === */
.header-box.glass-header {
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  height: var(--header-height);
  background-color: var(--glass-bg-light) !important;
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid var(--border-light);
  /* 确保 header 是相对定位容器，给子元素的 absolute 提供参照 */
  position: sticky; 
  display: flex; /* 主要是为了让 absolute 的子元素相对于它定位 */
  align-items: center;
  justify-content: center;
}

html.dark .header-box.glass-header {
  background-color: var(--glass-bg-dark) !important;
  border-bottom: 1px solid var(--border-dark);
}

/* 中间菜单 */
.custom-menu {
  border-bottom: none !important;
  background-color: transparent !important;
  height: 100%;
  /* menu 不需要 width 100%，它只需要包裹 center-nav */
  width: auto; 
  display: flex;
  align-items: center;
}

.center-nav {
  display: flex;
  align-items: center;
  height: 100%;
}

/* 绝对定位区域 */
.absolute-left {
  position: absolute;
  left: 24px;
  top: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  z-index: 10;
}

.absolute-right {
  position: absolute;
  right: 24px;
  top: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  z-index: 10;
}

/* 导航项样式 (恢复浅蓝色选中态) */
.el-menu--horizontal > .center-nav > .el-menu-item {
  border-bottom: none !important;
  color: var(--el-text-color-regular);
  font-weight: 500;
  font-size: 15px;
  height: 38px !important; 
  line-height: 38px !important;
  margin: 0 4px;
  border-radius: 12px; /* 稍微方一点的圆角，更现代 */
  transition: all 0.2s ease-in-out;
  padding: 0 20px !important;
}

.el-menu--horizontal > .center-nav > .el-menu-item:hover {
  background-color: rgba(0, 0, 0, 0.04) !important;
  color: var(--el-color-primary) !important;
}
html.dark .el-menu--horizontal > .center-nav > .el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.08) !important;
}

/* 关键：恢复浅蓝色高亮 */
.el-menu--horizontal > .center-nav > .el-menu-item.is-active {
  background-color: var(--el-color-primary-light-9) !important;
  color: var(--el-color-primary) !important;
  font-weight: 600;
}
html.dark .el-menu--horizontal > .center-nav > .el-menu-item.is-active {
  background-color: rgba(64, 158, 255, 0.2) !important;
  color: #409eff !important;
}

/* Logo 样式 */
.logo-wrapper {
  cursor: pointer;
  transition: opacity 0.2s;
  user-select: none;
}
.logo-wrapper:hover {
  opacity: 0.7;
}

.logo-emoji {
  font-size: 26px;
  margin-right: 8px;
  display: none; /* 隐藏原来的 emoji */
}

/* 新增 Logo 图片样式 */
.header-logo {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  margin-right: 10px;
  object-fit: cover;
}

.logo-text {
  font-size: 19px;
  font-weight: 700;
  letter-spacing: -0.5px;
  color: var(--el-text-color-primary);
}

/* 开关样式 */
.premium-switch {
  --el-switch-on-color: #333;
  --el-switch-off-color: #e5e5ea;
}

/* === 3. 内容区与页脚 === */
.main-box {
  flex-grow: 1; 
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px;
  /* 关键修复：覆盖 el-main 默认的 overflow: auto，消除双重滚动条 */
  overflow-x: hidden; 
  overflow-y: visible !important; 

  min-height: 0; /* ✅ 新增：允许子页面内部滚动容器正常工作 */
}

.footer-box {
  text-align: center;
  background-color: transparent;
  border-top: 1px solid var(--border-light);
  color: var(--el-text-color-secondary);
  padding: 40px 20px;
  font-size: 13px;
}
html.dark .footer-box { border-top: 1px solid var(--border-dark); }
.mobile-break { display: none; }

/* === 页面切换动画 === */
.slide-fade-enter-active, .slide-fade-leave-active {
  transition: opacity 0.4s ease, transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.slide-fade-enter-from { opacity: 0; transform: scale(0.98) translateY(10px); }
.slide-fade-leave-to { opacity: 0; }

/* === 📱 移动端适配 === */
@media (max-width: 768px) {
  .header-box.glass-header {
    justify-content: space-between;
    padding: 0 12px;
  }
  
  /* 1. 左右两侧：取消绝对定位，设为固定宽度以保证中间绝对居中 */
  .absolute-left, .absolute-right {
    position: static !important; /* 关键：取消绝对定位，回归文档流 */
    width: 60px;  /* 关键：设置相同的宽度，确保两边对称，从而让中间菜单视觉居中 */
    flex-shrink: 0;
    display: flex;
    align-items: center;
  }

  .absolute-left { justify-content: flex-start; } /* Logo 靠左 */
  .absolute-right { justify-content: flex-end; } /* 开关 靠右 */
  
  /* 2. 中间菜单：Flex 自适应占据剩余空间 */
  .custom-menu {
    position: static;
    transform: none;
    flex: 1; /* 占据左右剩下的所有空间 */
    justify-content: center;
    margin: 0 4px;
    width: 0; /* 防止 flex 子项溢出 */
    padding: 0; 
  }

  /* 确保内部容器也是居中的 */
  .center-nav {
    width: 100%;
    justify-content: center;
  }

  /* 3. 移动端 Logo 调整 */
  .logo-text { display: none; }
  .logo-emoji { font-size: 24px; margin-right: 0; }
  
  /* 4. 移动端导航项微调 */
  .el-menu--horizontal > .center-nav > .el-menu-item {
    font-size: 14px;
    padding: 0 8px !important; /* 缩小内边距 */
    height: 34px !important;
    line-height: 34px !important;
    margin: 0 1px;
    border-radius: 8px;
  }
  
  /* 5. 主内容区去边距 */
  .main-box { padding: 20px 0px; }
  .mobile-break { display: block; }
}
</style>