<template>
  <div class="app-layout">
    
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      background-color="#333"
      text-color="#fff"
      active-text-color="#ffd04b"
      router 
    >
      <el-menu-item index="/">
        <span style="font-weight: bold; font-size: 18px;">🦾 LAB DASHBOARD</span>
      </el-menu-item>
      
      <el-menu-item index="/">主页</el-menu-item>
      <el-menu-item index="/rank">🏆 排行榜</el-menu-item>
      <el-menu-item index="/activity">📅 活动信息</el-menu-item>
    </el-menu>

    <div class="main-content">
      <router-view />
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
// 当前激活的菜单项
const activeIndex = ref('/')
</script>

<style>
/* 全局简单的重置样式 */
body {
  margin: 0;
  padding: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  background-color: #f5f7fa;
}
.main-content {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto; /* 居中 */
}
.page-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>