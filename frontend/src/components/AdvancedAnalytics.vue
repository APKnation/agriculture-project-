<template>
  <div class="advanced-analytics">
    <div class="container-fluid py-4">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="analytics-header bg-gradient-primary text-white p-4 rounded-3 shadow-sm">
            <h2 class="fw-bold mb-2">
              <i class="bi bi-graph-up me-2"></i>
              Advanced Analytics
            </h2>
            <p class="mb-0 opacity-90">Comprehensive market insights and trends analysis</p>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-3">
                  <label class="form-label fw-semibold">Period</label>
                  <select v-model="filters.period" @change="fetchAnalytics" class="form-select">
                    <option value="weekly">Last 7 Days</option>
                    <option value="monthly">Last 30 Days</option>
                    <option value="yearly">Last Year</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label class="form-label fw-semibold">Region</label>
                  <select v-model="filters.region" @change="fetchAnalytics" class="form-select">
                    <option value="">All Regions</option>
                    <option value="North">North</option>
                    <option value="South">South</option>
                    <option value="East">East</option>
                    <option value="West">West</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label class="form-label fw-semibold">Crop</label>
                  <select v-model="filters.crop_id" @change="fetchAnalytics" class="form-select">
                    <option value="">All Crops</option>
                    <option v-for="crop in crops" :key="crop.id" :value="crop.id">
                      {{ crop.name }}
                    </option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label class="form-label fw-semibold">Report Type</label>
                  <select v-model="reportType" @change="fetchReport" class="form-select">
                    <option value="summary">Summary Report</option>
                    <option value="detailed">Detailed Report</option>
                    <option value="forecast">Forecast Report</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
          <span class="visually-hidden">Loading analytics...</span>
        </div>
        <p class="text-muted mt-3">Loading analytics data...</p>
      </div>

      <!-- Analytics Content -->
      <div v-else>
        <!-- Statistics Overview -->
        <div class="row g-4 mb-4">
          <div class="col-md-3">
            <div class="stat-card card border-0 shadow-sm h-100">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <p class="text-muted small text-uppercase mb-2">Average Price</p>
                    <h3 class="fw-bold mb-0">${{ analytics.statistics?.avg_price?.toFixed(2) || '0.00' }}</h3>
                  </div>
                  <div class="stat-icon bg-primary bg-opacity-10 text-primary rounded-3 p-2">
                    <i class="bi bi-currency-dollar"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="stat-card card border-0 shadow-sm h-100">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <p class="text-muted small text-uppercase mb-2">Total Records</p>
                    <h3 class="fw-bold mb-0">{{ analytics.statistics?.total_records || 0 }}</h3>
                  </div>
                  <div class="stat-icon bg-success bg-opacity-10 text-success rounded-3 p-2">
                    <i class="bi bi-database"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="stat-card card border-0 shadow-sm h-100">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <p class="text-muted small text-uppercase mb-2">Max Price</p>
                    <h3 class="fw-bold mb-0">${{ analytics.statistics?.max_price?.toFixed(2) || '0.00' }}</h3>
                  </div>
                  <div class="stat-icon bg-warning bg-opacity-10 text-warning rounded-3 p-2">
                    <i class="bi bi-arrow-up-circle"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="stat-card card border-0 shadow-sm h-100">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <p class="text-muted small text-uppercase mb-2">Price Volatility</p>
                    <h3 class="fw-bold mb-0">{{ (analytics.statistics?.price_stddev || 0).toFixed(2) }}</h3>
                  </div>
                  <div class="stat-icon bg-info bg-opacity-10 text-info rounded-3 p-2">
                    <i class="bi bi-graph-up-arrow"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Charts -->
        <div class="row g-4 mb-4">
          <!-- Time Series Chart -->
          <div class="col-lg-8">
            <div class="card border-0 shadow-sm">
              <div class="card-header bg-white border-0">
                <h5 class="card-title mb-0">
                  <i class="bi bi-graph-up me-2"></i>
                  Price Trends Over Time
                </h5>
              </div>
              <div class="card-body">
                <div class="chart-container" style="position: relative; height: 400px;">
                  <LineChart :data="timeSeriesData" :options="chartOptions" />
                </div>
              </div>
            </div>
          </div>

          <!-- Regional Comparison -->
          <div class="col-lg-4">
            <div class="card border-0 shadow-sm">
              <div class="card-header bg-white border-0">
                <h5 class="card-title mb-0">
                  <i class="bi bi-geo-alt me-2"></i>
                  Regional Comparison
                </h5>
              </div>
              <div class="card-body">
                <div class="chart-container" style="position: relative; height: 400px;">
                  <BarChart :data="regionalData" :options="barChartOptions" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Market Report -->
        <div class="row g-4">
          <div class="col-12">
            <div class="card border-0 shadow-sm">
              <div class="card-header bg-white border-0">
                <h5 class="card-title mb-0">
                  <i class="bi bi-file-earmark-text me-2"></i>
                  Market Report - {{ reportType.charAt(0).toUpperCase() + reportType.slice(1) }}
                </h5>
              </div>
              <div class="card-body">
                <div v-if="reportLoading" class="text-center py-3">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading report...</span>
                  </div>
                </div>
                <div v-else-if="marketReport" class="report-content">
                  <!-- Summary Report -->
                  <div v-if="reportType === 'summary'">
                    <div class="row g-4">
                      <div class="col-md-6">
                        <h6 class="fw-semibold text-primary">Market Overview</h6>
                        <ul class="list-unstyled">
                          <li><strong>Total Crops:</strong> {{ marketReport.overview?.total_crops }}</li>
                          <li><strong>Total Regions:</strong> {{ marketReport.overview?.total_regions }}</li>
                          <li><strong>Average Price:</strong> ${{ marketReport.overview?.avg_price?.toFixed(2) }}</li>
                          <li><strong>Total Transactions:</strong> {{ marketReport.overview?.total_transactions }}</li>
                        </ul>
                      </div>
                      <div class="col-md-6">
                        <h6 class="fw-semibold text-primary">Top Performing Crops</h6>
                        <div class="table-responsive">
                          <table class="table table-sm">
                            <thead>
                              <tr>
                                <th>Crop</th>
                                <th>Avg Price</th>
                                <th>Volume</th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr v-for="crop in marketReport.top_crops?.slice(0, 5)" :key="crop.crop__name">
                                <td>{{ crop.crop__name }}</td>
                                <td>${{ crop.avg_price?.toFixed(2) }}</td>
                                <td>{{ crop.total_volume }}</td>
                              </tr>
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Detailed Report -->
                  <div v-else-if="reportType === 'detailed'">
                    <div class="table-responsive">
                      <table class="table table-striped">
                        <thead>
                          <tr>
                            <th>Crop</th>
                            <th>Region</th>
                            <th>Avg Price</th>
                            <th>Max Price</th>
                            <th>Min Price</th>
                            <th>Transactions</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="item in marketReport.crop_performance_matrix?.slice(0, 10)" :key="`${item.crop__name}-${item.region}`">
                            <td>{{ item.crop__name }}</td>
                            <td>{{ item.region }}</td>
                            <td>${{ item.avg_price?.toFixed(2) }}</td>
                            <td>${{ item.max_price?.toFixed(2) }}</td>
                            <td>${{ item.min_price?.toFixed(2) }}</td>
                            <td>{{ item.transaction_count }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>

                  <!-- Forecast Report -->
                  <div v-else-if="reportType === 'forecast'">
                    <div class="forecast-grid">
                      <div class="row g-3">
                        <div v-for="forecast in marketReport.forecasts" :key="forecast.crop" class="col-md-4">
                          <div class="forecast-card border rounded-3 p-3">
                            <h6 class="fw-semibold">{{ forecast.crop }}</h6>
                            <div class="d-flex justify-content-between align-items-center mb-2">
                              <span class="text-muted">Current:</span>
                              <span class="fw-bold">${{ forecast.current_price?.toFixed(2) }}</span>
                            </div>
                            <div class="d-flex justify-content-between align-items-center mb-2">
                              <span class="text-muted">Forecast:</span>
                              <span class="fw-bold">${{ forecast.forecast_price?.toFixed(2) }}</span>
                            </div>
                            <div class="trend-badge">
                              <span :class="getTrendBadgeClass(forecast.trend)" class="badge">
                                {{ forecast.trend }}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useCropsStore } from '../stores/crops'
import axios from '../axios'
import LineChart from './charts/LineChart.vue'
import BarChart from './charts/BarChart.vue'

export default {
  name: 'AdvancedAnalytics',
  components: {
    LineChart,
    BarChart
  },
  setup() {
    const cropsStore = useCropsStore()
    
    // Reactive data
    const loading = ref(false)
    const reportLoading = ref(false)
    const analytics = ref({})
    const marketReport = ref(null)
    const reportType = ref('summary')
    const crops = ref([])
    
    const filters = ref({
      period: 'monthly',
      region: '',
      crop_id: ''
    })

    // Chart data
    const timeSeriesData = computed(() => {
      if (!analytics.value.time_series) return null
      
      return {
        labels: analytics.value.time_series.map(item => 
          new Date(item.period).toLocaleDateString()
        ),
        datasets: [
          {
            label: 'Average Price',
            data: analytics.value.time_series.map(item => item.avg_price),
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.1
          },
          {
            label: 'Max Price',
            data: analytics.value.time_series.map(item => item.max_price),
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            tension: 0.1
          },
          {
            label: 'Min Price',
            data: analytics.value.time_series.map(item => item.min_price),
            borderColor: 'rgb(54, 162, 235)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            tension: 0.1
          }
        ]
      }
    })

    const regionalData = computed(() => {
      if (!analytics.value.regional_comparison) return null
      
      return {
        labels: analytics.value.regional_comparison.map(item => item.region),
        datasets: [
          {
            label: 'Average Price',
            data: analytics.value.regional_comparison.map(item => item.avg_price),
            backgroundColor: [
              'rgba(255, 99, 132, 0.8)',
              'rgba(54, 162, 235, 0.8)',
              'rgba(255, 205, 86, 0.8)',
              'rgba(75, 192, 192, 0.8)'
            ],
            borderColor: [
              'rgb(255, 99, 132)',
              'rgb(54, 162, 235)',
              'rgb(255, 205, 86)',
              'rgb(75, 192, 192)'
            ],
            borderWidth: 1
          }
        ]
      }
    })

    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Price ($)'
          }
        }
      }
    }

    const barChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Average Price ($)'
          }
        }
      }
    }

    // Methods
    const fetchAnalytics = async () => {
      loading.value = true
      try {
        const params = Object.fromEntries(
          Object.entries(filters.value).filter(([_, v]) => v !== '')
        )
        const response = await axios.get('/api/analytics/advanced/', { params })
        analytics.value = response.data
      } catch (error) {
        console.error('Failed to fetch analytics:', error)
      } finally {
        loading.value = false
      }
    }

    const fetchReport = async () => {
      reportLoading.value = true
      try {
        const params = {
          type: reportType.value,
          region: filters.value.region || undefined
        }
        const response = await axios.get('/api/analytics/market-reports/', { params })
        marketReport.value = response.data
      } catch (error) {
        console.error('Failed to fetch report:', error)
      } finally {
        reportLoading.value = false
      }
    }

    const getTrendBadgeClass = (trend) => {
      switch (trend) {
        case 'upward':
          return 'bg-success'
        case 'downward':
          return 'bg-danger'
        default:
          return 'bg-secondary'
      }
    }

    // Lifecycle
    onMounted(async () => {
      await cropsStore.fetchAllCrops()
      crops.value = cropsStore.allCrops
      await fetchAnalytics()
      await fetchReport()
    })

    return {
      loading,
      reportLoading,
      analytics,
      marketReport,
      reportType,
      crops,
      filters,
      timeSeriesData,
      regionalData,
      chartOptions,
      barChartOptions,
      fetchAnalytics,
      fetchReport,
      getTrendBadgeClass
    }
  }
}
</script>

<style scoped>
.advanced-analytics {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.analytics-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-card {
  transition: transform 0.2s ease-in-out;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.chart-container {
  background: white;
  border-radius: 0.5rem;
}

.forecast-card {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  transition: transform 0.2s ease-in-out;
}

.forecast-card:hover {
  transform: translateY(-2px);
}

.trend-badge {
  text-align: center;
  margin-top: 0.5rem;
}

.card {
  border-radius: 0.75rem;
}

.card-header {
  border-radius: 0.75rem 0.75rem 0 0 !important;
}
</style>
