<template>
  <div class="page-container">
    <h1>🏆 综合排行榜</h1>
    
    <el-collapse style="margin-bottom: 20px;">
      <el-collapse-item title="🛠️ 筛选与工具 (点击展开)" name="1">
        <el-button type="primary">按分数排序</el-button>
        <el-button type="success">导出 Excel</el-button>
      </el-collapse-item>
    </el-collapse>

    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="rank" label="排名" width="80" />
      <el-table-column prop="name" label="ID / 名称" />
      <el-table-column prop="score" label="分数" sortable />
    </el-table>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 模拟数据，以后这里换成从数据库读取
const tableData = ref([
  { rank: 1, name: '机械臂-Alpha', score: 9800 },
  { rank: 2, name: '测试员-UserA', score: 8500 },
  { rank: 3, name: '算法-V2.0', score: 7200 },
])
</script>