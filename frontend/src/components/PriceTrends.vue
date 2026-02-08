<template>
  <div class="price-trends-container">
    <!-- Header Section -->
    <div class="page-header text-white p-4 mb-4 rounded-3 shadow-lg" style="background: var(--gradient-primary);">
      <div class="container-fluid">
        <div class="row align-items-center">
          <div class="col-md-6">
            <h1 class="mb-0 fw-bold">
              Price Trends
            </h1>
          </div>
          <div class="col-md-6 text-md-end">
            <div class="header-stats d-flex gap-3 justify-content-md-end">
              <div class="text-center">
                <div class="badge bg-white text-primary px-3 py-2 fs-6">
                  {{ crops.length }}
                </div>
                <small class="text-white-50">Crops</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="container-fluid py-4">
      <div class="row">
        <!-- Filters Section -->
        <div class="col-lg-3 mb-4">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-header bg-white border-bottom">
              <h5 class="mb-0 text-dark">
                Filters & Options
              </h5>
            </div>
            <div class="card-body">
              <!-- Crop Selector -->
              <div class="mb-4">
                <label for="cropSelect" class="form-label fw-semibold">Select Crop</label>
                <select
                  id="cropSelect"
                  v-model="selectedCrop"
                  @change="fetchTrends"
                  class="form-select"
                >
                  <option value="">All Crops</option>
                  <option v-for="crop in crops" :key="crop.id" :value="crop.id">
                    {{ crop.name }}
                  </option>
                </select>
              </div>

              <!-- Time Period -->
              <div class="mb-4">
                <label for="periodSelect" class="form-label fw-semibold">Time Period</label>
                <select
                  id="periodSelect"
                  v-model="selectedPeriod"
                  @change="fetchTrends"
                  class="form-select"
                >
                  <option value="7">Last 7 Days</option>
                  <option value="30">Last 30 Days</option>
                  <option value="90">Last 90 Days</option>
                  <option value="365">Last Year</option>
                </select>
              </div>

              <!-- Region Filter -->
              <div class="mb-4">
                <label for="regionSelect" class="form-label fw-semibold">Region</label>
                <select
                  id="regionSelect"
                  v-model="selectedRegion"
                  @change="fetchTrends"
                  class="form-select"
                >
                  <option value="">All Regions</option>
                  <option v-for="region in regions" :key="region" :value="region">
                    {{ region }}
                  </option>
                </select>
              </div>

              <!-- Action Buttons -->
              <div class="d-grid gap-2">
                <button @click="fetchTrends" class="btn btn-primary">
                  Update Chart
                </button>
                <button @click="exportData" class="btn btn-outline-secondary">
                  Export Data
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Chart Section -->
        <div class="col-lg-9 mb-4">
          <div class="card border-0 shadow-lg h-100">
            <div class="card-header bg-white border-bottom">
              <h5 class="mb-0 text-dark">
                Price Analysis Chart
              </h5>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2 mb-0 text-muted">Loading price trends...</p>
              </div>

              <div v-else-if="!trendData.length" class="text-center py-5">
                <div class="empty-state">
                  <h5 class="text-muted mb-3">No Data Available</h5>
                  <p class="text-muted">Select a crop and time period to view price trends.</p>
                </div>
              </div>

              <div v-else class="chart-container" style="height: 400px;">
                <canvas ref="trendChart"></canvas>
              </div>
            </div>
          </div>
        </div>

        <!-- Statistics Section -->
        <div class="col-12 mb-4">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-bottom">
              <h5 class="mb-0 text-dark">
                Price Statistics
              </h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-md-3 mb-3">
                  <div class="stat-card text-center p-3 rounded" style="background: var(--success-color);">
                    <h6 class="text-white mb-2">Current Price</h6>
                    <h4 class="text-white mb-0">{{ formatCurrency(currentPrice) }}</h4>
                  </div>
                </div>
                <div class="col-md-3 mb-3">
                  <div class="stat-card text-center p-3 rounded" style="background: var(--info-color);">
                    <h6 class="text-white mb-2">Average Price</h6>
                    <h4 class="text-white mb-0">{{ formatCurrency(averagePrice) }}</h4>
                  </div>
                </div>
                <div class="col-md-3 mb-3">
                  <div class="stat-card text-center p-3 rounded" style="background: var(--warning-color);">
                    <h6 class="text-white mb-2">Highest Price</h6>
                    <h4 class="text-white mb-0">{{ formatCurrency(highestPrice) }}</h4>
                  </div>
                </div>
                <div class="col-md-3 mb-3">
                  <div class="stat-card text-center p-3 rounded" style="background: var(--danger-color);">
                    <h6 class="text-white mb-2">Lowest Price</h6>
                    <h4 class="text-white mb-0">{{ formatCurrency(lowestPrice) }}</h4>
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
import axios from '../axios';
import Chart from 'chart.js/auto';

export default {
  name: 'PriceTrends',
  data() {
    return {
      crops: [],
      regions: ['Iringa', 'Dar es Salaam', 'Mwanza', 'Arusha', 'Dodoma', 'Tanga', 'Mbeya', 'Morogoro'],
      selectedCrop: '',
      selectedPeriod: '30',
      selectedRegion: '',
      trendData: [],
      loading: false,
      chart: null
    };
  },
  computed: {
    currentPrice() {
      return this.trendData.length > 0 ? this.trendData[this.trendData.length - 1].price : 0;
    },
    averagePrice() {
      if (this.trendData.length === 0) return 0;
      const sum = this.trendData.reduce((acc, item) => acc + item.price, 0);
      return sum / this.trendData.length;
    },
    highestPrice() {
      if (this.trendData.length === 0) return 0;
      return Math.max(...this.trendData.map(item => item.price));
    },
    lowestPrice() {
      if (this.trendData.length === 0) return 0;
      return Math.min(...this.trendData.map(item => item.price));
    }
  },
  async mounted() {
    await this.loadCrops();
  },
  methods: {
    async loadCrops() {
      try {
        const res = await axios.get('/crops/');
        this.crops = Array.isArray(res.data) ? res.data : [];
        console.log('🌾 Crops loaded:', this.crops.length);
        
        if (this.crops.length > 0) {
          this.selectedCrop = this.crops[0].id;
          await this.fetchTrends();
        }
      } catch (error) {
        console.error('Error loading crops:', error);
        this.showErrorMessage('Failed to load crops. Please try again.');
      }
    },

    async fetchTrends() {
      if (!this.selectedCrop) {
        this.showErrorMessage('Please select a crop first.');
        return;
      }

      this.loading = true;
      try {
        const params = {
          period: this.selectedPeriod,
          region: this.selectedRegion
        };

        const res = await axios.get(`/price-trends/${this.selectedCrop}/`, { params });
        this.trendData = Array.isArray(res.data) ? res.data : [];
        this.updateChart();
      } catch (error) {
        console.error('Error fetching trends:', error);
        this.showErrorMessage('Failed to load price trends. Please try again.');
      } finally {
        this.loading = false;
      }
    },

    updateChart() {
      if (this.chart) {
        this.chart.destroy();
      }

      const ctx = this.$refs.trendChart?.getContext('2d');
      if (!ctx || this.trendData.length === 0) return;

      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.trendData.map(item => this.formatDate(item.date)),
          datasets: [{
            label: 'Price Trend',
            data: this.trendData.map(item => item.price),
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderWidth: 2,
            tension: 0.4,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'top'
            },
            tooltip: {
              mode: 'index',
              intersect: false,
              callbacks: {
                label: function(context) {
                  return `Price: ${context.parsed.y.toLocaleString()} TZS`;
                }
              }
            },
            scales: {
              x: {
                grid: {
                  display: true,
                  color: 'rgba(0, 0, 0, 0.05)'
                },
                ticks: {
                  font: {
                    size: 12
                  }
                }
              },
              y: {
                grid: {
                  display: true,
                  color: 'rgba(0, 0, 0, 0.05)'
                },
                ticks: {
                  font: {
                    size: 12
                  },
                  callback: function(value) {
                    return value.toLocaleString() + ' TZS';
                  }
                },
                beginAtZero: true
              }
            }
          }
        }
      });
    },

    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric',
        year: 'numeric'
      });
    },

    formatCurrency(value) {
      return `TZS ${value.toLocaleString()}`;
    },

    showErrorMessage(message) {
      alert(message);
    },

    exportData() {
      if (this.trendData.length === 0) {
        this.showErrorMessage('No data to export.');
        return;
      }

      const csvContent = [
        ['Date', 'Price (TZS)'],
        ...this.trendData.map(item => [
          this.formatDate(item.date),
          item.price.toLocaleString()
        ])
      ].map(row => row.join(',')).join('\n');

      const blob = new Blob([csvContent], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `price-trends-${this.selectedCrop}-${new Date().toISOString().split('T')[0]}.csv`;
      a.click();
      window.URL.revokeObjectURL(url);
    }
  }
};
</script>

<style scoped>
.price-trends-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9f5e9 100%);
}

.page-header {
  background: linear-gradient(135deg, #198754 0%, #20c997 100%);
}

.card {
  border-radius: 0.75rem;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.stat-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.chart-container {
  position: relative;
  width: 100%;
}

.empty-state {
  padding: 3rem;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 0.5rem;
}

.form-select:focus {
  border-color: #198754;
  box-shadow: 0 0 0 0.25rem rgba(25, 135, 84, 0.25);
}

.btn-primary {
  background: linear-gradient(135deg, #198754 0%, #20c997 100%);
  border: none;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #146c43 0%, #1aa179 100%);
  transform: translateY(-1px);
}

:root {
  --gradient-primary: linear-gradient(135deg, #198754 0%, #20c997 100%);
  --success-color: linear-gradient(135deg, #198754 0%, #20c997 100%);
  --info-color: linear-gradient(135deg, #0d6efd 0%, #0dcaf0 100%);
  --warning-color: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
  --danger-color: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
}
</style>
