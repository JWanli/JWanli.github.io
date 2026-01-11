<template>
  <div class="page-container">
    <h1>🏆 综合排行榜</h1>
    
    <div v-if="loading" style="text-align: center; padding: 40px;">
      <el-icon class="is-loading" size="30"><Loading /></el-icon>
      <p>正在从云端获取最新战绩...</p>
    </div>

    <div v-else>
      <el-table :data="tableData" border stripe style="width: 100%">
        <el-table-column label="排名" width="80" align="center">
          <template #default="scope">
            <span v-if="scope.$index === 0">🥇</span>
            <span v-else-if="scope.$index === 1">🥈</span>
            <span v-else-if="scope.$index === 2">🥉</span>
            <span v-else>{{ scope.$index + 1 }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="name" label="选手" width="180">
          <template #default="scope">
            <div style="display: flex; align-items: center; cursor: pointer;" @click="goToProfile(scope.row.id)">
              <el-avatar :size="30" :src="scope.row.avatar_url" style="margin-right: 10px;">
                {{ scope.row.name.charAt(0) }}
              </el-avatar>
              
              <div>
                <div style="font-weight: bold; color: #409EFF;">{{ scope.row.name }}</div>
                <div v-if="scope.row.nick_name" style="font-size: 12px; color: #888;">
                  {{ scope.row.nick_name }}
                </div>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="region" label="地区/流派" width="150" />
        
        <el-table-column prop="current_elo" label="大枪等级分" sortable>
             <template #default="scope">
                <span style="color: #409EFF; font-weight: bold;">{{ scope.row.current_elo }}</span>
             </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import { supabase } from '../supabase' // 引入刚才建的配置文件
import { useRouter } from 'vue-router'

const tableData = ref([])
const loading = ref(true)
const router = useRouter()

const goToProfile = (id) => {
  router.push(`/profile/${id}`)
}

// 获取数据的函数
const fetchData = async () => {
  loading.value = true
  
  // 核心查询语句：查 players 表，按 current_elo 倒序排列
  const { data, error } = await supabase
    .from('players')
    .select('id, name, nick_name, region, current_elo')
    .order('current_elo', { ascending: false })
    // .limit(100) // 如果人多了，可以限制只查前 100 名
  
  if (error) {
    console.error('获取排名失败:', error)
    alert('数据加载失败，请检查控制台')
  } else {
    tableData.value = data
  }
  
  loading.value = false
}

// 页面一加载就自动运行
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.page-container {
  max-width: 900px;
  margin: 0 auto;
}
</style>