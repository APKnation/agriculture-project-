<template>
  <div class="dashboard-wrapper">
    <div class="container-fluid py-4 py-lg-5">
      <!-- Welcome Header -->
      <div class="row mb-4 mb-lg-5">
        <div class="col-12">
          <div class="welcome-card bg-gradient-primary text-white p-4 p-lg-5 rounded-4 shadow-lg">
            <div class="d-flex justify-content-between align-items-center flex-wrap gap-3">
              <div>
                <h1 class="fw-bold mb-3 display-5">
                  <i class="bi bi-sun me-2 me-lg-3"></i>
                  Welcome back, {{ farmerName }}!
                </h1>
                <p class="mb-0 opacity-90 lead">
                  <i class="bi bi-calendar3 me-2"></i>
                  {{ currentDate }}
                </p>
              </div>
              <div class="text-end">
                <div class="badge bg-white text-primary px-4 py-3 fs-5">
                  <i class="bi bi-clipboard-data me-2"></i>
                  {{ totalCrops }} Crops Tracked
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="d-flex flex-column align-items-center">
          <div class="spinner-border text-success mb-4" style="width: 4rem; height: 4rem;" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <div class="text-center">
            <h4 class="text-muted mb-2">Loading Your Dashboard</h4>
            <p class="text-muted">Fetching your agricultural data...</p>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div v-else>
        <!-- Key Metrics -->
        <div class="row g-4 g-lg-5 mb-4 mb-lg-5">
          <!-- Total Crops -->
          <div class="col-12 col-md-6 col-xl-3">
            <div class="metric-card card border-0 shadow-lg h-100">
              <div class="card-body p-4">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <p class="text-muted text-uppercase small fw-semibold mb-3">
                      <i class="bi bi-tree me-2"></i>My Crops
                    </p>
                    <h3 class="fw-bold mb-1">{{ totalCrops }}</h3>
                    <small class="text-success">
                      <i class="bi bi-check-circle-fill me-1"></i>Active
                    </small>
                  </div>
                  <div class="metric-icon bg-success bg-opacity-10 text-success">
                    <i class="bi bi-flower1"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Unread Notifications -->
          <div class="col-12 col-md-6 col-xl-3">
            <div class="metric-card card border-0 shadow-sm h-100">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <p class="text-muted text-uppercase small fw-semibold mb-2">
                      <i class="bi bi-bell me-1"></i>Notifications
                    </p>
                    <h3 class="fw-bold mb-1">{{ unreadNotifications }}</h3>
                    <small :class="unreadNotifications > 0 ? 'text-warning' : 'text-muted'">
                      <i :class="unreadNotifications > 0 ? 'bi bi-exclamation-circle-fill' : 'bi bi-check-circle'" class="me-1"></i>
                      {{ unreadNotifications > 0 ? 'Unread' : 'All caught up' }}
                    </small>
                  </div>
                  <div class="metric-icon bg-warning bg-opacity-10 text-warning">
                    <i class="bi bi-bell-fill"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Price Records -->
          <div class="col-12 col-md-6 col-xl-3">
            <div class="metric-card card border-0 shadow-sm h-100">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <p class="text-muted text-uppercase small fw-semibold mb-2">
                      <i class="bi bi-graph-up me-1"></i>Price Records
                    </p>
                    <h3 class="fw-bold mb-1">{{ totalPriceRecords }}</h3>
                    <small class="text-info">
                      <i class="bi bi-geo-alt-fill me-1"></i>{{ totalRegions }} Regions
                    </small>
                  </div>
                  <div class="metric-icon bg-info bg-opacity-10 text-info">
                    <i class="bi bi-cash-stack"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Average Market Price -->
          <div class="col-12 col-md-6 col-xl-3">
            <div class="metric-card card border-0 shadow-sm h-100">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <p class="text-muted text-uppercase small fw-semibold mb-2">
                      <i class="bi bi-currency-exchange me-1"></i>Avg Market Price
                    </p>
                    <h3 class="fw-bold mb-1">{{ averageMarketPrice }}</h3>
                    <small class="text-primary">
                      <i class="bi bi-activity me-1"></i>TZS per kg
                    </small>
                  </div>
                  <div class="metric-icon bg-primary bg-opacity-10 text-primary">
                    <i class="bi bi-coin"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Main Content Grid -->
        <div class="row g-4 mb-4">
          <!-- My Crops Table -->
          <div class="col-lg-7">
            <div class="card border-0 shadow-sm h-100">
              <div class="card-header bg-white border-bottom py-3">
                <div class="d-flex justify-content-between align-items-center">
                  <h5 class="mb-0 fw-bold">
                    <i class="bi bi-list-check text-success me-2"></i>
                    My Crops
                  </h5>
                  <router-link to="/crops" class="btn btn-sm btn-outline-success">
                    <i class="bi bi-plus-circle me-1"></i>Add Crop
                  </router-link>
                </div>
              </div>
              <div class="card-body p-0">
                <!-- Empty State -->
                <div v-if="crops.length === 0" class="text-center py-5">
                  <i class="bi bi-inbox display-4 text-muted mb-3"></i>
                  <h5 class="text-muted">No Crops Yet</h5>
                  <p class="text-muted">Add your first crop to get started</p>
                  <router-link to="/crops" class="btn btn-success">
                    <i class="bi bi-plus-circle me-2"></i>Add Your First Crop
                  </router-link>
                </div>

                <!-- Crops List -->
                <div v-else class="table-responsive">
                  <table class="table table-hover mb-0">
                    <thead class="table-light">
                      <tr>
                        <th class="px-4 py-3">Crop Name</th>
                        <th class="px-4 py-3">Category</th>
                        <th class="px-4 py-3">Season</th>
                        <th class="px-4 py-3 text-end">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="crop in crops" :key="crop.id">
                        <td class="px-4 py-3">
                          <div class="d-flex align-items-center">
                            <div class="crop-badge me-3">
                              <i class="bi bi-flower2"></i>
                            </div>
                            <span class="fw-semibold">{{ crop.name }}</span>
                          </div>
                        </td>
                        <td class="px-4 py-3">
                          <span class="badge bg-success-subtle text-success">
                            {{ crop.category || 'General' }}
                          </span>
                        </td>
                        <td class="px-4 py-3">
                          <span class="text-muted">{{ crop.season || 'All Year' }}</span>
                        </td>
                        <td class="px-4 py-3 text-end">
                          <button class="btn btn-sm btn-outline-primary" @click="viewCropPrices(crop.id)">
                            <i class="bi bi-graph-up me-1"></i>View Prices
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Notifications -->
          <div class="col-lg-5">
            <div class="card border-0 shadow-sm h-100">
              <div class="card-header bg-white border-bottom py-3">
                <div class="d-flex justify-content-between align-items-center">
                  <h5 class="mb-0 fw-bold">
                    <i class="bi bi-bell text-warning me-2"></i>
                    Recent Notifications
                  </h5>
                  <router-link to="/notifications" class="btn btn-sm btn-outline-warning">
                    View All
                  </router-link>
                </div>
              </div>
              <div class="card-body p-0">
                <!-- Empty State -->
                <div v-if="notifications.length === 0" class="text-center py-5">
                  <i class="bi bi-bell-slash display-4 text-muted mb-3"></i>
                  <h6 class="text-muted">No Notifications</h6>
                  <p class="text-muted small">You're all caught up!</p>
                </div>

                <!-- Notifications List -->
                <div v-else class="notification-list">
                  <div 
                    v-for="notification in recentNotifications" 
                    :key="notification.id"
                    class="notification-item p-3 border-bottom"
                    :class="{ 'unread': !notification.read }"
                  >
                    <div class="d-flex">
                      <div class="notification-icon me-3">
                        <i class="bi bi-info-circle-fill"></i>
                      </div>
                      <div class="flex-grow-1">
                        <h6 class="mb-1 fw-semibold">{{ notification.crop?.name || 'System Notification' }}</h6>
                        <p class="mb-1 small">{{ notification.message }}</p>
                        <small class="text-muted">
                          <i class="bi bi-clock me-1"></i>
                          {{ formatTimeAgo(notification.created_at) }}
                        </small>
                      </div>
                      <div v-if="!notification.read" class="ms-2">
                        <span class="badge bg-primary rounded-circle" style="width: 8px; height: 8px;"></span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions & Regional Insights -->
        <div class="row g-4">
          <!-- Quick Actions -->
          <div class="col-lg-4">
            <div class="card border-0 shadow-sm">
              <div class="card-header bg-white border-bottom py-3">
                <h5 class="mb-0 fw-bold">
                  <i class="bi bi-lightning-charge text-primary me-2"></i>
                  Quick Actions
                </h5>
              </div>
              <div class="card-body">
                <div class="d-grid gap-2">
                  <router-link to="/price-comparison" class="btn btn-outline-primary text-start">
                    <i class="bi bi-graph-up-arrow me-2"></i>
                    Compare Regional Prices
                  </router-link>
                  <router-link to="/notifications" class="btn btn-outline-warning text-start">
                    <i class="bi bi-bell me-2"></i>
                    View Selling Alerts
                  </router-link>
                  <router-link to="/crops" class="btn btn-outline-success text-start">
                    <i class="bi bi-plus-circle me-2"></i>
                    Add New Crop
                  </router-link>
                  <button class="btn btn-outline-info text-start" @click="refreshDashboard">
                    <i class="bi bi-arrow-clockwise me-2"></i>
                    Refresh Data
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Top Regions by Price -->
          <div class="col-lg-8">
            <div class="card border-0 shadow-sm">
              <div class="card-header bg-white border-bottom py-3">
                <h5 class="mb-0 fw-bold">
                  <i class="bi bi-bar-chart text-info me-2"></i>
                  Top Regions by Average Price
                </h5>
              </div>
              <div class="card-body">
                <!-- Empty State -->
                <div v-if="topRegions.length === 0" class="text-center py-4">
                  <i class="bi bi-map display-4 text-muted mb-3"></i>
                  <p class="text-muted">No regional data available yet</p>
                </div>

                <!-- Regions List -->
                <div v-else>
                  <div 
                    v-for="(region, index) in topRegions" 
                    :key="index"
                    class="region-item d-flex justify-content-between align-items-center mb-3 p-3 rounded"
                  >
                    <div class="d-flex align-items-center">
                      <div class="region-rank me-3">
                        {{ index + 1 }}
                      </div>
                      <div>
                        <h6 class="mb-0 fw-semibold">
                          <i class="bi bi-geo-alt-fill text-danger me-2"></i>
                          {{ region.region }}
                        </h6>
                        <small class="text-muted">{{ region.count }} price records</small>
                      </div>
                    </div>
                    <div class="text-end">
                      <div class="fw-bold text-success fs-5">
                        TZS {{ formatPrice(region.avg_price) }}
                      </div>
                      <small class="text-muted">avg price</small>
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
import axios from 'axios';

export default {
  name: 'Dashboard',
  data() {
    return {
      loading: true,
      farmerName: 'Farmer',
      crops: [],
      notifications: [],
      priceRecords: [],
      topRegions: [],
      
      // Metrics
      totalCrops: 0,
      unreadNotifications: 0,
      totalPriceRecords: 0,
      totalRegions: 0,
      averageMarketPrice: 'TZS 0'
    };
  },
  computed: {
    currentDate() {
      const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
      return new Date().toLocaleDateString('en-US', options);
    },
    recentNotifications() {
      return this.notifications.slice(0, 5);
    }
  },
  async mounted() {
    await this.loadDashboardData();
  },
  methods: {
    async loadDashboardData() {
      this.loading = true;
      try {
        // Fetch all data in parallel
        const [cropsRes, notificationsRes, priceRecordsRes] = await Promise.all([
          axios.get('/crops/'),
          axios.get('/notifications/'),
          axios.get('/price-records/')
        ]);

        // Store data
        this.crops = Array.isArray(cropsRes.data) ? cropsRes.data : [];
        this.notifications = Array.isArray(notificationsRes.data) ? notificationsRes.data : [];
        this.priceRecords = Array.isArray(priceRecordsRes.data) ? priceRecordsRes.data : [];

        console.log('📊 Dashboard data loaded:');
        console.log('Crops:', this.crops.length);
        console.log('Notifications:', this.notifications.length);
        console.log('Price Records:', this.priceRecords.length);

        // Calculate metrics
        this.calculateMetrics();
        
      } catch (error) {
        console.error('Error loading dashboard data:', error);
        console.error('Error details:', error.response?.data || error.message);
        
        // Don't automatically redirect to login on data loading errors
        // Only redirect on authentication errors (401)
        if (error.response?.status === 401) {
          console.log('🔐 Authentication error - redirecting to login');
          this.$router.push('/login');
        } else {
          console.log('📊 Data loading error - showing error message');
          this.errorMessage = 'Failed to load dashboard data. Please try refreshing the page.';
        }
      } finally {
        this.loading = false;
      }
    },
    
    calculateMetrics() {
      // Total crops
      this.totalCrops = this.crops.length;
      
      // Unread notifications
      this.unreadNotifications = this.notifications.filter(n => !n.read).length;
      
      // Total price records
      this.totalPriceRecords = this.priceRecords.length;
      
      // Unique regions
      const regions = new Set(this.priceRecords.map(p => p.region));
      this.totalRegions = regions.size;
      
      // Average market price
      if (this.priceRecords.length > 0) {
        const total = this.priceRecords.reduce((sum, record) => sum + parseFloat(record.price), 0);
        const avg = total / this.priceRecords.length;
        this.averageMarketPrice = `TZS ${this.formatPrice(avg.toFixed(2))}`;
      }
      
      // Top regions by average price
      this.calculateTopRegions();
    },
    
    calculateTopRegions() {
      const regionMap = {};
      
      this.priceRecords.forEach(record => {
        if (!regionMap[record.region]) {
          regionMap[record.region] = {
            region: record.region,
            total: 0,
            count: 0
          };
        }
        regionMap[record.region].total += parseFloat(record.price);
        regionMap[record.region].count += 1;
      });
      
      this.topRegions = Object.values(regionMap)
        .map(r => ({
          region: r.region,
          avg_price: r.total / r.count,
          count: r.count
        }))
        .sort((a, b) => b.avg_price - a.avg_price)
        .slice(0, 5);
    },
    
    formatPrice(price) {
      return new Intl.NumberFormat('en-TZ').format(price);
    },
    
    formatTimeAgo(dateString) {
      const date = new Date(dateString);
      const now = new Date();
      const seconds = Math.floor((now - date) / 1000);
      
      if (seconds < 60) return 'Just now';
      if (seconds < 3600) return `${Math.floor(seconds / 60)} minutes ago`;
      if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
      if (seconds < 604800) return `${Math.floor(seconds / 86400)} days ago`;
      
      return date.toLocaleDateString();
    },
    
    viewCropPrices(cropId) {
      this.$router.push(`/price-comparison?crop=${cropId}`);
    },
    
    async refreshDashboard() {
      await this.loadDashboardData();
    }
  }
};
</script>

<style scoped>
.dashboard-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.welcome-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  animation: fadeIn 0.5s ease-out;
}

.metric-card {
  transition: all 0.3s ease;
  border-radius: 12px;
}

.metric-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
}

.metric-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.crop-badge {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.notification-item {
  transition: all 0.2s ease;
}

.notification-item:hover {
  background-color: rgba(102, 126, 234, 0.05);
}

.notification-item.unread {
  background-color: rgba(13, 110, 253, 0.05);
  border-left: 3px solid #0d6efd;
}

.notification-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #ffc107 0%, #ff9800 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

<style scoped>
.dashboard-wrapper {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  min-height: 100vh;
}

.welcome-card {
  background: linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%);
  border: none;
  box-shadow: 0 8px 25px rgba(13, 110, 253, 0.3);
}

.metric-card {
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
  border-color: #dee2e6;
}

.metric-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.region-item {
  background: rgba(13, 110, 253, 0.03);
  border: 1px solid rgba(13, 110, 253, 0.1);
  transition: all 0.3s ease;
  border-radius: 0.75rem;
}

.region-item:hover {
  background: rgba(13, 110, 253, 0.08);
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.region-rank {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.1rem;
}

.card {
  border-radius: 1rem;
  animation: fadeIn 0.5s ease-out;
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.btn {
  border-radius: 0.5rem;
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Mobile Responsive Enhancements */
@media (max-width: 768px) {
  .dashboard-wrapper {
    padding: 1rem 0;
  }
  
  .welcome-card {
    padding: 2rem 1.5rem !important;
  }
  
  .metric-card .card-body {
    padding: 1.5rem !important;
  }
  
  .metric-icon {
    width: 50px;
    height: 50px;
    font-size: 1.25rem;
  }
  
  .region-rank {
    width: 35px;
    height: 35px;
    font-size: 1rem;
  }
}

@media (max-width: 576px) {
  .welcome-card {
    padding: 1.5rem 1rem !important;
  }
  
  .metric-card .card-body {
    padding: 1rem !important;
  }
  
  .metric-icon {
    width: 45px;
    height: 45px;
    font-size: 1.125rem;
  }
  
  .region-rank {
    width: 30px;
    height: 30px;
    font-size: 0.875rem;
  }
}
</style>