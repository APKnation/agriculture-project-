<template>
  <div class="marketplace-wrapper">
    <div class="container-fluid py-4 py-lg-5">
      <!-- Header -->
      <div class="row mb-4 mb-lg-5">
        <div class="col-12">
          <div class="marketplace-header bg-gradient-info text-white p-4 p-lg-5 rounded-4 shadow-lg">
            <div class="row align-items-center">
              <div class="col-md-8">
                <h1 class="fw-bold mb-3 display-5">
                  <i class="bi bi-shop me-2 me-lg-3"></i>
                  Farmer Marketplace
                </h1>
                <p class="mb-0 opacity-90 lead">
                  Connect with local farmers and find fresh produce
                </p>
              </div>
              <div class="col-md-4 text-md-end mt-3 mt-md-0">
                <div class="d-flex flex-column flex-md-row gap-2 align-items-md-end justify-content-md-end">
                  <div class="badge bg-white text-info fs-6 px-3 py-2">
                    <i class="bi bi-basket me-1"></i>
                    {{ posts.length }} Listings
                  </div>
                  <button @click="refreshMarketplace" 
                          :disabled="loading"
                          class="btn btn-outline-light btn-lg">
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

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="d-flex flex-column align-items-center">
          <div class="spinner-border text-info mb-4" style="width: 4rem; height: 4rem;" role="status">
            <span class="visually-hidden">Loading marketplace posts...</span>
          </div>
          <div class="text-center">
            <h4 class="text-muted mb-2">Loading Marketplace</h4>
            <p class="text-muted">Fetching fresh produce listings...</p>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-5">
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
          <i class="bi bi-exclamation-triangle-fill me-2"></i>
          {{ error }}
          <button type="button" class="btn-close" @click="error = null"></button>
        </div>
      </div>

      <!-- Marketplace Posts -->
      <div v-else class="row">
        <div class="col-12">
          <!-- Search and Filter Bar -->
          <div class="card border-0 shadow-sm mb-4">
            <div class="card-body p-3 p-lg-4">
              <div class="row g-3 align-items-center">
                <div class="col-md-4">
                  <div class="input-group input-group-lg">
                    <span class="input-group-text bg-light border-end-0">
                      <i class="bi bi-search text-info"></i>
                    </span>
                    <input 
                      v-model="searchQuery" 
                      type="text" 
                      class="form-control border-start-0" 
                      placeholder="Search crops, farmers..."
                    />
                  </div>
                </div>
                <div class="col-md-3">
                  <select v-model="selectedCrop" class="form-select form-select-lg">
                    <option value="">All Crops</option>
                    <option value="wheat">Wheat</option>
                    <option value="corn">Corn</option>
                    <option value="tomatoes">Tomatoes</option>
                    <option value="potatoes">Potatoes</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <select v-model="sortBy" class="form-select form-select-lg">
                    <option value="newest">Newest First</option>
                    <option value="price-low">Price: Low to High</option>
                    <option value="price-high">Price: High to Low</option>
                  </select>
                </div>
                <div class="col-md-2">
                  <button @click="applyFilters" class="btn btn-info btn-lg w-100">
                    <i class="bi bi-funnel me-2"></i>Filter
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Posts Grid -->
          <div class="row g-4">
            <div v-for="post in filteredPosts" :key="post.id" class="col-12 col-md-6 col-lg-4">
              <div class="marketplace-card card border-0 shadow-lg h-100">
                <div class="card-header bg-white border-0 p-0">
                  <div class="crop-image-placeholder bg-gradient-success text-white text-center py-4">
                    <i class="bi bi-flower1 display-4"></i>
                  </div>
                </div>
                <div class="card-body p-4">
                  <div class="mb-3">
                    <span class="badge bg-success fs-6 mb-2">{{ post.crop_name }}</span>
                    <h5 class="card-title fw-bold mb-2">{{ post.farmer_username }}'s Produce</h5>
                  </div>
                  
                  <div class="marketplace-details mb-3">
                    <div class="row g-2">
                      <div class="col-6">
                        <div class="detail-item p-2 bg-light rounded-3">
                          <div class="text-muted small mb-1">Quantity</div>
                          <div class="fw-semibold fs-5">{{ post.quantity }} kg</div>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="detail-item p-2 bg-light rounded-3">
                          <div class="text-muted small mb-1">Price</div>
                          <div class="fw-semibold fs-5 text-success">${{ post.price }}/kg</div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="contact-section">
                    <button @click="contactFarmer(post.contact)" 
                            class="btn btn-info btn-lg w-100">
                      <i class="bi bi-envelope me-2"></i>
                      Contact Farmer
                    </button>
                  </div>
                </div>
                <div class="card-footer bg-light text-center p-3">
                  <small class="text-muted">
                    <i class="bi bi-clock me-1"></i>
                    Listed {{ formatDate(post.created_at) }}
                  </small>
                </div>
              </div>
            </div>
          </div>

          <!-- No Posts State -->
          <div v-if="filteredPosts.length === 0" class="text-center py-5">
            <div class="card border-0 shadow-sm">
              <div class="card-body p-5">
                <i class="bi bi-inbox display-1 text-muted mb-3"></i>
                <h4 class="text-muted mb-2">No Marketplace Listings</h4>
                <p class="text-muted">No posts found matching your criteria. Try adjusting your filters.</p>
                <button @click="clearFilters" class="btn btn-outline-info mt-3">
                  <i class="bi bi-arrow-clockwise me-2"></i>Clear Filters
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const posts = ref([])
const loading = ref(true)
const error = ref(null)
const searchQuery = ref('')
const selectedCrop = ref('')
const sortBy = ref('newest')

// Computed property for filtered posts
const filteredPosts = computed(() => {
  let filtered = posts.value
  
  // Apply search filter
  if (searchQuery.value) {
    filtered = filtered.filter(post => 
      post.crop_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      post.farmer_username.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
  
  // Apply crop filter
  if (selectedCrop.value) {
    filtered = filtered.filter(post => post.crop_name.toLowerCase() === selectedCrop.value.toLowerCase())
  }
  
  // Apply sorting
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'price-low':
        return parseFloat(a.price) - parseFloat(b.price)
      case 'price-high':
        return parseFloat(b.price) - parseFloat(a.price)
      case 'newest':
      default:
        return new Date(b.created_at) - new Date(a.created_at)
    }
  })
  
  return filtered
})

onMounted(async () => {
  try {
    const res = await axios.get('/market-posts/')
    posts.value = res.data
  } catch (err) {
    console.error(err)
  }
})

const refreshPosts = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await axios.get('/market-posts/')
    posts.value = res.data
  } catch (err) {
    console.error(err)
    error.value = 'Failed to refresh marketplace posts.'
  } finally {
    loading.value = false
  }
}

const applyFilters = () => {
  // Filters are applied automatically through computed property
  console.log('Filters applied')
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedCrop.value = ''
  sortBy.value = 'newest'
}

const contactFarmer = (contact) => {
  // Enhanced contact method
  if (confirm(`Contact this farmer at: ${contact}?`)) {
    // This could open a modal, email client, or messaging system
    window.open(`mailto:${contact}`, '_blank')
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'Unknown'
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) return 'today'
  if (diffDays === 2) return 'yesterday'
  if (diffDays <= 7) return `${diffDays - 1} days ago`
  
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}
</script>

<style scoped>
.marketplace-wrapper {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  min-height: 100vh;
}

.marketplace-header {
  background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
  border: none;
  box-shadow: 0 8px 25px rgba(23, 162, 184, 0.3);
}

.marketplace-card {
  transition: all 0.3s ease;
  border: 1px solid transparent;
  overflow: hidden;
}

.marketplace-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.15);
  border-color: #dee2e6;
}

.crop-image-placeholder {
  background: linear-gradient(135deg, #198754 0%, #20c997 100%);
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.detail-item {
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.detail-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #e9ecef;
}

.contact-section {
  margin-top: auto;
}

.card {
  border-radius: 1rem;
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
}

.form-control {
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
  border: 2px solid #e9ecef;
}

.form-control:focus {
  border-color: #17a2b8;
  box-shadow: 0 0 0 0.2rem rgba(23, 162, 184, 0.25);
}

.input-group-text {
  border-radius: 0.5rem 0 0 0.5rem;
  border: 2px solid #e9ecef;
  border-right: none;
  background: #f8f9fa;
}

.input-group-lg .form-control {
  border-radius: 0 0.5rem 0.5rem 0;
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

.btn-info {
  background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
  border: none;
}

.btn-info:hover {
  background: linear-gradient(135deg, #138496 0%, #117a8b 100%);
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
  .marketplace-wrapper {
    padding: 1rem 0;
  }
  
  .marketplace-header {
    padding: 2rem 1.5rem !important;
  }
  
  .display-5 {
    font-size: 2rem !important;
  }
  
  .crop-image-placeholder {
    height: 80px;
  }
  
  .marketplace-card .card-body {
    padding: 1.5rem !important;
  }
}

@media (max-width: 576px) {
  .marketplace-header {
    padding: 1.5rem 1rem !important;
  }
  
  .display-5 {
    font-size: 1.75rem !important;
  }
  
  .crop-image-placeholder {
    height: 60px;
  }
  
  .marketplace-card .card-body {
    padding: 1rem !important;
  }
  
  .btn-lg {
    padding: 0.5rem 1rem;
    font-size: 1rem;
  }
}
</style>