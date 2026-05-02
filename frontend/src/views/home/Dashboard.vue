<script setup>
import { Pie, Bar } from 'vue-chartjs';
import { Chart as ChartJS, ArcElement, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend, } from 'chart.js';
import { DataAnalysis, PieChart, Check, Refresh, FolderOpened, } from '@element-plus/icons-vue';

document.title = 'Dashboard - Senati Helpdesk'

ChartJS.register(
  ArcElement,
  BarElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend
);

const chartData = {
  labels: ['Cerrado', 'Abierto', 'Re-abierto'],
  datasets: [
    {
      backgroundColor: ['#67C23A', '#409EFF', '#E6A23C'],
      data: [45, 30, 15],
    },
  ],
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: '#606266',
        font: {
          size: 17,
        },
      },
    },
  },
};
</script>

<template>
  <!-- Tarjetas de resumen -->
  <el-card>
    <el-row :gutter="20" class="mb-4">
      <el-col :xs="24" :sm="12" :md="8">
        <el-card shadow="hover" class="stat-card" body-style="padding: 20px;">
          <div class="card-header">
            <el-icon size="24" color="#67C23A">
              <Check />
            </el-icon>
            <span class="card-title" style="color: #67C23A;">Tickets Cerrados</span>
          </div>
          <el-statistic :value="45" value-style="color: #67C23A; font-size: 24px;" />
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8">
        <el-card shadow="hover" class="stat-card" body-style="padding: 20px;">
          <div class="card-header">
            <el-icon size="24" color="#409EFF">
              <FolderOpened />
            </el-icon>
            <span class="card-title" style="color: #409EFF;">Tickets Abiertos</span>
          </div>
          <el-statistic :value="30" value-style="color: #409EFF; font-size: 24px;" />
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8">
        <el-card shadow="hover" class="stat-card" body-style="padding: 20px;">
          <div class="card-header">
            <el-icon size="24" color="#E6A23C">
              <Refresh />
            </el-icon>
            <span class="card-title" style="color: #E6A23C;">Tickets Re-abiertos</span>
          </div>
          <el-statistic :value="15" value-style="color: #E6A23C; font-size: 24px;" />
        </el-card>
      </el-col>
    </el-row>

    <!-- Gráficos -->
    <el-row :gutter="20">
      <el-col :xs="24" :md="12">
        <el-card shadow="always" body-style="padding: 20px;">
          <template #header>
            <div class="card-header">
              <el-icon>
                <DataAnalysis />
              </el-icon>
              <span class="card-title" style="color: #409EFF;">Tickets por Estado (Barras)</span>
            </div>
          </template>
          <div style="height: 320px;">
            <Bar :data="chartData" :options="chartOptions" />
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :md="12">
        <el-card shadow="always" body-style="padding: 20px;">
          <template #header>
            <div class="card-header">
              <el-icon>
                <PieChart />
              </el-icon>
              <span class="card-title" style="color: #E6A23C;">Tickets por Estado (Circular)</span>
            </div>
          </template>
          <div style="height: 320px;">
            <Pie :data="chartData" :options="chartOptions" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </el-card>
</template>

<style scoped>
.mb-4 {
  margin-bottom: 1.5rem;
}

.stat-card {
  border-radius: 8px;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  color: #615f5f;
  margin-bottom: 10px;
}

.card-title {
  font-size: 16px;
}
</style>
