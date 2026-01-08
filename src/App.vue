<template>
  <el-container class="layout-container">
    
    <el-header class="header-box">
      <el-menu
        :default-active="activeIndex"
        mode="horizontal"
        background-color="#333"
        text-color="#fff"
        active-text-color="#ffd04b"
        :ellipsis="false" 
        router
        style="border:0;"
      >
        <el-menu-item index="/">
          <span style="font-size: 20px; font-weight: bold; margin-right: 10px;">🦾</span>
          <span style="font-weight: bold;">陆合枪汇</span>
        </el-menu-item>
        <div class="flex-grow" /> <el-menu-item index="/">主页</el-menu-item>
        <el-menu-item index="/rank">排行榜</el-menu-item>
        <el-menu-item index="/activity">活动记录</el-menu-item>
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

const route = useRoute()
const activeIndex = ref('/')

// 监听路由变化，自动高亮对应的菜单项
watch(() => route.path, (newPath) => {
  activeIndex.value = newPath
})
</script>

<style>
/* 1. 全局盒子模型重置：这是工程化开发的标配，防止 padding 撑大盒子 */
* {
  box-sizing: border-box;
}

/* 2. 基础设置 */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  /* 这里的背景色是为了防止滚动过快时出现白底 */
  background-color: #f0f2f5; 
}

/* 3. 关键修改：#app 不要设 height: 100%，否则内容多了背景会断 */
#app {
  min-height: 100vh; /* 至少占满一屏，内容多自动长高 */
  display: flex;
  flex-direction: column;
}

/* 布局容器 */
.layout-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header */
.header-box {
  padding: 0;
  background-color: #333;
  /* 加上 z-index 确保它永远浮在内容上面（可选） */
  position: relative;
  z-index: 100;
}

/* Main 内容区 */
.main-box {
  flex-grow: 1; /* 自动撑满剩余空间 */
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f0f2f5;
  /* 防止内容溢出产生横向滚动条 */
  overflow-x: hidden; 
}

/* Footer 底部栏 */
.footer-box {
  text-align: center;
  background-color: #2c3e50;
  color: #fff;
  /* 调整一下 padding，让它看起来更紧凑一点，不再那么松散 */
  padding: 30px 20px; 
  width: 100%;
}

/* 4. 新增：强制去掉 Footer 里面 p 标签的默认边距，消除“缝隙” */
.footer-box p {
  margin: 5px 0; /* 给一点点行间距即可 */
  line-height: 1.5; /* 优化阅读体验 */
}

/* 占位符 */
.flex-grow {
  flex-grow: 1;
}
</style>