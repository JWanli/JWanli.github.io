<template>
  <div class="leaderboard-container">
    <div class="header">
      <h2 class="title">🏆 综合排行榜</h2>
      <p class="subtitle">实时更新 • 实力见证</p>
    </div>

    <el-card class="box-card" shadow="hover">
      <el-table 
        v-loading="loading" 
        :data="tableData" 
        style="width: 100%" 
        :row-style="{ height: isMobile ? '50px' : '65px' }" 
        stripe
        :size="isMobile ? 'small' : 'default'"
        :default-sort="{ prop: 'current_elo', order: 'descending' }"
        class="custom-table"
      >
        
        <!-- 1. 排名 -->
        <el-table-column type="index" label="排名" :width="isMobile ? 38 : 80" align="center">
          <template #default="scope">
            <div class="rank-badge" :class="getRankClass(scope.$index)">
              {{ scope.$index + 1 }}
            </div>
          </template>
        </el-table-column>

        <!-- 2. 选手：自适应 -->
        <el-table-column label="选手" min-width="90">
          <template #default="scope">
            <div class="player-cell" @click="goToProfile(scope.row.id)">
              <el-avatar :size="isMobile ? 32 : 44" :src="scope.row.avatar_url" class="avatar">
                {{ scope.row.name.charAt(0) }}
              </el-avatar>
              
              <div class="name-info">
                <span class="main-name">{{ scope.row.name }}</span>
                <span v-if="!isMobile && scope.row.nick_name" class="sub-name">{{ scope.row.nick_name }}</span>
              </div>
            </div>
          </template>
        </el-table-column>

        <!-- 3. 等级：去除 label 文字 -->
        <el-table-column label="" :width="isMobile ? 30 : 100" align="center">
          <template #default="scope">
            <div 
              v-if="scope.row.grade > 0"
              class="level-box" 
              :class="getLevelClass(scope.row.grade)"
            >
              {{ scope.row.grade }}
            </div>
            <span v-else class="no-level" style="font-size: 12px; color: #ddd;">•</span>
          </template>
        </el-table-column>

        <!-- 4. 地区：略微缩小移动端宽度 -->
        <el-table-column prop="region" label="地区" :width="isMobile ? 50 : 120" align="center" show-overflow-tooltip>
          <template #default="scope">
            <span class="region-text" :style="{ fontSize: isMobile ? '12px' : '15px' }">
              {{ scope.row.region || '-' }}
            </span>
          </template>
        </el-table-column>

        <!-- 5. 分数：宽度微增，确保"分数"二字不换行 -->
        <el-table-column prop="current_elo" label="分数" :width="isMobile ? 55 : 140" sortable align="center">
          <template #default="scope">
            <span class="elo-text">{{ scope.row.current_elo }}</span>
          </template>
        </el-table-column>

        <!-- 6. 活跃度：改为"活跃"，宽度微增 -->
        <el-table-column prop="activity" label="活跃" :width="isMobile ? 45 : 140" sortable align="center">
          <template #default="scope">
            <!-- 电脑端：进度条 -->
            <div v-if="!isMobile" class="activity-cell">
              <el-progress 
                :percentage="scope.row.activity || 0" 
                :color="getActivityColor(scope.row.activity)"
                :stroke-width="6"
                :show-text="false"
                class="custom-progress"
              />
              <span class="activity-num">{{ scope.row.activity || 0 }}%</span>
            </div>
            <!-- 手机端：纯数字 -->
            <span 
              v-else 
              style="font-size: 12px; font-weight: bold;" 
              :style="{ color: getActivityColor(scope.row.activity) }"
            >
              {{ scope.row.activity || 0 }}
            </span>
          </template>
        </el-table-column>

      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue' 
import { useRouter } from 'vue-router'
import { supabase } from '../supabase'
import { useWindowSize } from '@vueuse/core'

const router = useRouter()
const loading = ref(true)
const tableData = ref([])

const { width } = useWindowSize()
const isMobile = computed(() => width.value < 768) 

const fetchData = async () => {
  loading.value = true
  try {
    const { data, error } = await supabase
      .from('players')
      .select('id, name, nick_name, region, current_elo, avatar_url, activity, grade')
      .order('current_elo', { ascending: false })

    if (error) throw error
    tableData.value = data
  } catch (err) {
    console.error('获取排名失败:', err)
  } finally {
    loading.value = false
  }
}

const goToProfile = (id) => {
  router.push(`/profile/${id}`)
}

const getRankClass = (index) => {
  if (index === 0) return 'rank-1' 
  if (index === 1) return 'rank-2' 
  if (index === 2) return 'rank-3' 
  return 'rank-normal'             
}

const getLevelClass = (grade) => {
  if (grade === 1) return 'level-l1'    
  if (grade === 2) return 'level-l2'  
  if (grade === 3) return 'level-l3'    
  if (grade === 4) return 'level-l4'    
  if (grade === 5) return 'level-l5'
  return 'level-l5'
}

const getActivityColor = (val) => {
  if (!val) return '#dcdfe6'
  if (val >= 80) return '#67C23A'
  if (val >= 50) return '#E6A23C'
  return '#F56C6C'
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
/* 引入更加清晰的字体栈 */
.leaderboard-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 30px 20px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}
.title {
  font-size: 32px;
  color: #1a1a1a;
  margin-bottom: 8px;
  font-weight: 800; /* 加粗标题 */
  letter-spacing: -0.5px;
  transition: color 0.3s;
}
.subtitle {
  color: #888;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.3s;
}

/* === 排名徽章 (这里修改不同Rank的配色) === */
.rank-badge {
  width: 28px;
  height: 28px;
  line-height: 28px;
  border-radius: 6px; /* 方圆角，更现代 */
  margin: 0 auto;
  font-weight: 800;
  font-size: 14px;
  color: #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

/* 🥇 冠军色 */
.rank-1 {
  background: linear-gradient(135deg, #FFD700 0%, #FDB931 100%);
  text-shadow: 0 1px 1px rgba(0,0,0,0.2);
  transform: scale(1.1); /* 冠军稍微大一点 */
}
/* 🥈 亚军色 */
.rank-2 {
  background: linear-gradient(135deg, #E0E0E0 0%, #BDBDBD 100%);
  color: #555;
}
/* 🥉 季军色 */
.rank-3 {
  background: linear-gradient(135deg, #CD7F32 0%, #A0522D 100%);
}
/* 普通排名 */
.rank-normal {
  background: transparent;
  color: #909399;
  box-shadow: none;
  font-weight: 600;
}

/* === 选手信息 === */
.player-cell {
  display: flex;
  align-items: center;
  cursor: pointer;
}
.avatar {
  margin-right: 15px;
  border: 2px solid #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: border-color 0.3s;
}
.name-info {
  display: flex;
  flex-direction: row; 
  align-items: baseline; 
  gap: 8px;
  /* 手机端防止溢出 */
  flex-wrap: wrap; 
}
.main-name {
  font-weight: 700;
  font-size: 16px;
  color: #2c3e50;
  transition: color 0.3s;
}
.sub-name {
  font-size: 16px;
  color: #909399;  /* 使用浅灰色区分 */
  font-weight: 400;
  transition: color 0.3s;
}

/* === 等级方框 (这里改 Lv 方块的样式) === */
.level-box {
  display: inline-block;
  width: 24px;   /* 固定宽度 */
  height: 24px;  /* 固定高度 */
  line-height: 24px; /* 垂直居中 */
  font-size: 14px;
  font-weight: 700;
  border-radius: 2px; /* 极小的圆角，接近正方形 */
  text-align: center;
  color: #fff; /* 所有等级文字统一为白色 */
}
.level-l5   { background: #dcdfe6; }
.level-l4   { background: #94c5b4; }
.level-l3   { background: #6d9cc1; }
.level-l2   { background: #9b8dca; }
.level-l1   { background: #a46f63; }

/* === 地区 === */
/* 去掉背景胶囊样式，改为清晰的纯文本 */
.region-text {
  font-size: 15px;
  color: #303133;
  font-weight: 500;
  transition: color 0.3s;
}

/* === Elo 分数 (重点优化) === */
.elo-text {
  font-family: "Roboto Mono", "Menlo", monospace; 
  font-weight: 700;
  color: #2c3e50;
  font-size: 17px;
  letter-spacing: -0.5px;
  transition: color 0.3s;
}

/* 📱 手机端样式微调 */
@media (max-width: 768px) {
  /* 去除容器内边距，实现无边框效果 */
  .leaderboard-container {
    padding: 0; 
    max-width: 100%;
  }

  /* 去除卡片的边框和阴影，让表格贴边 */
  .box-card {
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
  }
  
  .header {
    margin: 20px 0 10px 0; /* 调整头部间距 */
  }
  
  .title {
    font-size: 24px; /* 标题改小 */
  }

  /* 这种超紧凑模式下，分数需要很小 */
  .elo-text {
    font-size: 13px; 
  }

  /* 调整头像在手机上的右边距 */
  .avatar {
    margin-right: 6px;
  }

  /* 名字字体 */
  .main-name {
    font-size: 13px;
    line-height: 1.2;
  }

  /* 等级盒子缩小 */
  .level-box {
    width: 18px;
    height: 18px;
    line-height: 18px;
    font-size: 12px;
  }
  
  /* === 🔥 重写表头样式，解决文字显示不全问题 === */
  
  /* 强制减小表头单元格 padding */
  :deep(.el-table__header-wrapper th .cell) {
    padding: 0 1px !important;  /* 左右几乎不留缝隙 */
    font-size: 11px !important; /* 字体缩小 */
    line-height: 1.2;
    display: flex;              /* 使用 Flex 布局让文字和图标挤在一起 */
    justify-content: center;
    align-items: center;
    font-weight: 600;
  }

  /* 缩小排序小箭头的占位宽度 */
  :deep(.el-table .caret-wrapper) {
    width: 11px !important;
    margin-left: 0px !important; 
  }
  
  /* 调整排序小箭头的形状大小 */
  :deep(.el-table .sort-caret) {
    border-width: 4px !important;
  }
}

/* === 活跃度 === */
.activity-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}
.custom-progress {
  width: 60px;
}
.activity-num {
  font-size: 12px;
  color: #909399;
  font-family: monospace;
}

/* === 🌙 夜间模式适配 (Dark Mode) === */
html.dark .title {
  color: #E5EAF3; /* Element Plus Text Primary Dark */
}

html.dark .subtitle {
  color: #A3A6AD; /* Element Plus Text Secondary Dark */
}

html.dark .main-name {
  color: #E5EAF3;
}

html.dark .sub-name {
  color: #A3A6AD;
}

html.dark .region-text {
  color: #E5EAF3;
}

html.dark .elo-text {
  color: #E5EAF3;
}

html.dark .rank-normal {
  color: #A3A6AD;
}

html.dark .avatar {
  border-color: #363637; /* 深色边框，避免白色突兀 */
  background-color: #2b2b2b;
}

html.dark-l5 {
  background: #4C4D4F; /* 深色模式下的L5背景 */
  color: #b1b3b8;
}

/* 如果有需要，可以针对不同等级在深色模式下进行微调，
   但目前的彩色方块在深色背景下通常也很好看，所以保持原样。
   唯一可能需要调整的是 L5 (灰色)，上面已处理。
*/
</style>