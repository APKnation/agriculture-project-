<template>
  <div class="officer-dashboard">
    <!-- Header Section -->
    <div class="dashboard-header bg-gradient-success text-white p-4 mb-4 rounded-3 shadow-lg">
      <div class="container-fluid">
        <div class="row align-items-center">
          <div class="col-md-6">
            <h1 class="mb-0 fw-bold">
              <i class="bi bi-clipboard-data me-3"></i>
              Market Officer Dashboard
            </h1>
          </div>
          <div class="col-md-6 text-md-end">
            <div class="user-info">
              <span class="badge bg-white text-success fs-6 mb-2">
                <i class="bi bi-person-circle me-2"></i>
                {{ user.username }}
              </span>
              <div class="text-white-50">
                <i class="bi bi-geo-alt me-1"></i>
                {{ user.region }} Region
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container-fluid">
      <!-- Quick Stats -->
      <div class="row mb-4">
        <div class="col-md-3 mb-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center">
              <div class="text-primary mb-2">
                <i class="bi bi-currency-dollar fs-1"></i>
              </div>
              <h5 class="card-title">Total Markets</h5>
              <p class="card-text fs-4 fw-bold text-primary">{{ totalMarkets }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center">
              <div class="text-success mb-2">
                <i class="bi bi-graph-up fs-1"></i>
              </div>
              <h5 class="card-title">Price Records</h5>
              <p class="card-text fs-4 fw-bold text-success">{{ totalPriceRecords }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center">
              <div class="text-info mb-2">
                <i class="bi bi-exclamation-triangle fs-1"></i>
              </div>
              <h5 class="card-title">Price Alerts</h5>
              <p class="card-text fs-4 fw-bold text-info">{{ totalAlerts }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center">
              <div class="text-warning mb-2">
                <i class="bi bi-people fs-1"></i>
              </div>
              <h5 class="card-title">Active Farmers</h5>
              <p class="card-text fs-4 fw-bold text-warning">{{ totalFarmers }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="row">
        <!-- Price Management -->
        <div class="col-lg-6 mb-4">
          <div class="card border-0 shadow-lg">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">
                <i class="bi bi-plus-circle me-2"></i>
                Add Price Record
              </h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="addPriceRecord">
                <div class="mb-3">
                  <label class="form-label fw-semibold">
                    <i class="bi bi-flower1 me-2"></i>
                    Select Crop
                  </label>
                  <select v-model="cropId" class="form-select form-select-lg" required>
                    <option value="">Choose a crop...</option>
                    <option v-for="crop in crops" :key="crop.id" :value="crop.id">
                      {{ crop.name }}
                    </option>
                  </select>
                </div>
                <div class="mb-3">
                  <label class="form-label fw-semibold">
                    <i class="bi bi-geo-alt me-2"></i>
                    Region
                  </label>
                  <input v-model="region" type="text" class="form-control form-control-lg" 
                         placeholder="Enter region" required />
                </div>
                <div class="mb-3">
                  <label class="form-label fw-semibold">
                    <i class="bi bi-currency-dollar me-2"></i>
                    Price (TZS)
                  </label>
                  <input v-model="price" type="number" step="0.01" class="form-control form-control-lg" 
                         placeholder="Enter price" required />
                </div>
                <button type="submit" class="btn btn-primary btn-lg w-100" 
                        :disabled="loading || !cropId || !region || !price">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  <i class="bi bi-check-circle me-2"></i>
                  Add Price Record
                </button>
              </form>
            </div>
          </div>
        </div>

        <!-- Recent Price Records -->
        <div class="col-lg-6 mb-4">
          <div class="card border-0 shadow-lg">
            <div class="card-header bg-success text-white">
              <h5 class="mb-0">
                <i class="bi bi-clock-history me-2"></i>
                Recent Price Records
              </h5>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2 mb-0">Loading price records...</p>
              </div>
              <div v-else-if="recentRecords.length === 0" class="text-center py-4">
                <i class="bi bi-inbox fs-1 text-muted"></i>
                <p class="text-muted mt-2 mb-0">No recent price records</p>
              </div>
              <div v-else class="recent-records">
                <div v-for="record in recentRecords" :key="record.id" 
                     class="record-item d-flex justify-content-between align-items-center py-2 border-bottom">
                  <div>
                    <strong>{{ record.crop?.name || 'Unknown' }}</strong>
                    <div class="text-muted small">
                      <i class="bi bi-geo-alt me-1"></i>
                      {{ record.region }}
                    </div>
                  </div>
                  <div class="text-end">
                    <span class="badge bg-success fs-6">TZS {{ record.price }}</span>
                    <div class="text-muted small">
                      {{ formatDate(record.date) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Market Overview -->
      <div class="row mt-4">
        <div class="col-12">
          <div class="card border-0 shadow-lg">
            <div class="card-header bg-info text-white">
              <h5 class="mb-0">
                <i class="bi bi-graph-up-arrow me-2"></i>
                Market Overview
              </h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-md-4">
                  <h6 class="text-muted">Top Performing Crops</h6>
                  <div v-if="topCrops.length > 0">
                    <div v-for="crop in topCrops" :key="crop.name" 
                         class="d-flex justify-content-between align-items-center py-1">
                      <span>{{ crop.name }}</span>
                      <span class="badge bg-success">TZS {{ crop.avg_price }}</span>
                    </div>
                  </div>
                  <div v-else class="text-muted">
                    <i class="bi bi-dash-circle"></i> No data available
                  </div>
                </div>
                <div class="col-md-4">
                  <h6 class="text-muted">Active Regions</h6>
                  <div v-if="activeRegions.length > 0">
                    <div v-for="region in activeRegions" :key="region.name" 
                         class="d-flex justify-content-between align-items-center py-1">
                      <span>{{ region.name }}</span>
                      <span class="badge bg-info">{{ region.count }}</span>
                    </div>
                  </div>
                  <div v-else class="text-muted">
                    <i class="bi bi-dash-circle"></i> No data available
                  </div>
                </div>
                <div class="col-md-4">
                  <h6 class="text-muted">Recent Activity</h6>
                  <div class="small">
                    <div class="d-flex align-items-center py-1">
                      <i class="bi bi-plus-circle text-success me-2"></i>
                      <span>{{ recentActivity.price_records || 0 }} price records added</span>
                    </div>
                    <div class="d-flex align-items-center py-1">
                      <i class="bi bi-exclamation-triangle text-warning me-2"></i>
                      <span>{{ recentActivity.alerts || 0 }} price alerts created</span>
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
import axios from '../axios';

export default {
  name: 'OfficerDashboard',
  data() {
    return { 
      user: {}, 
      crops: [], 
      cropId: null, 
      region: '', 
      price: '',
      loading: false,
      recentRecords: [],
      totalMarkets: 0,
      totalPriceRecords: 0,
      totalAlerts: 0,
      totalFarmers: 0,
      topCrops: [],
      activeRegions: [],
      recentActivity: {}
    };
  },
  async mounted() {
    await this.loadDashboardData();
  },
  methods: {
    async loadDashboardData() {
      this.loading = true;
      try {
        // Get current user
        const userRes = await axios.get('/users/me/');
        this.user = userRes.data;

        // Load all data in parallel
        const [cropsRes, priceRes, alertsRes, usersRes] = await Promise.all([
          axios.get('/crops/'),
          axios.get('/price-records/?limit=10'),
          axios.get('/price-alerts/?limit=5'),
          axios.get('/users/')
        ]);

        this.crops = cropsRes.data;
        this.recentRecords = priceRes.data;
        this.totalPriceRecords = priceRes.data.length;
        this.totalAlerts = alertsRes.data.length;
        
        // Calculate statistics
        this.calculateStatistics(usersRes.data, priceRes.data);
        
      } catch (error) {
        console.error('Error loading dashboard data:', error);
      } finally {
        this.loading = false;
      }
    },

    calculateStatistics(users, priceRecords) {
      // Total farmers
      this.totalFarmers = users.filter(u => u.role === 'farmer').length;
      
      // Total markets (unique regions from price records)
      const uniqueRegions = [...new Set(priceRecords.map(r => r.region))];
      this.totalMarkets = uniqueRegions.length;
      
      // Top performing crops
      const cropPrices = {};
      priceRecords.forEach(record => {
        if (!cropPrices[record.crop?.name]) {
          cropPrices[record.crop?.name] = [];
        }
        cropPrices[record.crop?.name].push(record.price);
      });
      
      this.topCrops = Object.entries(cropPrices)
        .map(([name, prices]) => ({
          name,
          avg_price: (prices.reduce((a, b) => a + b, 0) / prices.length).toFixed(2)
        }))
        .sort((a, b) => b.avg_price - a.avg_price)
        .slice(0, 5);
      
      // Active regions
      const regionCounts = {};
      priceRecords.forEach(record => {
        regionCounts[record.region] = (regionCounts[record.region] || 0) + 1;
      });
      
      this.activeRegions = Object.entries(regionCounts)
        .map(([name, count]) => ({ name, count }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 5);
      
      // Recent activity (mock data for now)
      this.recentActivity = {
        price_records: Math.floor(Math.random() * 10),
        alerts: Math.floor(Math.random() * 5)
      };
    },

    async addPriceRecord() {
      this.loading = true;
      try {
        await axios.post('/price-records/', {
          crop: this.cropId,
          region: this.region,
          price: parseFloat(this.price)
        });
        
        // Reset form
        this.cropId = null;
        this.region = '';
        this.price = '';
        
        // Reload data
        await this.loadDashboardData();
        
        // Show success message
        this.showSuccessMessage('Price record added successfully!');
        
      } catch (error) {
        console.error('Error adding price record:', error);
        this.showErrorMessage('Failed to add price record. Please try again.');
      } finally {
        this.loading = false;
      }
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      });
    },

    showSuccessMessage(message) {
      // Create a simple success notification
      const alertDiv = document.createElement('div');
      alertDiv.className = 'alert alert-success alert-dismissible fade show position-fixed';
      alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
      alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      `;
      document.body.appendChild(alertDiv);
      
      // Auto remove after 3 seconds
      setTimeout(() => {
        if (alertDiv.parentNode) {
          alertDiv.parentNode.removeChild(alertDiv);
        }
      }, 3000);
    },

    showErrorMessage(message) {
      // Create a simple error notification
      const alertDiv = document.createElement('div');
      alertDiv.className = 'alert alert-danger alert-dismissible fade show position-fixed';
      alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
      alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      `;
      document.body.appendChild(alertDiv);
      
      // Auto remove after 5 seconds
      setTimeout(() => {
        if (alertDiv.parentNode) {
          alertDiv.parentNode.removeChild(alertDiv);
        }
      }, 5000);
    }
  }
};
</script>

<style scoped>
.officer-dashboard {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.dashboard-header {
  background: linear-gradient(135deg, #198754 0%, #20c997 100%);
}

.record-item:hover {
  background-color: #f8f9fa;
}

.card {
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
}

.position-fixed {
  position: fixed;
}

.badge {
  font-size: 0.8em;
}

.text-primary {
  color: #0d6efd !important;
}

.text-success {
  color: #198754 !important;
}

.text-info {
  color: #0dcaf0 !important;
}

.text-warning {
  color: #ffc107 !important;
}

.bg-gradient-success {
  background: linear-gradient(135deg, #198754 0%, #20c997 100%);
}
</style>
