<template>
  <div class="leaderboard-container">
    <div class="header">
      <h2 class="title">🏆 综合排行榜</h2>
      <p class="subtitle">实时更新 • 实力见证</p>
    </div>

    <div class="table-frame">
      <el-table 
        v-loading="loading" 
        :data="tableData" 
        style="width: 100%" 
        stripe
        :size="isMobile ? 'small' : 'default'"
        :default-sort="{ prop: 'current_elo', order: 'descending' }"
        class="custom-table"
        @sort-change="handleSortChange"
        @row-click="handleRowClick"
      >
        
        <!-- 1. 排名：调小宽度 -->
        <el-table-column type="index" label="排名" :width="isMobile ? 42 : 70" align="center">
          <template #default="scope">
            <div class="rank-badge" :class="getRankClass(scope.$index)">
              {{ scope.$index + 1 }}
            </div>
          </template>
        </el-table-column>

        <!-- 2. 升降：图标调小，列宽微调 -->
        <el-table-column
          label=""
          :width="isMobile ? 20 : 30"
          align="center"
          class-name="rank-change-col"
        >
          <template #default="scope">
            <span
              v-if="scope.row.rank_change"
              class="rank-change"
              :class="getRankChangeClass(scope.row.rank_change)"
            >
              {{ scope.row.rank_change }}
            </span>
          </template>
        </el-table-column>

        <!-- 3. 选手：自适应 -->
        <el-table-column label="选手" min-width="90">
          <template #default="scope">
            <!-- 移除 div 上的 @click，交由 tr 统一处理 -->
            <div class="player-cell">
              <el-avatar :size="isMobile ? 32 : 44" :src="scope.row.avatar_url" class="avatar">
                {{ scope.row.name.charAt(0) }}
              </el-avatar>
              
                  <div class="name-info">
                    <span class="main-name">{{ scope.row.name }}</span>
                    <span v-if="scope.row.nick_name" class="sub-name">
                      {{ scope.row.nick_name }}
                    </span>
                  </div>
            </div>
          </template>
        </el-table-column>

        <!-- 4. 等级：PC端宽度缩小到 70 (原100) -->
        <el-table-column label="" :width="isMobile ? 26 : 70" align="center">
          <template #default="scope">
            <div 
              v-if="scope.row.grade > 0"
              class="level-box" 
              :class="getLevelClass(scope.row.grade)"
            >
              {{ scope.row.grade }}
            </div>
          </template>
        </el-table-column>

        <!-- 5. 地区：微调宽度 -->
        <el-table-column prop="region" label="地区" :width="isMobile ? 42 : 100" align="center" show-overflow-tooltip>
          <template #default="scope">
            <span class="region-text" :style="{ fontSize: isMobile ? '12px' : '15px' }">
              {{ scope.row.region || '-' }}
            </span>
          </template>
        </el-table-column>

        <!-- 6. 分数：微调宽度 -->
        <el-table-column 
          prop="current_elo" 
          label="分数" 
          :width="isMobile ? 48 : 100" 
          sortable 
          :sort-orders="['descending', 'ascending', null]"
          align="center"
        >
          <template #default="scope">
            <span class="elo-text">{{ scope.row.current_elo }}</span>
          </template>
        </el-table-column>

        <!-- 7. 活跃度：加宽一点点防止表头换行 -->
        <el-table-column 
          prop="activity" 
          label="活跃" 
          :width="isMobile ? 56 : 120" 
          sortable="custom" 
          :sort-orders="['descending', 'ascending', null]"
          align="center"
        >
          <template #default="scope">
            <!-- 电脑/iPad端：进度条 -->
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
    </div>
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

// === 核心修改逻辑 ===
// 1. isMobile: 严格限制在 < 768px (手机)，这样 iPad 会进入桌面排版
const isMobile = computed(() => width.value < 768) 

// 2. isTablet: 定义 768px ~ 1100px 为平板或小屏笔记本区间
// 在这个区间内，我们隐藏次要信息(如昵称)，保证主要信息不换行
const isTablet = computed(() => width.value >= 768 && width.value < 1100)

// 处理表格排序
const handleSortChange = ({ prop, order }) => {
  if (prop === 'activity') {
    tableData.value.sort((a, b) => {
      const actA = a.activity || 0
      const actB = b.activity || 0
      
      // 如果活跃度相同，则始终按 ELO 分数降序排列（分数高的在前）
      if (actA === actB) {
        return b.current_elo - a.current_elo
      }
      
      // 否则按活跃度排序
      // ascending: 升序 (小 -> 大)，descending: 降序 (大 -> 小)
      return order === 'ascending' ? actA - actB : actB - actA
    })
  }
}

// 新增：点击整行跳转
const handleRowClick = (row) => {
  goToProfile(row.id)
}

const fetchData = async () => {
  loading.value = true
  try {
    const { data, error } = await supabase
      .from('players')
      .select('id, name, nick_name, region, current_elo, avatar_url, activity, grade, rank_change')
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
  return 'rank-normal'
}

const getRankChangeClass = (val) => {
  if (val === '↑') return 'rank-change-up'
  if (val === '↓') return 'rank-change-down'
  if (val === '+') return 'rank-change-new'
  return 'rank-change-none'
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
.custom-table :deep(.el-table__header-wrapper th .cell) {
  font-size: 16px !important;
  font-weight: 800 !important;
  color: #303133 !important;
  letter-spacing: 0.2px;
  /* 强制表头不换行，这是解决“活跃”换行的关键 */
  white-space: nowrap !important;
}

/* 新增：让表格行显示为手指形状，提示可点击 */
.custom-table :deep(.el-table__row) {
  cursor: pointer;
  transition: background-color 0.2s; /* 增加简单的悬停过渡效果 */
}

/* 引入更加清晰的字体栈 */
.leaderboard-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 30px 20px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.table-frame {
  background: #fff;
  border-radius: 12px; /* 增加圆角 */
  overflow: hidden; /* 确保圆角不被内部元素遮挡 */
  /* 稍微轻一点的阴影，更接近原生 */
  box-shadow: 0 1px 4px rgba(0,0,0,0.05); 
  border: 1px solid #ebeef5; /* Element Plus 默认边框色 */
  transition: background-color 0.3s, border-color 0.3s;
}

html.dark .table-frame {
  background: #1d1e1f;
  border: 1px solid #434343; /* 深色边框 */
  box-shadow: 0 1px 4px rgba(0,0,0,0.2);
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
.rank-badge {
  width: 28px;
  height: 28px;
  line-height: 28px;
  border-radius: 6px; 
  margin: 0 auto;
  font-weight: 800;
  font-size: 14px;
  color: #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}


/* 普通排名 */
.rank-normal {
  background: transparent;
  color: #909399;
  box-shadow: none;
  font-weight: 600;
}
:deep(.rank-change-col .cell) {
  padding-left: 0 !important;
  padding-right: 0 !important;
  display: flex;
  justify-content: center;
  align-items: center;
}
.rank-change {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  line-height: 18px;
  font-weight: 900;
  font-size: 18px;
  border-radius: 4px;
  border: 1px solid transparent;
  box-sizing: border-box;
}

/* 手机端减小升降符号大小 */


/* ↑ 绿色 */
.rank-change-up {
  color: #67C23A;

}

/* ↓ 红色 */
.rank-change-down {
  color: #F56C6C;

}

/* + 黄色（新加入） */
.rank-change-new {
  color: #E6A23C;

}
.rank-change-none{ color: #C0C4CC; } /* 无变化 */
/* === 选手信息 === */
.player-cell {
  display: flex;
  align-items: center;
  /* cursor: pointer; 移除这里单独的 pointer */
  padding-left: 0px; /* ✅ 新增：整体右移一点 */
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
  /* 新增：强制不换行 */
  white-space: nowrap;
}
.sub-name {
  font-size: 16px;
  color: #909399;  /* 使用浅灰色区分 */
  font-weight: 400;
  transition: color 0.3s;
}

/* === 等级方块 (这里改 Lv 方块的样式) === */
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
  /* 1. 使用负 margin 抵消 App.vue 中 main-box 的 20px padding */
  .leaderboard-container {
    /* 修正：App.vue 在手机端 padding 已经是 0，所以这里不需要负 margin */
    margin-left: 0 !important;
    width: 100% !important;
    max-width: none !important;
    padding: 0 !important; /* 自身不留 padding */
    box-sizing: border-box;
  }

  /* 2. 标题也跟着拉宽了，稍微给点内边距 */
  .header {
    margin: 15px 0 10px 0;
    padding: 0 16px;
  }
  .title { font-size: 22px; }

  /* 3. 卡片设置 */
  .table-frame {
    /* 修正：去掉负margin，防止在极窄屏幕上出现横向滚动条，保证行宽一致 */
    margin: 0 !important; 
    width: 100% !important; 
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    border-left: none; /* 手机端去掉左右边框，增加可用空间 */
    border-right: none;
  }


  /* 这种超紧凑模式下，分数需要很小 */
  .elo-text {
    font-size: 13px; 
  }

  /* 调整头像在手机上的右边距 */
  .avatar {
    margin-right: 6px;
  }

  /* 名字信息竖向排列，防止挤压 */
  .name-info {
    flex-direction: column !important; /* 强制竖向 */
    align-items: flex-start !important;
    justify-content: center; /* 垂直居中 */
    gap: 0 !important;
    flex: 1; /* 占据剩余空间 */
    min-width: 0; /* 关键：允许 flex 子项缩小，配合 text-overflow */
    height: 36px; /* 固定高度，确保有没有昵称都占一样的高度 */
    overflow: hidden;
  }

  /* 名字字体 */
  .main-name {
    font-size: 13px;
    line-height: 1.4;
    white-space: nowrap;
    width: 100%;
    overflow: hidden;
    text-overflow: ellipsis; /* 超长省略 */
  }

  /* ✅ 新增：手机端显示昵称时，字体调小 */
  .sub-name {
    font-size: 11px; /* 再调小一点，且作为副标题在下方显示 */
    color: #909399;
    white-space: nowrap;
    width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.2;
    margin-top: 0;
  }
  
  /* 强制固定行高，防止有无昵称出现高度差 */
  :deep(.el-table__row) {
    height: 58px !important;
  }

  .rank-change {
    font-size: 14px;
    width: 14px;
    height: 14px;
    line-height: 14px;
  }

  /* 强制压缩表格单元格的左右 padding，挤出空间给名字 */
  :deep(.el-table .cell) {
    padding: 0 2px !important;
  }
  
  /* 优化：第一列和最后一列增加边距，防止贴边 */
  :deep(.el-table__header-wrapper th:first-child .cell),
  :deep(.el-table__body-wrapper td:first-child .cell) {
    padding-left: 10px !important;
  }
  :deep(.el-table__header-wrapper th:last-child .cell),
  :deep(.el-table__body-wrapper td:last-child .cell) {
    padding-right: 10px !important;
  }
  
  /* 🔴 修复表头样式，确保活跃不换行 */
  :deep(.el-table__header-wrapper th .cell) {
    padding: 0 1px !important;  /* 左右缝隙 */
    font-size: 13px !important; /* 🔴 调小字体 */
    font-weight: 700;
    line-height: 1.2;
  display: flex;
  align-items: center;
    font-weight: 600;
}

  /* ✅ 新增：只有原本设定为居中的列（即包含 is-center 类的 th），才强制 flex 居中 */
  /* 这样“选手”列没有 is-center，就会默认保持左对齐 */
  :deep(.el-table__header-wrapper th.is-center .cell) {
  justify-content: center;
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

html.dark .custom-table :deep(.el-table__header-wrapper th .cell) {
  color: #E5EAF3 !important;
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