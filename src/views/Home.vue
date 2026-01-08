<template>
  <div class="page-container home-content">
    
    <img :src="logoImage" alt="Logo" class="my-logo" />

    <h1>👋 欢迎来到 陆合枪汇</h1>
    <p class="subtitle">这里记录大枪等级分、竞技赛事活动以及我的个人思考。</p>
    
    <div class="intro-box">
      <h3>🛠️ 关于陆合枪汇</h3>
      <p>本项目基于 Vue 3 + Vite 构建，旨在打造一个轻量级、可视化的武术数据发布平台。</p>
    </div>
  </div>
</template>

<script setup>
// 引用图片：确保 src/assets/ 下面真的有 liuhelogo.png 这个文件
import logoImage from '../assets/liuhelogo.png' 
</script>

<style scoped>
/* 把两个 style 合并成一个了，看起来更干净 */
.home-content {
  text-align: center;
  padding: 40px;
}

.my-logo {
  width: 120px;
  height: 120px;
  border-radius: 0%; /* 圆形头像 */
  object-fit: cover;  /* 防止图片变形 */
  margin-bottom: 20px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1); /* 加点阴影 */
  border: 2px solid #eee; /* 给图片加个细边框，更好看 */
}

.subtitle {
  color: #666;
  font-size: 1.2em;
  margin-bottom: 30px;
}

.intro-box {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  display: inline-block;
  text-align: left;
  max-width: 600px; /* 限制一下文字框的最大宽度，防止太宽读着累 */
}
</style>