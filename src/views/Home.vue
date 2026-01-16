<template>
  <div class="page-container home-content">
    
    <img :src="logoImage" alt="Logo" class="my-logo" />

    <!-- 修改：包裹“陆合枪汇”并添加类名 -->
    <h1>👋 欢迎来到 <span class="brand-name">陆合枪汇</span></h1>
    
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
  padding: 40px 20px;
}

/* 📱 移动端：减少内边距 */
@media (max-width: 768px) {
  .home-content {
    padding: 20px 10px;
  }
  
  .my-logo {
    width: 100px;
    height: 100px;
  }
  
  .intro-box {
    max-width: 100%; /* 占满宽度 */
  }
}

.my-logo {
  width: 120px;
  height: 120px;
  border-radius: 0%; /* 圆形头像 */
  object-fit: cover;  /* 防止图片变形 */
  margin-bottom: 20px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1); /* 加点阴影 */
  border: 2px solid var(--el-border-color);
}

.subtitle {
  /*color: #666;*/
  color: var(--el-text-color-secondary);
  font-size: 1.2em;
  margin-bottom: 30px;
}

.intro-box {
  /*background: #f8f9fa;*/
  background: var(--el-fill-color);
  border: 1px solid var(--el-border-color);
  padding: 20px;
  border-radius: 8px;
  display: inline-block;
  text-align: left;
  max-width: 600px; /* 限制一下文字框的最大宽度，防止太宽读着累 */
}
.intro-box h3 {
  color: var(--el-text-color-primary);
  margin-top: 0;
}
.intro-box p {
  color: var(--el-text-color-regular);
  margin-bottom: 0;
}

/* === 新增：品牌名称手机端换行处理 === */
.brand-name {
  display: inline; /* PC端默认行内显示 */
}

@media (max-width: 768px) {
  .brand-name {
    display: block; /* 手机端变为块级元素，强制换行 */
    margin-top: 4px; /* 增加一点行间距，更美观 */
  }
}
</style>