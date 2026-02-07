<template>
  <div class="weather-dashboard">
    <div class="container-fluid py-4 py-lg-5">
      <!-- Header -->
      <div class="row mb-4 mb-lg-5">
        <div class="col-12">
          <div class="weather-header bg-gradient-info text-white p-4 p-lg-5 rounded-4 shadow-lg">
            <div class="row align-items-center">
              <div class="col-md-8">
                <h1 class="fw-bold mb-3 mb-md-2 display-5">
                  <i class="bi bi-cloud-sun me-2 me-lg-3"></i>
                  Weather Dashboard
                </h1>
                <p class="mb-0 opacity-90 lead">Real-time weather data and farming recommendations</p>
              </div>
              <div class="col-md-4 text-md-end mt-3 mt-md-0">
                <div class="d-flex flex-column flex-md-row gap-2 justify-content-md-end">
                  <span class="badge bg-white text-info fs-6">
                    <i class="bi bi-clock me-1"></i>
                    {{ currentTime }}
                  </span>
                  <span class="badge bg-white text-info fs-6">
                    <i class="bi bi-calendar me-1"></i>
                    {{ currentDate }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Region Selector -->
      <div class="row mb-4 mb-lg-5">
        <div class="col-12">
          <div class="card border-0 shadow-lg">
            <div class="card-body p-4 p-lg-5">
              <div class="row align-items-center">
                <div class="col-lg-6 mb-3 mb-lg-0">
                  <label class="form-label fw-semibold fs-5">
                    <i class="bi bi-geo-alt me-2"></i>
                    Select Region
                  </label>
                  <select v-model="selectedRegion" @change="fetchWeatherData" 
                          class="form-select form-select-lg">
                    <option value="" disabled>Choose a region...</option>
                    <option v-for="region in regions" :key="region.name" :value="region.name">
                      {{ region.name }} ({{ region.crop_count }} crops)
                    </option>
                  </select>
                  <div v-if="selectedRegion" class="region-info mt-2">
                    <small class="text-muted">
                      <i class="bi bi-info-circle me-1"></i>
                      <span v-if="regions.find(r => r.name === selectedRegion)">
                        {{ regions.find(r => r.name === selectedRegion).crops.join(', ') }}
                      </span>
                    </small>
                  </div>
                </div>
                <div class="col-lg-6">
                  <div class="d-flex flex-column flex-lg-row gap-3 align-items-center justify-content-lg-end h-100">
                    <button @click="checkWeatherAlerts" 
                            :disabled="!selectedRegion || loading"
                            class="btn btn-primary btn-lg px-4">
                      <i class="bi bi-exclamation-triangle me-2"></i>
                      <span class="d-none d-sm-inline">Check Alerts</span>
                      <span class="d-sm-none">Alerts</span>
                    </button>
                    <button @click="refreshWeather" 
                            :disabled="!selectedRegion || loading"
                            class="btn btn-outline-primary btn-lg px-4">
                      <i class="bi bi-arrow-clockwise me-2"></i>
                      <span class="d-none d-sm-inline">Refresh</span>
                      <span class="d-sm-none">↻</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="d-flex flex-column align-items-center">
          <div class="spinner-border text-info mb-4" style="width: 4rem; height: 4rem;" role="status">
            <span class="visually-hidden">Loading weather data...</span>
          </div>
          <div class="text-center">
            <h4 class="text-muted mb-2">Loading Weather Data</h4>
            <p class="text-muted">Fetching latest weather information for {{ selectedRegion || 'your region' }}...</p>
          </div>
        </div>
      </div>

      <!-- Weather Content -->
      <div v-else-if="selectedRegion && currentWeather">
        <!-- Current Weather Card -->
        <div class="row g-4 g-lg-5 mb-4 mb-lg-5">
          <div class="col-12">
            <div class="card border-0 shadow-lg h-100">
              <div class="card-header bg-gradient-primary text-white border-0 p-4 p-lg-5">
                <h4 class="card-title mb-0">
                  <i class="bi bi-cloud-sun me-2"></i>
                  Current Weather - {{ selectedRegion }}
                </h4>
                <div class="text-end">
                  <span class="badge bg-white text-primary fs-6">
                    <i class="bi bi-clock me-1"></i>
                    {{ formatDateTime(currentWeather.created_at) }}
                  </span>
                </div>
              </div>
              <div class="card-body p-4 p-lg-5">
                <div class="row align-items-center">
                  <div class="col-md-4 text-center mb-4 mb-md-0">
                    <div class="weather-icon mb-3">
                      <i :class="getWeatherIcon(currentWeather.weather_condition)" 
                         class="display-1 text-primary"></i>
                    </div>
                    <h2 class="fw-bold mb-0 display-4">{{ currentWeather.temperature }}°C</h2>
                    <p class="text-muted fs-5">{{ currentWeather.weather_condition }}</p>
                  </div>
                  <div class="col-md-8">
                    <div class="row g-3 g-lg-4">
                      <div class="col-6">
                        <div class="weather-stat p-3 bg-light rounded-3">
                          <div class="stat-label text-muted small mb-2">
                            <i class="bi bi-droplet me-2"></i>
                            Humidity
                          </div>
                          <div class="stat-value fw-semibold fs-4 text-info">
                            {{ currentWeather.humidity }}%
                          </div>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="weather-stat p-3 bg-light rounded-3">
                          <div class="stat-label text-muted small mb-2">
                            <i class="bi bi-cloud-rain me-2"></i>
                            Rainfall
                          </div>
                          <div class="stat-value fw-semibold fs-4 text-primary">
                            {{ currentWeather.rainfall || 0 }}mm
                          </div>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="weather-stat p-3 bg-light rounded-3">
                          <div class="stat-label text-muted small mb-2">
                            <i class="bi bi-wind me-2"></i>
                            Wind Speed
                          </div>
                          <div class="stat-value fw-semibold fs-4 text-success">
                            {{ currentWeather.wind_speed || 0 }} km/h
                          </div>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="weather-stat p-3 bg-light rounded-3">
                          <div class="stat-label text-muted small mb-2">
                            <i class="bi bi-thermometer me-2"></i>
                            Feels Like
                          </div>
                          <div class="stat-value fw-semibold fs-4 text-warning">
                            {{ getFeelsLikeTemperature(currentWeather.temperature) }}
                          </div>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="weather-stat p-3 bg-light rounded-3">
                          <div class="stat-label text-muted small mb-2">
                            <i class="bi bi-eye me-2"></i>
                            Visibility
                          </div>
                          <div class="stat-value fw-semibold fs-4 text-secondary">
                            {{ currentWeather.visibility || 10 }}km
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="row g-3 g-lg-4">
                      <div class="col-6">
                        <div class="weather-stat p-3 bg-light rounded-3">
                          <div class="stat-label text-muted small mb-2">
                            <i class="bi bi-sunrise me-2"></i>
                            Sunrise
                          </div>
                          <div class="stat-value fw-semibold fs-4 text-warning">
                            {{ formatTime(currentWeather.sunrise) }}
                          </div>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="weather-stat p-3 bg-light rounded-3">
                          <div class="stat-label text-muted small mb-2">
                            <i class="bi bi-sunset me-2"></i>
                            Sunset
                          </div>
                          <div class="stat-value fw-semibold fs-4 text-warning">
                            {{ formatTime(currentWeather.sunset) }}
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

        <!-- Weather Forecast -->
        <div class="row g-4 mb-4 mb-lg-5">
          <div class="col-12">
            <div class="card border-0 shadow-lg">
              <div class="card-header bg-gradient-info text-white border-0 p-4 p-lg-5">
                <h4 class="card-title mb-0">
                  <i class="bi bi-calendar-week me-2"></i>
                  5-Day Weather Forecast
                  <span class="badge bg-white text-info fs-6 ms-2">
                    <i class="bi bi-info-circle me-1"></i>
                    {{ forecast.length }} Days
                  </span>
                </h4>
              </div>
              <div class="card-body p-4 p-lg-5">
                <div v-if="forecast.length === 0" class="text-center text-muted py-5">
                  <i class="bi bi-info-circle display-4 mb-3"></i>
                  <h5 class="text-muted mb-2">No Forecast Data Available</h5>
                  <p class="text-muted">Try selecting a different region.</p>
                </div>
                <div v-else class="forecast-grid">
                  <div class="row g-3 g-lg-4">
                    <div v-for="day in forecast" :key="day.date" class="col-md-2 col-sm-4 col-lg-3">
                      <div class="forecast-card text-center p-4 border rounded-3 shadow-sm">
                        <div class="forecast-date fw-semibold mb-2">
                          {{ formatDate(day.date) }}
                        </div>
                        <div class="forecast-icon mb-2">
                          <i :class="getWeatherIcon(day.weather_condition)" 
                             class="fs-3 text-primary"></i>
                        </div>
                        <div class="forecast-temp fw-bold mb-1">
                          {{ Math.round(day.temperature) }}°C
                        </div>
                        <div class="forecast-condition small text-muted mb-1">
                          {{ day.weather_condition }}
                        </div>
                        <div class="forecast-details small">
                          <div><i class="bi bi-droplet text-info"></i> {{ day.rainfall || 0 }}mm</div>
                          <div><i class="bi bi-wind text-success"></i> {{ Math.round(day.wind_speed || 0) }}km/h</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Farming Recommendations -->
        <div class="row g-4 mb-4 mb-lg-5">
          <div class="col-lg-6">
            <div class="card border-0 shadow-lg h-100">
              <div class="card-header bg-gradient-success text-white border-0 p-4 p-lg-5">
                <h4 class="card-title mb-0">
                  <i class="bi bi-lightbulb me-2"></i>
                  General Recommendations
                  <span class="badge bg-white text-success fs-6 ms-2">
                    <i class="bi bi-check-circle me-1"></i>
                    {{ recommendations.general_recommendations ? recommendations.general_recommendations.length : 0 }} Tips
                  </span>
                </h4>
              </div>
              <div class="card-body p-4 p-lg-5">
                <div v-if="recommendations.general_recommendations">
                  <div class="recommendations-list">
                    <div v-for="(rec, index) in recommendations.general_recommendations" 
                         :key="index" class="recommendation-item p-3 mb-3 bg-light rounded-3">
                      <div class="d-flex align-items-start">
                        <div class="recommendation-icon bg-success bg-opacity-10 text-success me-3">
                          <i class="bi bi-check-circle-fill"></i>
                        </div>
                        <div class="flex-grow-1">
                          <div class="recommendation-text fs-5">{{ rec }}</div>
                          <div class="recommendation-meta small text-muted">
                            <i class="bi bi-clock me-1"></i>
                            Based on current {{ selectedRegion }} conditions
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="text-center text-muted py-4">
                  <i class="bi bi-info-circle display-4 mb-3"></i>
                  <h5 class="text-muted mb-2">No Recommendations Available</h5>
                  <p class="text-muted">Check back later for farming recommendations based on current weather conditions.</p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-lg-6">
            <div class="card border-0 shadow-lg h-100">
              <div class="card-header bg-gradient-primary text-white border-0 p-4 p-lg-5">
                <h4 class="card-title mb-0">
                  <i class="bi bi-seedling me-2"></i>
                  Crop-Specific Recommendations
                  <span class="badge bg-white text-primary fs-6 ms-2">
                    <i class="bi bi-flower1 me-1"></i>
                    {{ recommendations.crop_specific_recommendations ? recommendations.crop_specific_recommendations.length : 0 }} Crops
                  </span>
                </h4>
              </div>
              <div class="card-body p-4 p-lg-5">
                <div v-if="recommendations.crop_specific_recommendations">
                  <div class="crop-recommendations">
                    <div v-for="crop in recommendations.crop_specific_recommendations" 
                         :key="crop.crop" class="crop-rec mb-4 p-3 bg-light rounded-3">
                      <div class="crop-header d-flex justify-content-between align-items-center mb-3">
                        <div class="d-flex align-items-center">
                          <div class="crop-icon bg-primary bg-opacity-10 text-white me-3">
                            <i :class="getCropIcon(crop.crop)" class="fs-4"></i>
                          </div>
                          <div>
                            <div class="crop-name fw-semibold text-primary fs-5">{{ crop.crop }}</div>
                            <div class="crop-region small text-muted">{{ getMarketName(crop.market) }}</div>
                          </div>
                        </div>
                        <div class="crop-priority">
                          <span :class="`badge bg-${getPriorityColor(crop.priority)} fs-6 px-3 py-2`">
                            <i class="bi bi-flag me-1"></i>{{ crop.priority }} Priority
                          </span>
                        </div>
                      </div>
                      <div class="crop-recommendation mb-3 fs-6">{{ crop.recommendation }}</div>
                      <div class="crop-actions mt-2">
                        <button class="btn btn-sm btn-outline-primary me-2">
                          <i class="bi bi-info-circle"></i>
                          View Details
                        </button>
                        <button class="btn btn-sm btn-success ms-2">
                          <i class="bi bi-bookmark"></i>
                          Save Recommendation
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="text-center text-muted py-4">
                  <i class="bi bi-info-circle display-4 mb-3"></i>
                  <h5 class="text-muted mb-2">No Crop-Specific Recommendations</h5>
                  <p class="text-muted">Add crops to your profile to get personalized farming advice.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- No Region Selected -->
      <div v-else class="text-center py-5">
        <div class="container">
          <div class="row justify-content-center">
            <div class="col-lg-8">
              <div class="card border-0 shadow-lg">
                <div class="card-body p-5">
                  <i class="bi bi-geo-alt display-1 text-muted mb-4"></i>
                  <h2 class="text-muted mb-3">Select a Region to View Weather Data</h2>
                  <p class="text-muted fs-5 mb-4">
                    Choose your farming region from the dropdown above to get started with real-time weather information and farming recommendations.
                  </p>
                  <div class="d-flex flex-column flex-sm-row gap-3 justify-content-center">
                    <button @click="selectRegion('North')" class="btn btn-outline-primary btn-lg">
                      <i class="bi bi-compass me-2"></i> North Region
                    </button>
                    <button @click="selectRegion('South')" class="btn btn-outline-primary btn-lg">
                      <i class="bi bi-compass me-2"></i> South Region
                    </button>
                    <button @click="selectRegion('East')" class="btn btn-outline-primary btn-lg">
                      <i class="bi bi-compass me-2"></i> East Region
                    </button>
                    <button @click="selectRegion('West')" class="btn btn-outline-primary btn-lg">
                      <i class="bi bi-compass me-2"></i> West Region
                    </button>
                    <button @click="selectRegion('Central')" class="btn btn-outline-primary btn-lg">
                      <i class="bi bi-compass me-2"></i> Central Region
                    </button>
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
import { ref, onMounted, watch } from 'vue'
import axios from '../axios'

export default {
  name: 'WeatherDashboard',
  setup() {
    const regions = ref([])
    const selectedRegion = ref('')
    const currentWeather = ref(null)
    const forecast = ref([])
    const alerts = ref([])
    const recommendations = ref({})
    const loading = ref(false)
    const currentTime = ref('')
    const currentDate = ref('')

    // Update current time and date
    const updateDateTime = () => {
      const now = new Date()
      currentTime.value = now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
      })
      currentDate.value = now.toLocaleDateString('en-US', { 
        weekday: 'short', 
        month: 'short', 
        day: 'numeric' 
      })
    }

    // Initialize date/time and update every minute
    updateDateTime()
    const timeInterval = setInterval(updateDateTime, 60000)

    const selectRegion = (region) => {
      selectedRegion.value = region
      fetchWeatherData()
    }

    const fetchRegions = async () => {
      try {
        const response = await axios.get('/regions/')
        regions.value = response.data
        
        // Auto-select first region if none selected
        if (!selectedRegion.value && regions.value.length > 0) {
          selectedRegion.value = regions.value[0].name
        }
      } catch (error) {
        console.error('Error fetching regions:', error)
      }
    }

    const fetchWeatherData = async () => {
      if (!selectedRegion.value) return
      
      loading.value = true
      try {
        // Fetch current weather
        const currentResponse = await axios.get('/api/weather/current/', {
          params: { region: selectedRegion.value }
        })
        currentWeather.value = currentResponse.data

        // Fetch forecast
        const forecastResponse = await axios.get('/api/weather/forecast/', {
          params: { region: selectedRegion.value, days: 5 }
        })
        forecast.value = forecastResponse.data

        // Fetch alerts
        const alertsResponse = await axios.get('/api/weather/alerts/', {
          params: { region: selectedRegion.value }
        })
        alerts.value = alertsResponse.data

        // Fetch recommendations
        const recResponse = await axios.get('/api/weather/recommendations/', {
          params: { region: selectedRegion.value }
        })
        recommendations.value = recResponse.data

      } catch (error) {
        console.error('Error fetching weather data:', error)
      } finally {
        loading.value = false
      }
    }

    const checkWeatherAlerts = async () => {
      if (!selectedRegion.value) return
      
      try {
        const response = await axios.post('/api/weather/check_alerts/', {
          region: selectedRegion.value
        })
        
        // Refresh alerts after checking
        const alertsResponse = await axios.get('/api/weather/alerts/', {
          params: { region: selectedRegion.value }
        })
        alerts.value = alertsResponse.data

      } catch (error) {
        console.error('Error checking weather alerts:', error)
      }
    }

    const refreshWeather = () => {
      fetchWeatherData()
    }

    const getWeatherIcon = (condition) => {
      const icons = {
        'Clear': 'bi-sun-fill text-warning',
        'Clouds': 'bi-cloud-fill text-secondary',
        'Rain': 'bi-cloud-rain-fill text-primary',
        'Snow': 'bi-snow text-info',
        'Thunderstorm': 'bi-cloud-lightning-fill text-warning',
        'Drizzle': 'bi-cloud-drizzle-fill text-primary',
        'Mist': 'bi-cloud-haze text-secondary',
        'Fog': 'bi-cloud-fog text-secondary'
      }
      return icons[condition] || 'bi-cloud-fill text-secondary'
    }

    const getAlertIcon = (severity) => {
      const icons = {
        'low': 'bi-info-circle text-info',
        'medium': 'bi-exclamation-circle text-warning',
        'high': 'bi-exclamation-triangle text-danger',
        'critical': 'bi-exclamation-triangle-fill text-danger'
      }
      return icons[severity] || 'bi-info-circle text-info'
    }

    const getPriorityColor = (priority) => {
      const colors = {
        'low': 'success',
        'medium': 'warning',
        'high': 'danger',
        'critical': 'danger'
      }
      return colors[priority] || 'secondary'
    }

    const getFeelsLikeTemperature = (temp) => {
      if (temp >= 35) return 'Very Hot'
      if (temp >= 28) return 'Hot'
      if (temp >= 21) return 'Warm'
      if (temp >= 15) return 'Cool'
      if (temp >= 10) return 'Mild'
      return 'Cold'
    }

    const formatTime = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const formatDateTime = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    onMounted(() => {
      fetchRegions()
    })

    watch(selectedRegion, (newRegion) => {
      if (newRegion) {
        fetchWeatherData()
      }
    })

    return {
      regions,
      selectedRegion,
      loading,
      currentWeather,
      forecast,
      alerts,
      recommendations,
      currentTime,
      currentDate,
      fetchWeatherData,
      checkWeatherAlerts,
      refreshWeather,
      selectRegion,
      getWeatherIcon,
      getAlertIcon,
      getPriorityColor,
      formatDate,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.weather-dashboard {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  min-height: 100vh;
}

.weather-header {
  background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
  border: none;
  box-shadow: 0 8px 25px rgba(23, 162, 184, 0.3);
}

.weather-stat {
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.weather-stat:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #dee2e6;
}

.alert-item {
  transition: all 0.3s ease;
  border-left: 4px solid;
}

.alert-low {
  border-left-color: #17a2b8;
  background-color: rgba(23, 162, 184, 0.05);
}

.alert-medium {
  border-left-color: #ffc107;
  background-color: rgba(255, 193, 7, 0.05);
}

.alert-high {
  border-left-color: #dc3545;
  background-color: rgba(220, 53, 69, 0.05);
}

.alert-critical {
  border-left-color: #6f42c1;
  background-color: rgba(111, 66, 193, 0.05);
}

.alert-item:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.crop-rec {
  transition: all 0.3s ease;
}

.crop-rec:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.weather-icon {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.card {
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
}

.btn {
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.form-select {
  transition: all 0.3s ease;
}

.form-select:focus {
  border-color: #17a2b8;
  box-shadow: 0 0 0 0.2rem rgba(23, 162, 184, 0.25);
}

/* Mobile Responsive Enhancements */
@media (max-width: 768px) {
  .weather-dashboard {
    padding: 1rem 0;
  }
  
  .weather-header {
    padding: 2rem 1.5rem !important;
  }
  
  .card-body {
    padding: 1.5rem !important;
  }
  
  .display-4 {
    font-size: 2.5rem !important;
  }
  
  .display-1 {
    font-size: 3rem !important;
  }
}

@media (max-width: 576px) {
  .weather-header {
    padding: 1.5rem 1rem !important;
  }
  
  .card-body {
    padding: 1rem !important;
  }
  
  .display-4 {
    font-size: 2rem !important;
  }
  
  .display-1 {
    font-size: 2.5rem !important;
  }
  
  .btn-lg {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
}

/* Smooth animations */
.spinner-border {
  animation: spinner-border 0.75s linear infinite;
}

/* Custom scrollbar for better UX */
.alert-list::-webkit-scrollbar {
  width: 6px;
}

.alert-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.alert-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 10px;
}

.alert-list::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
