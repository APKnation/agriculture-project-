<template>
  <div class="price-comparison-wrapper">
    <div class="container py-5">
      <!-- Header Section -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="text-center mb-4">
            <h2 class="fw-bold display-6 mb-2">
              <i class="bi bi-graph-up-arrow text-success me-3"></i>
              Regional Price Comparison
            </h2>
            <p class="text-muted lead">
              Compare crop prices across different regions to make informed selling decisions
            </p>
          </div>
        </div>
      </div>

      <!-- Crop Selection Card -->
      <div class="row justify-content-center mb-4">
        <div class="col-lg-8 col-md-10">
          <div class="card border-0 shadow-sm">
            <div class="card-body p-4">
              <label class="form-label fw-semibold mb-3">
                <i class="bi bi-funnel-fill text-primary me-2"></i>
                Select Crop to Compare Prices
              </label>
              <div class="input-group input-group-lg">
                <span class="input-group-text bg-white border-end-0">
                  <i class="bi bi-search text-muted"></i>
                </span>
                <select 
                  v-model="selectedCrop" 
                  @change="fetchComparison"
                  class="form-select form-select-lg border-start-0"
                  :disabled="loading || crops.length === 0"
                >
                  <option :value="null" disabled>Choose a crop...</option>
                  <option v-for="crop in crops" :key="crop.id" :value="crop.id">
                    {{ crop.name }}
                  </option>
                </select>
              </div>
              <small class="text-muted mt-2 d-block">
                <i class="bi bi-info-circle me-1"></i>
                Select a crop to view regional price variations
              </small>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="text-muted mt-3">Loading price data...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="row justify-content-center">
        <div class="col-lg-8">
          <div class="alert alert-danger d-flex align-items-center" role="alert">
            <i class="bi bi-exclamation-triangle-fill me-3 fs-4"></i>
            <div>{{ error }}</div>
          </div>
        </div>
      </div>

      <!-- Empty State - No Crop Selected -->
      <div v-else-if="!selectedCrop" class="row justify-content-center">
        <div class="col-lg-8">
          <div class="empty-state text-center py-5">
            <i class="bi bi-graph-up display-1 text-muted mb-3"></i>
            <h4 class="text-muted mb-3">Select a Crop to Begin</h4>
            <p class="text-muted">
              Choose a crop from the dropdown above to compare prices across different regions
            </p>
          </div>
        </div>
      </div>

      <!-- No Data State -->
      <div v-else-if="comparison.length === 0 && !loading" class="row justify-content-center">
        <div class="col-lg-8">
          <div class="empty-state text-center py-5">
            <i class="bi bi-inbox display-1 text-muted mb-3"></i>
            <h4 class="text-muted mb-3">No Price Data Available</h4>
            <p class="text-muted">
              There are currently no price records for this crop in any region
            </p>
          </div>
        </div>
      </div>

      <!-- Price Comparison Results -->
      <div v-else class="row">
        <!-- Statistics Cards -->
        <div class="col-12 mb-4">
          <div class="row g-3">
            <div class="col-md-4">
              <div class="stat-card bg-success bg-gradient text-white">
                <div class="stat-icon">
                  <i class="bi bi-arrow-up-circle-fill"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-label">Highest Price</div>
                  <div class="stat-value">{{ highestPrice }}</div>
                  <div class="stat-sublabel">{{ highestRegion }}</div>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="stat-card bg-primary bg-gradient text-white">
                <div class="stat-icon">
                  <i class="bi bi-graph-up"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-label">Average Price</div>
                  <div class="stat-value">{{ averagePrice }}</div>
                  <div class="stat-sublabel">Across all regions</div>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="stat-card bg-warning bg-gradient text-white">
                <div class="stat-icon">
                  <i class="bi bi-arrow-down-circle-fill"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-label">Lowest Price</div>
                  <div class="stat-value">{{ lowestPrice }}</div>
                  <div class="stat-sublabel">{{ lowestRegion }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Price List -->
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-bottom py-3">
              <h5 class="mb-0 fw-semibold">
                <i class="bi bi-list-ul text-primary me-2"></i>
                Price by Region ({{ comparison.length }} regions)
              </h5>
            </div>
            <div class="card-body p-0">
              <div class="list-group list-group-flush">
                <div 
                  v-for="(record, index) in sortedComparison" 
                  :key="record.id"
                  class="list-group-item list-group-item-action price-item"
                  :class="getPriceClass(record.price)"
                >
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="d-flex align-items-center">
                      <div class="region-badge me-3">
                        {{ index + 1 }}
                      </div>
                      <div>
                        <h6 class="mb-1 fw-semibold">
                          <i class="bi bi-geo-alt-fill me-2"></i>
                          {{ record.region }}
                        </h6>
                        <small class="text-muted">
                          <i class="bi bi-calendar3 me-1"></i>
                          {{ formatDate(record.date) }}
                        </small>
                      </div>
                    </div>
                    <div class="text-end">
                      <div class="price-tag">
                        <span class="currency">TZS</span>
                        <span class="amount">{{ formatPrice(record.price) }}</span>
                      </div>
                      <div class="price-indicator">
                        <span v-if="isPriceHigh(record.price)" class="badge bg-success-subtle text-success">
                          <i class="bi bi-arrow-up"></i> High
                        </span>
                        <span v-else-if="isPriceLow(record.price)" class="badge bg-danger-subtle text-danger">
                          <i class="bi bi-arrow-down"></i> Low
                        </span>
                        <span v-else class="badge bg-warning-subtle text-warning">
                          <i class="bi bi-dash"></i> Average
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
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return { 
      crops: [], 
      selectedCrop: null, 
      comparison: [],
      loading: false,
      error: null
    };
  },
  computed: {
    sortedComparison() {
      return [...this.comparison].sort((a, b) => b.price - a.price);
    },
    highestPrice() {
      if (this.comparison.length === 0) return 'N/A';
      const highest = Math.max(...this.comparison.map(r => r.price));
      return `TZS ${this.formatPrice(highest)}`;
    },
    lowestPrice() {
      if (this.comparison.length === 0) return 'N/A';
      const lowest = Math.min(...this.comparison.map(r => r.price));
      return `TZS ${this.formatPrice(lowest)}`;
    },
    averagePrice() {
      if (this.comparison.length === 0) return 'N/A';
      const avg = this.comparison.reduce((sum, r) => sum + r.price, 0) / this.comparison.length;
      return `TZS ${this.formatPrice(avg)}`;
    },
    highestRegion() {
      if (this.comparison.length === 0) return '';
      const highest = this.comparison.reduce((max, r) => r.price > max.price ? r : max);
      return highest.region;
    },
    lowestRegion() {
      if (this.comparison.length === 0) return '';
      const lowest = this.comparison.reduce((min, r) => r.price < min.price ? r : min);
      return lowest.region;
    }
  },
  async mounted() {
    await this.fetchCrops();
  },
  methods: {
    async fetchCrops() {
      this.loading = true;
      this.error = null;
      
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/crops/');
        console.log('Crops:', res.data);
        this.crops = res.data;
      } catch (err) {
        console.error('Error fetching crops:', err);
        this.error = 'Failed to load crops. Please try again later.';
      } finally {
        this.loading = false;
      }
    },
    async fetchComparison() {
      if (!this.selectedCrop) return;
      
      this.loading = true;
      this.error = null;
      
      try {
        const res = await axios.get(
          `http://127.0.0.1:8000/api/price-records/?crop=${this.selectedCrop}`
        );
        console.log('Comparison:', res.data);
        this.comparison = res.data;
      } catch (err) {
        console.error('Error fetching comparison:', err);
        this.error = 'Failed to load price comparison. Please try again.';
      } finally {
        this.loading = false;
      }
    },
    formatPrice(price) {
      return new Intl.NumberFormat('en-TZ').format(price);
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
    isPriceHigh(price) {
      if (this.comparison.length === 0) return false;
      const avg = this.comparison.reduce((sum, r) => sum + r.price, 0) / this.comparison.length;
      return price > avg * 1.1; // 10% above average
    },
    isPriceLow(price) {
      if (this.comparison.length === 0) return false;
      const avg = this.comparison.reduce((sum, r) => sum + r.price, 0) / this.comparison.length;
      return price < avg * 0.9; // 10% below average
    },
    getPriceClass(price) {
      if (this.isPriceHigh(price)) return 'border-start border-success border-3';
      if (this.isPriceLow(price)) return 'border-start border-danger border-3';
      return 'border-start border-warning border-3';
    }
  }
};
</script>

<style scoped>
/* Background */
.price-comparison-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Select Styling */
.form-select:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.15);
}

.input-group:focus-within .input-group-text {
  border-color: #0d6efd;
}

/* Statistics Cards */
.stat-card {
  border-radius: 15px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  animation: slideIn 0.5s ease-out;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  font-size: 2.5rem;
  opacity: 0.9;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.9;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.stat-sublabel {
  font-size: 0.75rem;
  opacity: 0.8;
}

/* Price List Items */
.price-item {
  padding: 1.25rem;
  transition: all 0.3s ease;
  cursor: pointer;
}

.price-item:hover {
  background-color: rgba(13, 110, 253, 0.05);
  transform: translateX(5px);
}

.region-badge {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.1rem;
}

.price-tag {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.currency {
  font-size: 0.875rem;
  color: #6c757d;
  font-weight: 500;
}

.amount {
  font-size: 1.5rem;
  font-weight: bold;
  color: #212529;
}

.price-indicator {
  display: flex;
  justify-content: flex-end;
}

/* Empty State */
.empty-state {
  background: white;
  border-radius: 15px;
  padding: 3rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.empty-state i {
  opacity: 0.3;
}

/* Card Styling */
.card {
  border-radius: 15px;
  overflow: hidden;
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

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Badge Styling */
.badge {
  font-weight: 500;
  padding: 0.35rem 0.75rem;
  font-size: 0.8rem;
}

.bg-success-subtle {
  background-color: rgba(25, 135, 84, 0.1) !important;
}

.bg-danger-subtle {
  background-color: rgba(220, 53, 69, 0.1) !important;
}

.bg-warning-subtle {
  background-color: rgba(255, 193, 7, 0.1) !important;
}

/* Responsive */
@media (max-width: 768px) {
  .stat-card {
    flex-direction: column;
    text-align: center;
  }
  
  .stat-icon {
    font-size: 2rem;
  }
  
  .stat-value {
    font-size: 1.5rem;
  }
  
  .price-tag {
    flex-direction: column;
    align-items: flex-end;
    gap: 0.25rem;
  }
  
  .amount {
    font-size: 1.25rem;
  }
}
</style>