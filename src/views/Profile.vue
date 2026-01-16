<template>
  <div class="page-container" v-loading="loading">
    <div class="nav-header">
      <el-button @click="$router.back()" :icon="ArrowLeft" plain size="small">返回排行榜</el-button>
    </div>

    <div v-if="player" class="profile-content">
      
      <el-card class="header-card" shadow="always">
        <div class="header-inner">
          <el-avatar :size="100" :src="player.avatar_url" class="big-avatar">
            {{ player.name.charAt(0) }}
          </el-avatar>
          
          <div class="header-info">
            <div class="name-row">
              <h1 class="name">{{ player.name }}</h1>
              <el-tag v-if="player.grade > 0" type="warning" effect="dark" round>
                Lv.{{ player.grade }} 级
              </el-tag>
            </div>
            
            <p v-if="player.nick_name" class="nickname">@{{ player.nick_name }}</p>
            
            <div class="meta-row">
              <span class="meta-item">📍 {{ player.region || '未知地区' }}</span>
              <span class="meta-item">🔥 活跃度 {{ player.activity || 0 }}%</span>
            </div>

            <div class="teams-row" v-if="teams.length > 0">
              <span class="label">所属团体：</span>
              <el-tag 
                v-for="team in teams" 
                :key="team.id" 
                size="small" 
                effect="plain"
                class="team-tag"
              >
                {{ team.name }}
              </el-tag>
            </div>
          </div>

          <div class="elo-box">
            <div class="elo-label">Current Elo</div>
            <div class="elo-number">{{ player.current_elo }}</div>
            <div class="elo-max">历史最高: {{ player.max_elo || player.current_elo }}</div>
          </div>
        </div>
      </el-card>

      <div class="main-layout">
        <div class="left-col">
          <el-card class="box-card chart-card">
            <template #header>
              <div class="card-header">
                <span>📈 战力走势</span>
              </div>
            </template>
            <div class="chart-container">
              <v-chart class="chart" :option="chartOption" autoresize />
            </div>
          </el-card>
        </div>

        <div class="right-col">
          <el-card class="box-card achievements-card">
            <template #header>
              <div class="card-header">
                <span>🏆 赛事荣誉</span>
              </div>
            </template>
            
            <div v-if="hasAchievements" class="achievements-list">
              <div v-if="achievements.champion?.length" class="achieve-group">
                <div class="achieve-title gold">🥇 冠军</div>
                <div v-for="(item, i) in achievements.champion" :key="i" class="achieve-item">
                  {{ item }}
                </div>
              </div>

              <div v-if="achievements.runner_up?.length" class="achieve-group">
                <div class="achieve-title silver">🥈 亚军</div>
                <div v-for="(item, i) in achievements.runner_up" :key="i" class="achieve-item">
                  {{ item }}
                </div>
              </div>

              <div v-if="achievements.top4?.length" class="achieve-group">
                <div class="achieve-title bronze">🥉 四强</div>
                <div v-for="(item, i) in achievements.top4" :key="i" class="achieve-item">
                  {{ item }}
                </div>
              </div>

              <div v-if="achievements.top8?.length" class="achieve-group">
                <div class="achieve-title normal">🎖 八强</div>
                <div v-for="(item, i) in achievements.top8" :key="i" class="achieve-item">
                  {{ item }}
                </div>
              </div>
            </div>
            
            <el-empty v-else description="暂无主要赛事记录" :image-size="80"></el-empty>
          </el-card>
          
          <el-card class="box-card bio-card" style="margin-top: 20px;">
             <template #header><span>📝 简介</span></template>
             <p style="color: #666; font-size: 14px; line-height: 1.6;">
               {{ player.bio || '这位选手专注于修炼，尚未填写简介。' }}
             </p>
          </el-card>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { supabase } from '../supabase'
import { ArrowLeft } from '@element-plus/icons-vue'

// ECharts 相关
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, DataZoomComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, DataZoomComponent])

const route = useRoute()
const loading = ref(true)
const player = ref(null)
const teams = ref([]) // 存储团体列表
const achievements = ref({}) // 存储荣誉对象
const chartOption = ref({})

// 判断是否有荣誉数据
const hasAchievements = computed(() => {
  if (!achievements.value) return false
  const { champion, runner_up, top4, top8 } = achievements.value
  return (champion?.length || 0) + (runner_up?.length || 0) + (top4?.length || 0) + (top8?.length || 0) > 0
})

const fetchPlayerDetail = async () => {
  const playerId = route.params.id
  loading.value = true

  try {
    // 1. 获取选手详情 (包含 JSONB achievements)
    const { data: pData, error: pError } = await supabase
      .from('players')
      .select('*')
      .eq('id', playerId)
      .single()
    
    if (pError) throw pError
    player.value = pData
    achievements.value = pData.achievements || {}

    // 2. 获取选手所属团体
    // 这是一个跨表查询：从 player_teams 表查，同时关联 teams 表取名字
    const { data: tData, error: tError } = await supabase
      .from('player_teams')
      .select(`
        teams (
          id,
          name
        )
      `)
      .eq('player_id', playerId)

    if (!tError && tData) {
      // 整理数据结构: [{teams: {name: 'A'}}] -> [{name: 'A'}]
      teams.value = tData.map(item => item.teams).filter(Boolean)
    }

    // 3. 获取 Elo 历史 (用于画图)
    const { data: hData, error: hError } = await supabase
      .from('elo_history')
      .select('new_elo, date')
      .eq('player_id', playerId)
      .order('date', { ascending: true })
    
    if (!hError) {
      const dates = hData.map(d => d.date)
      const scores = hData.map(d => d.new_elo)
      setupChart(dates, scores)
    }

  } catch (err) {
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}

const setupChart = (dates, scores) => {
  chartOption.value = {
    tooltip: { trigger: 'axis' },
    grid: { top: '10%', left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: dates, boundaryGap: false },
    yAxis: { type: 'value', scale: true },
    dataZoom: [{ type: 'inside' }],
    series: [{
      data: scores,
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      itemStyle: { color: '#409EFF' },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(64,158,255,0.4)' },
            { offset: 1, color: 'rgba(64,158,255,0)' }
          ]
        }
      }
    }]
  }
}

onMounted(() => {
  fetchPlayerDetail()
})
</script>

<style scoped>
.page-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px;
}
.nav-header {
  margin-bottom: 15px;
}

/* 顶部卡片 */
.header-card {
  background: linear-gradient(135deg, #ffffff 0%, #f3f5f7 100%);
  border: none;
  transition: background 0.3s;
}
.header-inner {
  display: flex;
  align-items: center;
  gap: 25px;
}
.header-info {
  flex: 1;
}
.name-row {
  display: flex;
  align-items: center;
  gap: 10px;
}
.name { margin: 0; font-size: 28px; color: #303133; transition: color 0.3s; }
.nickname { color: #909399; margin: 5px 0 10px; font-size: 14px; transition: color 0.3s; }
.meta-row { display: flex; gap: 15px; margin-bottom: 10px; color: #606266; font-size: 14px; transition: color 0.3s; }
.teams-row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.label { font-size: 13px; color: #909399; }
.team-tag { border-radius: 4px; }

/* 右侧 Elo 大数字 */
.elo-box {
  text-align: center;
  padding-left: 30px;
  border-left: 1px solid #e4e7ed;
  transition: border-color 0.3s;
}
.elo-label { font-size: 12px; color: #909399; text-transform: uppercase; letter-spacing: 1px; }
.elo-number { font-size: 42px; font-weight: 800; color: #409EFF; line-height: 1.2; }
.elo-max { font-size: 12px; color: #C0C4CC; transition: color 0.3s; }

/* 布局：左右栏 */
.main-layout {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}
.left-col { flex: 2; }
.right-col { flex: 1; min-width: 300px; }

.chart-container { height: 350px; width: 100%; }

/* 荣誉列表 */
.achieve-group { margin-bottom: 15px; }
.achieve-title { font-weight: bold; font-size: 14px; margin-bottom: 5px; padding-bottom: 5px; border-bottom: 1px dashed #eee; transition: border-color 0.3s; }
.achieve-title.gold { color: #D4AF37; }
.achieve-title.silver { color: #A8A9AD; }
.achieve-title.bronze { color: #CD7F32; }
.achieve-title.normal { color: #606266; }

.achieve-item { font-size: 13px; color: #606266; line-height: 1.6; padding-left: 5px; transition: color 0.3s; }

/* 移动端适配 */
@media (max-width: 768px) {
  .header-inner { flex-direction: column; text-align: center; }
  .elo-box { border-left: none; padding-left: 0; margin-top: 20px; }
  .main-layout { flex-direction: column; }
}

/* === 🌙 夜间模式适配 (Dark Mode) === */

/* 顶部卡片背景 */
html.dark .header-card {
  background: linear-gradient(135deg, #1d1e1f 0%, #2b2b2b 100%);
  border: 1px solid #363637; /* 深色边框 */
}

/* 文本颜色适配 */
html.dark .name { color: #E5EAF3; }
html.dark .nickname { color: #A3A6AD; }
html.dark .meta-row { color: #A3A6AD; }
html.dark .label { color: #A3A6AD; }

/* 分隔线与装饰线 */
html.dark .elo-box {
  border-left-color: #4C4D4F;
}
html.dark .elo-max { color: #6C6E72; }

/* 下方卡片背景与文本 */
html.dark .box-card {
  /* Element Plus 卡片通常会自动适配，但如果没有，强制深色背景 */
  background-color: #1d1e1f;
  border-color: #4C4D4F;
  color: #E5EAF3;
}

html.dark .card-header span {
  color: #E5EAF3;
}

/* 荣誉列表适配 */
html.dark .achieve-title {
  border-bottom-color: #4C4D4F;
}
html.dark .achieve-title.normal { color: #A3A6AD; }
html.dark .achieve-item { color: #bbb; }
html.dark .achieve-title.gold { color: #FFD700; /* 可以在深色下稍微提亮 */ }
html.dark .achieve-title.silver { color: #C0C4CC; }

/* 简介文字颜色 */
html.dark .bio-card p {
  color: #bbb !important; /* 修正内联样式的颜色 */
}
</style>