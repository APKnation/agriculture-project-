<template>
  <div class="farmer-dashboard-wrapper">
    <div class="container-fluid py-4">
      <!-- Welcome Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="welcome-hero bg-gradient-success text-white p-4 rounded-3 shadow-sm">
            <div class="d-flex justify-content-between align-items-center flex-wrap gap-3">
              <div>
                <h2 class="fw-bold mb-2">
                  <i class="bi bi-person-circle me-2"></i>
                  Farmer Dashboard
                </h2>
                <p v-if="user.username" class="mb-0 fs-5 opacity-90">
                  <i class="bi bi-hand-thumbs-up me-2"></i>
                  Welcome, <strong>{{ user.username }}</strong> from <strong>{{ user.region }}</strong>
                </p>
                <p v-else class="mb-0 opacity-75">Loading your profile...</p>
              </div>
              <div class="text-end">
                <div class="badge bg-white text-success px-3 py-2 fs-6">
                  <i class="bi bi-calendar3 me-2"></i>
                  {{ currentDate }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" style="width: 3rem; height: 3rem;" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="text-muted mt-3">Loading your dashboard...</p>
      </div>

      <!-- Main Content -->
      <div v-else>
        <!-- Quick Stats -->
        <div class="row g-4 mb-4">
          <div class="col-md-3 col-sm-6">
            <div class="stat-card card border-0 shadow-sm">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <p class="text-muted small text-uppercase mb-2">My Crops</p>
                    <h3 class="fw-bold mb-0">{{ crops.length }}</h3>
                  </div>
                  <div class="icon-box bg-success bg-opacity-10 text-success">
                    <i class="bi bi-flower1"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-3 col-sm-6">
            <div class="stat-card card border-0 shadow-sm">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <p class="text-muted small text-uppercase mb-2">Notifications</p>
                    <h3 class="fw-bold mb-0">{{ notifications.length }}</h3>
                  </div>
                  <div class="icon-box bg-warning bg-opacity-10 text-warning">
                    <i class="bi bi-bell-fill"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-3 col-sm-6">
            <div class="stat-card card border-0 shadow-sm">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <p class="text-muted small text-uppercase mb-2">Market Prices</p>
                    <h3 class="fw-bold mb-0">{{ marketPrices.length }}</h3>
                  </div>
                  <div class="icon-box bg-info bg-opacity-10 text-info">
                    <i class="bi bi-graph-up"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-3 col-sm-6">
            <div class="stat-card card border-0 shadow-sm">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <p class="text-muted small text-uppercase mb-2">Farming Tips</p>
                    <h3 class="fw-bold mb-0">{{ tips.length }}</h3>
                  </div>
                  <div class="icon-box bg-primary bg-opacity-10 text-primary">
                    <i class="bi bi-lightbulb-fill"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Main Content Grid -->
        <div class="row g-4 mb-4">
          <!-- Your Crops -->
          <div class="col-lg-8">
            <div class="card border-0 shadow-sm h-100">
              <div class="card-header bg-white border-bottom py-3">
                <h5 class="mb-0 fw-bold">
                  <i class="bi bi-tree text-success me-2"></i>
                  Your Crops
                </h5>
              </div>
              <div class="card-body p-0">
                <!-- Empty State -->
                <div v-if="crops.length === 0" class="text-center py-5">
                  <i class="bi bi-inbox display-4 text-muted mb-3"></i>
                  <h5 class="text-muted">No Crops Yet</h5>
                  <p class="text-muted">Add your first crop to get started</p>
                </div>

                <!-- Crops List -->
                <div v-else class="list-group list-group-flush">
                  <div 
                    v-for="crop in crops" 
                    :key="crop.id"
                    class="list-group-item list-group-item-action crop-item"
                  >
                    <div class="row align-items-center">
                      <div class="col-md-4">
                        <div class="d-flex align-items-center">
                          <div class="crop-icon me-3">
                            <i class="bi bi-flower2"></i>
                          </div>
                          <div>
                            <h6 class="mb-0 fw-bold">{{ crop.name }}</h6>
                            <small class="text-muted">Crop ID: #{{ crop.id }}</small>
                          </div>
                        </div>
                      </div>
                      <div class="col-md-8">
                        <div class="row text-center text-md-start">
                          <div class="col-md-4 mt-3 mt-md-0">
                            <small class="text-muted d-block">Planted</small>
                            <strong>{{ formatDate(crop.planting_date) }}</strong>
                          </div>
                          <div class="col-md-4 mt-3 mt-md-0">
                            <small class="text-muted d-block">Expected Harvest</small>
                            <strong>{{ formatDate(crop.expected_harvest_date) }}</strong>
                          </div>
                          <div class="col-md-4 mt-3 mt-md-0">
                            <small class="text-muted d-block">Yield Estimate</small>
                            <strong class="text-success">{{ crop.yield_estimate }} tons</strong>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Weather & Notifications -->
          <div class="col-lg-4">
            <!-- Weather Card -->
            <div class="card border-0 shadow-sm mb-4">
              <div class="card-header bg-white border-bottom py-3">
                <h5 class="mb-0 fw-bold">
                  <i class="bi bi-cloud-sun text-warning me-2"></i>
                  Weather Forecast
                </h5>
              </div>
              <div class="card-body">
                <div v-if="weather.summary" class="text-center">
                  <i class="bi bi-cloud-sun-fill display-1 text-warning mb-3"></i>
                  <h3 class="fw-bold mb-2">{{ weather.temperature }}°C</h3>
                  <p class="text-muted mb-0">{{ weather.summary }}</p>
                  <div class="alert alert-info mt-3 mb-0" role="alert">
                    <small>
                      <i class="bi bi-info-circle me-1"></i>
                      Weather data for {{ user.region }}
                    </small>
                  </div>
                </div>
                <div v-else class="text-center py-4">
                  <i class="bi bi-cloud-slash display-4 text-muted mb-3"></i>
                  <p class="text-muted">No weather data available</p>
                </div>
              </div>
            </div>

            <!-- Quick Notifications -->
            <div class="card border-0 shadow-sm">
              <div class="card-header bg-white border-bottom py-3">
                <div class="d-flex justify-content-between align-items-center">
                  <h5 class="mb-0 fw-bold">
                    <i class="bi bi-bell text-warning me-2"></i>
                    Notifications
                  </h5>
                  <span class="badge bg-warning">{{ notifications.length }}</span>
                </div>
              </div>
              <div class="card-body p-0" style="max-height: 300px; overflow-y: auto;">
                <div v-if="notifications.length === 0" class="text-center py-4">
                  <i class="bi bi-bell-slash display-4 text-muted mb-3"></i>
                  <p class="text-muted small">No notifications</p>
                </div>
                <div v-else class="list-group list-group-flush">
                  <div 
                    v-for="note in notifications" 
                    :key="note.id"
                    class="list-group-item notification-item"
                  >
                    <div class="d-flex align-items-start">
                      <div class="notification-dot me-3"></div>
                      <p class="mb-0 small">{{ note.message }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Market Prices & Farming Tips -->
        <div class="row g-4">
          <!-- Market Prices -->
          <div class="col-lg-6">
            <div class="card border-0 shadow-sm h-100">
              <div class="card-header bg-white border-bottom py-3">
                <h5 class="mb-0 fw-bold">
                  <i class="bi bi-cash-stack text-success me-2"></i>
                  Market Prices in {{ user.region }}
                </h5>
              </div>
              <div class="card-body p-0">
                <div v-if="marketPrices.length === 0" class="text-center py-5">
                  <i class="bi bi-graph-down display-4 text-muted mb-3"></i>
                  <h6 class="text-muted">No Market Prices Available</h6>
                </div>
                <div v-else class="table-responsive">
                  <table class="table table-hover mb-0">
                    <thead class="table-light">
                      <tr>
                        <th class="px-4 py-3">Crop</th>
                        <th class="px-4 py-3">Region</th>
                        <th class="px-4 py-3 text-end">Price</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="price in marketPrices" :key="price.id">
                        <td class="px-4 py-3">
                          <strong>{{ price.crop_name }}</strong>
                        </td>
                        <td class="px-4 py-3">
                          <span class="badge bg-info-subtle text-info">
                            <i class="bi bi-geo-alt me-1"></i>
                            {{ price.region }}
                          </span>
                        </td>
                        <td class="px-4 py-3 text-end">
                          <span class="text-success fw-bold fs-5">
                            {{ formatPrice(price.price) }} TZS
                          </span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          <!-- Farming Tips -->
          <div class="col-lg-6">
            <div class="card border-0 shadow-sm h-100">
              <div class="card-header bg-white border-bottom py-3">
                <h5 class="mb-0 fw-bold">
                  <i class="bi bi-lightbulb text-primary me-2"></i>
                  Farming Tips for {{ user.region }}
                </h5>
              </div>
              <div class="card-body">
                <div v-if="tips.length === 0" class="text-center py-4">
                  <i class="bi bi-journal-x display-4 text-muted mb-3"></i>
                  <h6 class="text-muted">No Tips Available</h6>
                </div>
                <div v-else>
                  <div 
                    v-for="tip in tips" 
                    :key="tip.id"
                    class="tip-card mb-3 p-3 rounded border"
                  >
                    <div class="d-flex align-items-start">
                      <div class="tip-icon me-3">
                        <i class="bi bi-lightbulb-fill"></i>
                      </div>
                      <div>
                        <h6 class="fw-bold mb-2">
                          <i class="bi bi-star-fill text-warning me-1"></i>
                          {{ tip.title }}
                        </h6>
                        <p class="mb-0 text-muted small">{{ tip.content }}</p>
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
import axios from '../axios';

export default {
  data() {
    return { 
      user: {}, 
      crops: [], 
      marketPrices: [], 
      weather: {}, 
      notifications: [], 
      tips: [],
      loading: true
    };
  },
  computed: {
    currentDate() {
      const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
      return new Date().toLocaleDateString('en-US', options);
    }
  },
  async mounted() {
    await this.loadDashboard();
  },
  methods: {
    async loadDashboard() {
      this.loading = true;
      
      try {
        // Test with a fresh token directly
        console.log('🔄 Getting fresh token...');
        const loginRes = await axios.post('/auth/login/', {
          username: 'apk',
          password: '1212'
        });
        
        const freshToken = loginRes.data.token;
        console.log('🔑 Fresh token:', freshToken);
        
        // Use the fresh token for the request
        const userRes = await axios.get('/users/me/', {
          headers: { Authorization: `Bearer ${freshToken}` }
        });
        console.log('✅ User data received:', userRes.data);
        this.user = userRes.data;

        // Fetch all data in parallel
        const [cropsRes, pricesRes, notesRes, tipsRes, weatherRes] = await Promise.all([
          axios.get(`/crops/?farmer=${this.user.id}`),
          axios.get(`/price-records/?region=${this.user.region}`),
          axios.get(`/notifications/?user=${this.user.id}`),
          axios.get(`/tips/?region=${this.user.region}`),
          axios.get(`/weather/?region=${this.user.region}`)
        ]);

        this.crops = cropsRes.data;
        this.marketPrices = pricesRes.data;
        this.notifications = notesRes.data;
        this.tips = tipsRes.data;
        this.weather = weatherRes.data;

      } catch (error) {
        console.error('Error loading dashboard:', error);
        if (error.response && error.response.status === 401) {
          this.$router.push('/login');
        }
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
    
    formatPrice(price) {
      return new Intl.NumberFormat('en-TZ').format(price);
    }
  }
};
</script>

<style scoped>
.farmer-dashboard-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.welcome-hero {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  animation: fadeIn 0.5s ease-out;
}

.stat-card {
  transition: all 0.3s ease;
  border-radius: 12px;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
}

.icon-box {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.crop-icon {
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  flex-shrink: 0;
}

.crop-item {
  transition: all 0.2s ease;
  padding: 1.25rem;
}

.crop-item:hover {
  background-color: rgba(40, 167, 69, 0.05);
  transform: translateX(5px);
}

.notification-item {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-dot {
  width: 8px;
  height: 8px;
  background: #ffc107;
  border-radius: 50%;
  margin-top: 6px;
  flex-shrink: 0;
}

.tip-card {
  background: rgba(13, 110, 253, 0.03);
  border-color: rgba(13, 110, 253, 0.1) !important;
  transition: all 0.3s ease;
}

.tip-card:hover {
  background: rgba(13, 110, 253, 0.08);
  transform: translateX(5px);
}

.tip-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #0d6efd 0%, #0dcaf0 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card {
  border-radius: 12px;
  animation: fadeIn 0.5s ease-out;
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

.table thead {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.table th {
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.5px;
  border: none !important;
}

.bg-info-subtle {
  background-color: rgba(13, 202, 240, 0.1) !important;
}

@media (max-width: 768px) {
  .stat-card {
    margin-bottom: 1rem;
  }
  
  .crop-item .row > div {
    margin-top: 0.75rem;
  }
}
</style>