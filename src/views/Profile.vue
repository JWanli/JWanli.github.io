<template>
  <div class="page-container" v-loading="loading">
    <div style="margin-bottom: 20px;">
      <el-button @click="$router.back()" :icon="ArrowLeft" circle />
      <span style="margin-left: 10px; color: #666;">返回排行榜</span>
    </div>

    <div v-if="player" class="profile-content">
      <el-card class="box-card header-card">
        <div class="header-content">
          <el-avatar :size="80" :src="player.avatar_url || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'" />
          <div class="info-text">
            <h1 class="name">
              {{ player.name }}
              <el-tag v-if="player.nick_name" size="small" type="info">{{ player.nick_name }}</el-tag>
            </h1>
            <p class="region">📍 {{ player.region || '未知地区' }}</p>
            <div class="stats">
              <span class="elo-highlight">⚡ {{ player.current_elo }}</span> 
              <span class="elo-label">当前 Elo 分</span>
            </div>
          </div>
        </div>
      </el-card>

      <el-card class="box-card" style="margin-top: 20px;">
        <template #header>
          <div class="card-header">
            <span>📜 选手简介</span>
          </div>
        </template>
        <p v-if="player.bio">{{ player.bio }}</p>
        <p v-else style="color: #999; font-style: italic;">这位选手很神秘，还没有留下简介...</p>
      </el-card>

      <el-card class="box-card" style="margin-top: 20px;">
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
    
    <div v-else-if="!loading" style="text-align: center; margin-top: 50px;">
      <el-empty description="未找到该选手信息" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { supabase } from '../supabase'
import { ArrowLeft } from '@element-plus/icons-vue'

// 引入 ECharts
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, TitleComponent, DataZoomComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, TitleComponent, DataZoomComponent])

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const player = ref(null)
const chartOption = ref({})

// 获取数据
const fetchPlayerDetail = async () => {
  const playerId = route.params.id
  loading.value = true

  try {
    // 1. 获取选手基本信息
    const { data: pData, error: pError } = await supabase
      .from('players')
      .select('*')
      .eq('id', playerId)
      .single()
    
    if (pError) throw pError
    player.value = pData

    // 2. 获取 Elo 历史记录
    const { data: hData, error: hError } = await supabase
      .from('elo_history')
      .select('new_elo, date, match_id')
      .eq('player_id', playerId)
      .order('date', { ascending: true }) // 按时间正序
    
    if (hError) throw hError

    // 3. 准备图表数据
    // 如果没有历史记录，只显示当前分
    const dates = hData.map(d => new Date(d.date).toLocaleDateString())
    const scores = hData.map(d => d.new_elo)

    setupChart(dates, scores)

  } catch (err) {
    console.error('Error fetching profile:', err)
  } finally {
    loading.value = false
  }
}

// 配置图表
const setupChart = (dates, scores) => {
  chartOption.value = {
    tooltip: {
      trigger: 'axis',
      formatter: '{b} <br/> Elo: {c}'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates
    },
    yAxis: {
      type: 'value',
      scale: true // 让Y轴不从0开始，根据分数自动调整范围
    },
    series: [
      {
        name: 'Elo',
        type: 'line',
        data: scores,
        smooth: true, // 平滑曲线
        lineStyle: { color: '#409EFF', width: 3 },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(64,158,255,0.5)' },
              { offset: 1, color: 'rgba(64,158,255,0)' }
            ]
          }
        }
      }
    ],
    // 增加缩放条，方便查看长历史
    dataZoom: [{ type: 'inside' }, { type: 'slider' }]
  }
}

onMounted(() => {
  fetchPlayerDetail()
})
</script>

<style scoped>
.page-container {
  max-width: 800px;
  margin: 0 auto;
}
.header-card {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border: none;
}
/* 适配深色模式 */
.dark .header-card {
  background: linear-gradient(135deg, #2c3e50 0%, #000000 100%);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}
.name {
  margin: 0;
  font-size: 24px;
}
.region {
  color: #666;
  margin: 5px 0 10px 0;
}
.elo-highlight {
  font-size: 28px;
  font-weight: bold;
  color: #409EFF;
}
.elo-label {
  font-size: 12px;
  color: #888;
  margin-left: 5px;
}
.chart-container {
  height: 300px;
  width: 100%;
}
.chart {
  height: 100%;
  width: 100%;
}
</style>