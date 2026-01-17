<template>
  <div class="page-container home-content">
    
    <!-- 移除了原有的中间大图，因为已经移到左上角了 -->
    
    <div class="hero-section">
      <h1>🏆 大枪等级分 <span class="version-tag">Beta</span></h1>
      <p class="subtitle">基于 Elo 算法的古典武艺竞技对抗评估系统</p>
    </div>

    <div class="cards-layout">
      
      <!-- 原有的介绍板块，改为介绍等级分 -->
      <div class="intro-box info-card">
        <h3>📊 什么是大枪等级分？</h3>
        <p>这是一套旨在量化长枪竞技水平的数据系统。我们记录真实的实战与比赛结果，通过算法动态计算每位选手的战力值，直观呈现选手的竞技状态与成长轨迹。</p>
      </div>

      <!-- 新增：跳转排行榜的 Block -->
      <div class="intro-box action-card" @click="$router.push('/rank')">
        <div class="action-content">
          <h3>🚀 查看综合排行榜</h3>
          <p>点击浏览当前所有选手的实时排名、段位及地区分布。</p>
        </div>
        <div class="action-icon">➜</div>
      </div>

    </div>

  </div>
</template>

<script setup>
// 移除不再使用的图片引用
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<style scoped>
.home-content {
  text-align: center;
  padding: 60px 20px;
  max-width: 800px;
  margin: 0 auto;
}

.hero-section {
  margin-bottom: 50px;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: var(--el-text-color-primary);
  letter-spacing: -1px;
}

.version-tag {
  font-size: 0.4em;
  vertical-align: super;
  background-color: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
}

.subtitle {
  color: var(--el-text-color-secondary);
  font-size: 1.25em;
  margin-top: 10px;
  font-weight: 400;
}

/* 卡片布局 */
.cards-layout {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}

.intro-box {
  background: var(--el-fill-color); /* 保持原有背景色逻辑 */
  border: 1px solid var(--el-border-color); /* 保持原有边框逻辑 */
  padding: 24px;
  border-radius: 12px;
  text-align: left;
  width: 100%;
  max-width: 600px;
  transition: all 0.3s ease;
}

.intro-box h3 {
  color: var(--el-text-color-primary);
  margin-top: 0;
  font-size: 1.15rem;
  margin-bottom: 10px;
}

.intro-box p {
  color: var(--el-text-color-regular);
  margin-bottom: 0;
  line-height: 1.6;
}

/* 🟢 修改：跳转卡片的特殊样式 */
.action-card {
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--el-bg-color-overlay); /* 稍微突出一点 */
  border: 1px solid var(--el-border-color-darker); /* 稍微加深边框 */
  position: relative;
  overflow: hidden;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  border-color: var(--el-color-primary);
}

.action-card:hover h3 {
  color: var(--el-color-primary);
}

.action-icon {
  font-size: 24px;
  color: var(--el-text-color-placeholder);
  transition: transform 0.3s, color 0.3s;
  font-weight: bold;
}

.action-card:hover .action-icon {
  transform: translateX(4px);
  color: var(--el-color-primary);
}

/* 📱 移动端适配 */
@media (max-width: 768px) {
  .home-content {
    padding: 30px 15px;
  }
  
  h1 {
    font-size: 1.8rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }

  .intro-box {
    padding: 20px;
  }
}
</style>