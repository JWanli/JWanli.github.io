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
        stripe
        :default-sort="{ prop: 'current_elo', order: 'descending' }"
      >
        
        <el-table-column type="index" label="排名" width="80" align="center">
          <template #default="scope">
            <div class="rank-badge" :class="'rank-' + (scope.$index + 1)">
              {{ scope.$index + 1 }}
            </div>
          </template>
        </el-table-column>

        <el-table-column label="选手" min-width="200">
          <template #default="scope">
            <div class="player-cell" @click="goToProfile(scope.row.id)">
              <el-avatar :size="40" :src="scope.row.avatar_url" class="avatar">
                {{ scope.row.name.charAt(0) }}
              </el-avatar>
              
              <div class="name-info">
                <div class="main-name">
                  {{ scope.row.name }}
                  <el-tag v-if="scope.row.grade > 0" size="small" type="warning" effect="dark" round style="margin-left: 5px; transform: scale(0.8);">
                    Lv.{{ scope.row.grade }}
                  </el-tag>
                </div>
                <div v-if="scope.row.nick_name" class="sub-name">
                  @{{ scope.row.nick_name }}
                </div>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="region" label="地区" width="120" align="center">
          <template #default="scope">
            <el-tag v-if="scope.row.region" type="info" size="small" effect="plain">
              {{ scope.row.region }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>

        <el-table-column prop="current_elo" label="大枪等级分" width="150" sortable align="center">
          <template #default="scope">
            <span class="elo-text">{{ scope.row.current_elo }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="activity" label="活跃度" width="150" sortable align="center">
          <template #default="scope">
            <div class="activity-cell">
              <el-progress 
                :percentage="scope.row.activity || 0" 
                :color="getActivityColor(scope.row.activity)"
                :stroke-width="8"
                :show-text="false"
              />
              <span class="activity-text">{{ scope.row.activity || 0 }}%</span>
            </div>
          </template>
        </el-table-column>

      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../supabase'

const router = useRouter()
const loading = ref(true)
const tableData = ref([])

// 获取数据
const fetchData = async () => {
  loading.value = true
  try {
    // 增加查询 nick_name, activity, grade
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

// 跳转详情
const goToProfile = (id) => {
  router.push(`/profile/${id}`)
}

// 活跃度颜色逻辑
const getActivityColor = (val) => {
  if (!val) return '#909399'
  if (val >= 80) return '#67C23A' // 绿色
  if (val >= 50) return '#E6A23C' // 黄色
  return '#F56C6C' // 红色
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.leaderboard-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}
.header {
  text-align: center;
  margin-bottom: 30px;
}
.title {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 5px;
}
.subtitle {
  color: #7f8c8d;
  font-size: 14px;
}

/* 排名徽章样式 */
.rank-badge {
  width: 24px;
  height: 24px;
  line-height: 24px;
  border-radius: 50%;
  background: #f0f2f5;
  color: #606266;
  margin: 0 auto;
  font-weight: bold;
  font-size: 12px;
}
.rank-1 { background: #FFD700; color: #fff; box-shadow: 0 2px 4px rgba(255, 215, 0, 0.4); }
.rank-2 { background: #C0C0C0; color: #fff; }
.rank-3 { background: #CD7F32; color: #fff; }

/* 选手列样式 */
.player-cell {
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: transform 0.2s;
}
.player-cell:hover {
  transform: translateX(5px);
}
.avatar {
  margin-right: 12px;
  background-color: #409EFF;
  flex-shrink: 0;
}
.name-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.main-name {
  font-weight: bold;
  font-size: 15px;
  color: #2c3e50;
  display: flex;
  align-items: center;
}
.sub-name {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}

/* Elo 分数样式 */
.elo-text {
  font-family: 'Roboto Mono', monospace;
  font-weight: bold;
  color: #409EFF;
  font-size: 16px;
}

/* 活跃度样式 */
.activity-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}
.activity-text {
  font-size: 12px;
  color: #606266;
  min-width: 35px;
}
</style>