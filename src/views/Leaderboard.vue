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
        :row-style="{ height: '65px' }" 
        stripe
        :default-sort="{ prop: 'current_elo', order: 'descending' }"
      >
        
        <!-- 调整排名列宽度，手机上更窄 -->
        <el-table-column type="index" label="排名" :width="isMobile ? 50 : 80" align="center">
          <template #default="scope">
            <div class="rank-badge" :class="getRankClass(scope.$index)">
              {{ scope.$index + 1 }}
            </div>
          </template>
        </el-table-column>

        <el-table-column label="选手" min-width="140">
          <template #default="scope">
            <div class="player-cell" @click="goToProfile(scope.row.id)">
              <el-avatar :size="isMobile ? 36 : 44" :src="scope.row.avatar_url" class="avatar">
                {{ scope.row.name.charAt(0) }}
              </el-avatar>
              
              <div class="name-info">
                <span class="main-name">{{ scope.row.name }}</span>
                <!-- 手机上名字太长可以考虑换行，这里暂时保持横向 -->
                <span v-if="scope.row.nick_name" class="sub-name">{{ scope.row.nick_name }}</span>
              </div>
            </div>
          </template>
        </el-table-column>

        <!-- 📱 手机端隐藏：等级 -->
        <el-table-column v-if="!isMobile" label="等级" width="100" align="center">
          <template #default="scope">
            <div 
              v-if="scope.row.grade > 0"
              class="level-box" 
              :class="getLevelClass(scope.row.grade)"
            >
              {{ scope.row.grade }}
            </div>
            <span v-else class="no-level">-</span>
          </template>
        </el-table-column>

        <!-- 📱 手机端隐藏：地区 -->
        <el-table-column v-if="!isMobile" prop="region" label="地区" width="120" align="center">
          <template #default="scope">
            <span class="region-text">{{ scope.row.region || '-' }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="current_elo" label="分数" :width="isMobile ? 80 : 140" sortable align="center">
          <template #default="scope">
            <span class="elo-text">{{ scope.row.current_elo }}</span>
          </template>
        </el-table-column>

        <!-- 📱 手机端隐藏：活跃度 -->
        <el-table-column v-if="!isMobile" prop="activity" label="活跃度" width="140" sortable align="center">
          <template #default="scope">
            <div class="activity-cell">
              <el-progress 
                :percentage="scope.row.activity || 0" 
                :color="getActivityColor(scope.row.activity)"
                :stroke-width="6"
                :show-text="false"
                class="custom-progress"
              />
              <span class="activity-num">{{ scope.row.activity || 0 }}%</span>
            </div>
          </template>
        </el-table-column>

      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue' // 引入 computed
import { useRouter } from 'vue-router'
import { supabase } from '../supabase'
import { useWindowSize } from '@vueuse/core' // 引入窗口尺寸检测

const router = useRouter()
const loading = ref(true)
const tableData = ref([])

// 📱 响应式检测移动端
const { width } = useWindowSize()
const isMobile = computed(() => width.value < 768) // 小于768px视为移动端

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

// === 样式逻辑控制 ===

// 1. 排名颜色逻辑
const getRankClass = (index) => {
  if (index === 0) return 'rank-1' // 冠军
  if (index === 1) return 'rank-2' // 亚军
  if (index === 2) return 'rank-3' // 季军
  return 'rank-normal'             // 普通
}

// 2. 等级方框颜色逻辑 (你可以根据需求修改这里的数字门槛)
const getLevelClass = (grade) => {
  if (grade === 1) return 'level-l1'    
  if (grade === 2) return 'level-l2'  
  if (grade === 3) return 'level-l3'    
  if (grade === 4) return 'level-l4'    
  if (grade === 5) return 'level-l5'
  return 'level-l5'
}

// 3. 活跃度颜色
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
  .leaderboard-container {
    padding: 15px 5px; /* 减少容器边距 */
  }
  
  .header {
    margin-bottom: 20px;
  }
  
  .title {
    font-size: 24px; /* 标题改小 */
  }

  .elo-text {
    font-size: 15px; /* 分数改小 */
  }

  /* 调整头像在手机上的右边距 */
  .avatar {
    margin-right: 8px;
  }

  .main-name {
    font-size: 14px;
  }
  
  .sub-name {
    font-size: 12px;
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