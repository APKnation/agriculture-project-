<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Supply & Demand Insights</h2>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-blue-500" role="status"></div>
      <p class="mt-2 text-gray-500">Loading demand insights...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-red-500 py-5 text-center">
      {{ error }}
    </div>

    <!-- Table -->
    <div class="table-responsive">
      <table class="table table-hover mb-0">
        <thead class="table-light">
          <tr>
            <th class="border-0">
              <div class="d-flex align-items-center">
                <i class="bi bi-flower1 me-2"></i>
                <span>Crop</span>
              </div>
            </th>
            <th class="border-0">
              <div class="d-flex align-items-center">
                <i class="bi bi-shop me-2"></i>
                <span>Market</span>
              </div>
            </th>
            <th class="border-0">
              <div class="d-flex align-items-center">
                <i class="bi bi-speedometer2 me-2"></i>
                <span>Demand Level</span>
              </div>
            </th>
            <th class="border-0">
              <div class="d-flex align-items-center">
                <i class="bi bi-clipboard-data me-2"></i>
                <span>Records</span>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(d, index) in demand" :key="d.id" 
              :class="getRowClass(d.demand_level)">
            <td>
              <div class="d-flex align-items-center">
                <div class="crop-icon bg-light rounded-2 p-2 me-2">
                  <i :class="getCropIcon(d.crop__name)" class="text-success"></i>
                </div>
                <div>
                  <div class="fw-semibold">{{ d.crop__name }}</div>
                  <small class="text-muted d-block">{{ getMarketName(d.market) }}</small>
                </div>
              </div>
            </td>
            <td>
              <span class="badge bg-info fs-6">{{ getMarketName(d.market) }}</span>
            </td>
            <td>
              <div class="d-flex align-items-center">
                <span :class="`badge fs-6 bg-${getDemandLevelColor(d.demand_level)}`">
                  <i class="bi bi-graph-up me-1"></i>
                  {{ getDemandLevelText(d.demand_level) }}
                </span>
                <div class="ms-2">
                  <small class="text-muted">Score: {{ calculateDemandScore(d) }}</small>
                </div>
              </div>
            </td>
            <td>
              <div class="d-flex align-items-center">
                <i class="bi bi-clipboard-data me-2 text-muted"></i>
                <span class="fw-semibold">{{ d.records }}</span>
                <div class="ms-2">
                  <small class="text-muted">{{ getRecordCountText(d.records) }}</small>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const demand = ref([])
const loading = ref(true)
const error = ref(null)

// Computed properties for demand statistics
const getHighDemandCount = computed(() => {
  return demand.value.filter(d => d.demand_level === 'High').length
})

const getModerateDemandCount = computed(() => {
  return demand.value.filter(d => d.demand_level === 'Moderate').length
})

const getLowDemandCount = computed(() => {
  return demand.value.filter(d => d.demand_level === 'Low').length
})

onMounted(async () => {
  try {
    const res = await axios.get('/demand/')
    demand.value = res.data
  } catch (err) {
    console.error(err)
  }
})

const refreshData = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await axios.get('/demand/')
    demand.value = res.data
  } catch (err) {
    console.error(err)
    error.value = 'Failed to refresh demand insights.'
  } finally {
    loading.value = false
  }
}

// Helper functions
const getRowClass = (demandLevel) => {
  switch (demandLevel?.toLowerCase()) {
    case 'high':
      return 'table-danger'
    case 'moderate':
      return 'table-warning'
    case 'low':
      return 'table-success'
    default:
      return ''
  }
}

const getDemandLevelColor = (demandLevel) => {
  switch (demandLevel?.toLowerCase()) {
    case 'high':
      return 'danger'
    case 'moderate':
      return 'warning'
    case 'low':
      return 'success'
    default:
      return 'secondary'
  }
}

const getDemandLevelText = (demandLevel) => {
  return demandLevel || 'Unknown'
}

const getMarketName = (market) => {
  const marketNames = {
    'N': 'North',
    'S': 'South', 
    'E': 'East',
    'W': 'West',
    'C': 'Central'
  }
  return marketNames[market] || market || 'Unknown'
}

const getCropIcon = (cropName) => {
  const cropIcons = {
    'Wheat': 'bi-flower1',
    'Corn': 'bi-flower2',
    'Tomatoes': 'bi-flower3',
    'Potatoes': 'bi-flower1',
    'Rice': 'bi-flower2',
    'Onions': 'bi-flower3',
    'Maize': 'bi-flower1',
    'Cotton': 'bi-flower2',
    'Sorghum': 'bi-flower3',
    'Millet': 'bi-flower1',
    'Barley': 'bi-flower2',
    'Soybeans': 'bi-flower3',
    'Groundnuts': 'bi-flower1',
    'Cassava': 'bi-flower2',
    'Yams': 'bi-flower3',
    'Taro': 'bi-flower1',
    'Plantains': 'bi-flower2',
    'Sweet potatoes': 'bi-flower3',
    'Cocoyams': 'bi-flower1',
    'Bananas': 'bi-flower2',
    'Coffee': 'bi-flower3',
    'Tea': 'bi-flower1',
    'Sugarcane': 'bi-flower2',
    'Sugar beets': 'bi-flower3'
  }
  return cropIcons[cropName] || 'bi-flower1'
}

const calculateDemandScore = (demandData) => {
  let score = 0
  
  // Base score from demand indicators
  if (demandData.demand_indicators > 0) score += demandData.demand_indicators * 20
  if (demandData.market_activity > 0) score += demandData.market_activity * 2
  
  // Add records score (capped at 50)
  const recordsScore = Math.min(demandData.records || 0, 50) * 0.5
  
  return Math.min(score + recordsScore, 100)
}

const getRecordCountText = (count) => {
  if (count >= 50) return 'High Activity'
  if (count >= 20) return 'Moderate Activity'
  if (count >= 10) return 'Low Activity'
  if (count >= 5) return 'Minimal Activity'
  return 'No Activity'
}
</script>

<style scoped>
.demand-insights-wrapper {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  min-height: 100vh;
}

.demand-header {
  background: linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%);
  border: none;
  box-shadow: 0 8px 25px rgba(13, 110, 253, 0.3);
}

.demand-summary-card {
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.demand-summary-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
  border-color: #dee2e6;
}

.summary-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin: 0 auto;
}

.crop-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

.card {
  border-radius: 1rem;
  transition: all 0.3s ease;
  overflow: hidden;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.table {
  margin-bottom: 0;
}

.table th {
  border-top: none;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.5px;
  background-color: #f8f9fa;
}

.table td {
  vertical-align: middle;
  border-top: 1px solid #dee2e6;
}

.table-danger {
  --bs-table-bg: rgba(220, 53, 69, 0.1);
}

.table-warning {
  --bs-table-bg: rgba(255, 193, 7, 0.1);
}

.table-success {
  --bs-table-bg: rgba(25, 135, 84, 0.1);
}

.btn {
  border-radius: 0.5rem;
  transition: all 0.3s ease;
  font-weight: 600;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.btn-outline-light {
  border-color: rgba(255, 255, 255, 0.3);
  color: rgba(255, 255, 255, 0.9);
}

.btn-outline-light:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
  color: #fff;
}

.alert {
  border-radius: 0.75rem;
  border: none;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile Responsive Enhancements */
@media (max-width: 768px) {
  .demand-insights-wrapper {
    padding: 1rem 0;
  }
  
  .demand-header {
    padding: 2rem 1.5rem !important;
  }
  
  .display-5 {
    font-size: 2rem !important;
  }
  
  .summary-icon {
    width: 50px;
    height: 50px;
    font-size: 1.25rem;
  }
  
  .demand-summary-card .card-body {
    padding: 1.5rem !important;
  }
}

@media (max-width: 576px) {
  .demand-header {
    padding: 1.5rem 1rem !important;
  }
  
  .display-5 {
    font-size: 1.75rem !important;
  }
  
  .summary-icon {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
  
  .demand-summary-card .card-body {
    padding: 1rem !important;
  }
  
  .table-responsive {
    font-size: 0.875rem;
  }
}
</style>
