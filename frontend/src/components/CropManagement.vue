<template>
  <div class="crop-management">
    <!-- Header Section -->
    <div class="hero-section bg-gradient-primary text-white py-4 mb-4 shadow-lg">
      <div class="container-fluid">
        <div class="row align-items-center">
          <div class="col-md-6">
            <h1 class="mb-0 fw-bold display-6">
              <i class="bi bi-flower1 me-3"></i>
              {{ editMode ? 'Edit Crop' : 'Crop Management' }}
            </h1>
          </div>
          <div class="col-md-6 text-md-end">
            <button @click="showAddModal = true" class="btn btn-light btn-lg shadow-sm hover-lift">
              <i class="bi bi-plus-circle me-2"></i>
              Add New Crop
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters Section -->
    <div class="container-fluid mb-4">
      <div class="row g-3">
        <div class="col-lg-4">
          <div class="input-group input-group-lg">
            <span class="input-group-text bg-light border-0">
              <i class="bi bi-search text-muted"></i>
            </span>
            <input 
              v-model="searchQuery" 
              type="text" 
              class="form-control border-start-0 shadow-sm" 
              placeholder="Search crops by name..."
              @input="filterCrops"
            >
          </div>
        </div>
        <div class="col-lg-3">
          <select v-model="statusFilter" class="form-select form-select-lg shadow-sm" @change="filterCrops">
            <option value="">All Status</option>
            <option value="planted">🌱 Planted</option>
            <option value="growing">🌿 Growing</option>
            <option value="harvested">🌾 Harvested</option>
          </select>
        </div>
        <div class="col-lg-3">
          <select v-model="typeFilter" class="form-select form-select-lg shadow-sm" @change="filterCrops">
            <option value="">All Types</option>
            <option value="vegetables">🥬 Vegetables</option>
            <option value="fruits">🍎 Fruits</option>
            <option value="grains">🌾 Grains</option>
            <option value="legumes">🫘 Legumes</option>
          </select>
        </div>
        <div class="col-lg-2">
          <div class="btn-group w-100" role="group">
            <button 
              @click="viewMode = 'grid'" 
              :class="['btn', 'btn-outline-primary', viewMode === 'grid' ? 'active' : '']"
              class="btn-lg"
            >
              <i class="bi bi-grid-3x3-gap"></i>
            </button>
            <button 
              @click="viewMode = 'list'" 
              :class="['btn', 'btn-outline-primary', viewMode === 'list' ? 'active' : '']"
              class="btn-lg"
            >
              <i class="bi bi-list-ul"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="container-fluid">
      <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading crops...</span>
      </div>
      <p class="mt-2 mb-0 text-muted">Loading your crops...</p>
    </div>

      <div v-else-if="filteredCrops.length === 0" class="text-center py-5">
        <i class="bi bi-inbox display-1 text-muted mb-3"></i>
        <h4 class="text-muted">No crops found</h4>
        <p class="text-muted">
          {{ searchQuery || statusFilter || typeFilter ? 'Try adjusting your filters' : 'Add your first crop to get started' }}
        </p>
        <button @click="showAddModal = true" class="btn btn-primary mt-3">
          <i class="bi bi-plus-circle me-2"></i>
          Add Your First Crop
        </button>
      </div>

      <!-- Grid View -->
      <div v-else-if="viewMode === 'grid'" class="row g-4">
        <div v-for="crop in filteredCrops" :key="crop.id" class="col-lg-3 col-md-4 col-sm-6 mb-4">
          <div class="card crop-card h-100 border-0 shadow-sm hover-lift transition-all">
            <div class="crop-image-container position-relative">
              <img v-if="crop.image_url" :src="crop.image_url" :alt="crop.name" class="crop-image">
              <div v-else class="crop-image-placeholder bg-light">
                <i class="bi bi-image text-muted"></i>
              </div>
              <div class="crop-status-badge position-absolute top-0 end-0 m-2" :class="getStatusClass(crop.status)">
                <i class="bi bi-circle-fill me-1"></i>
                {{ crop.status }}
              </div>
            </div>
            <div class="card-body">
              <h5 class="card-title text-truncate fw-bold">{{ crop.name }}</h5>
              <div class="d-flex align-items-center mb-2">
                <span class="badge bg-light text-dark me-2">
                  <i class="bi bi-tag me-1"></i>
                  {{ crop.type }}
                </span>
              </div>
              <p class="text-muted small mb-3">{{ crop.description || 'No description available' }}</p>
              <div class="crop-details">
                <div class="row g-2">
                  <div class="col-6">
                    <div class="detail-item d-flex align-items-center">
                      <i class="bi bi-calendar-event text-primary me-2"></i>
                      <div>
                        <small class="text-muted d-block">Planted</small>
                        <span class="fw-medium">{{ formatDate(crop.planting_date) }}</span>
                      </div>
                    </div>
                  </div>
                  <div class="col-6">
                    <div class="detail-item d-flex align-items-center">
                      <i class="bi bi-calendar-check text-success me-2"></i>
                      <div>
                        <small class="text-muted d-block">Expected Harvest</small>
                        <span class="fw-medium">{{ formatDate(crop.expected_harvest_date) }}</span>
                      </div>
                    </div>
                  </div>
                  <div class="col-12 mt-2">
                    <div class="detail-item d-flex align-items-center">
                      <i class="bi bi-bar-chart text-warning me-2"></i>
                      <div>
                        <small class="text-muted d-block">Yield Estimate</small>
                        <span class="fw-medium">{{ crop.yield_estimate || 'Not set' }} tons</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="card-footer bg-transparent border-top-0 pt-0">
              <div class="btn-group w-100">
                <button @click="editCrop(crop)" class="btn btn-sm btn-outline-primary hover-scale">
                  <i class="bi bi-pencil me-1"></i>
                  Edit
                </button>
                <button @click="viewCropDetails(crop)" class="btn btn-sm btn-outline-info hover-scale">
                  <i class="bi bi-eye me-1"></i>
                  View
                </button>
                <button @click="deleteCrop(crop)" class="btn btn-sm btn-outline-danger hover-scale">
                  <i class="bi bi-trash me-1"></i>
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- List View -->
      <div v-else class="crop-list">
        <div v-for="crop in filteredCrops" :key="crop.id" class="crop-item card mb-3 border-0 shadow-sm hover-lift">
          <div class="card-body p-0">
            <div class="row align-items-center g-0">
              <div class="col-auto">
                <div class="crop-image-container-small">
                  <img v-if="crop.image_url" :src="crop.image_url" :alt="crop.name" class="crop-image-small">
                  <div v-else class="crop-image-placeholder-small bg-light">
                    <i class="bi bi-image text-muted"></i>
                  </div>
                </div>
              </div>
              <div class="col">
                <div class="p-3">
                  <div class="d-flex align-items-start justify-content-between">
                    <div>
                      <h5 class="card-title fw-bold mb-1">{{ crop.name }}</h5>
                      <div class="d-flex align-items-center mb-2">
                        <span class="badge bg-light text-dark me-2">
                          <i class="bi bi-tag me-1"></i>
                          {{ crop.type }}
                        </span>
                        <span class="badge" :class="getStatusClass(crop.status)">
                          <i class="bi bi-circle-fill me-1"></i>
                          {{ crop.status }}
                        </span>
                      </div>
                      <p class="text-muted small mb-2">{{ crop.description || 'No description available' }}</p>
                      <div class="row g-2">
                        <div class="col-md-4">
                          <small class="text-muted">Planted:</small>
                          <div class="fw-medium">{{ formatDate(crop.planting_date) }}</div>
                        </div>
                        <div class="col-md-4">
                          <small class="text-muted">Expected:</small>
                          <div class="fw-medium">{{ formatDate(crop.expected_harvest_date) }}</div>
                        </div>
                        <div class="col-md-4">
                          <small class="text-muted">Yield:</small>
                          <div class="fw-medium">{{ crop.yield_estimate || 'N/A' }} tons</div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="col-auto">
                    <div class="btn-group-vertical">
                      <button @click="editCrop(crop)" class="btn btn-sm btn-outline-primary mb-2 hover-scale">
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button @click="viewCropDetails(crop)" class="btn btn-sm btn-outline-info mb-2 hover-scale">
                        <i class="bi bi-eye"></i>
                      </button>
                      <button @click="deleteCrop(crop)" class="btn btn-sm btn-outline-danger hover-scale">
                        <i class="bi bi-trash"></i>
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

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal || editMode" class="modal fade show d-flex align-items-center justify-content-center" style="background-color: rgba(0,0,0,0.6);">
      <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg">
          <div class="modal-header bg-gradient-primary text-white border-0">
            <h5 class="modal-title mb-0">
              <i class="bi bi-flower1 me-2"></i>
              {{ editMode ? 'Edit Crop' : 'Add New Crop' }}
            </h5>
            <button type="button" class="btn-close btn-close-white" @click="closeModal">
              <i class="bi bi-x-lg"></i>
            </button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="saveCrop">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label fw-bold">
                    <i class="bi bi-tag me-2"></i>
                    Crop Name
                  </label>
                  <input v-model="cropForm.name" type="text" class="form-control form-control-lg" placeholder="Enter crop name" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold">
                    <i class="bi bi-bookmark me-2"></i>
                    Crop Type
                  </label>
                  <select v-model="cropForm.type" class="form-select form-select-lg" required>
                    <option value="">Select type</option>
                    <option value="vegetables">🥬 Vegetables</option>
                    <option value="fruits">🍎 Fruits</option>
                    <option value="grains">🌾 Grains</option>
                    <option value="legumes">🫘 Legumes</option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold">
                    <i class="bi bi-calendar-event me-2"></i>
                    Planting Date
                  </label>
                  <input v-model="cropForm.planting_date" type="date" class="form-control form-control-lg" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold">
                    <i class="bi bi-calendar-check me-2"></i>
                    Expected Harvest Date
                  </label>
                  <input v-model="cropForm.expected_harvest_date" type="date" class="form-control form-control-lg">
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold">
                    <i class="bi bi-graph-up me-2"></i>
                    Yield Estimate (tons)
                  </label>
                  <input v-model="cropForm.yield_estimate" type="number" step="0.1" class="form-control form-control-lg" placeholder="e.g., 5.5">
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold">
                    <i class="bi bi-flag me-2"></i>
                    Status
                  </label>
                  <select v-model="cropForm.status" class="form-select form-select-lg">
                    <option value="planted">🌱 Planted</option>
                    <option value="growing">🌿 Growing</option>
                    <option value="harvested">🌾 Harvested</option>
                  </select>
                </div>
                <div class="col-12">
                  <label class="form-label fw-bold">
                    <i class="bi bi-text-paragraph me-2"></i>
                    Description
                  </label>
                  <textarea v-model="cropForm.description" class="form-control" rows="3" placeholder="Enter crop description..."></textarea>
                </div>
                <div class="col-12">
                  <label class="form-label fw-bold">
                    <i class="bi bi-image me-2"></i>
                    Crop Image
                  </label>
                  <div class="image-upload-area">
                    <input 
                      ref="cropImageInput" 
                      type="file" 
                      class="form-control" 
                      accept="image/*"
                      @change="previewImage"
                    >
                    <div v-if="cropForm.image_url" class="image-preview mt-3">
                      <img :src="cropForm.image_url" alt="Crop image" class="preview-image">
                      <button type="button" class="btn btn-sm btn-outline-danger remove-image" @click="removeImage">
                        <i class="bi bi-trash"></i>
                        Remove
                      </button>
                    </div>
                    <div v-else class="upload-placeholder mt-3">
                      <i class="bi bi-cloud-upload display-4 text-muted"></i>
                      <p class="text-muted mb-0">Click to upload crop image</p>
                      <small class="text-muted">Supported formats: JPG, PNG, GIF (Max 5MB)</small>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer bg-light border-0">
            <div class="d-flex justify-content-between align-items-center">
              <div class="text-muted">
                <i class="bi bi-info-circle me-2"></i>
                {{ editMode ? 'Update crop information' : 'Add new crop to your collection' }}
              </div>
              <div>
                <button type="button" class="btn btn-secondary me-2" @click="closeModal">
                  <i class="bi bi-x-circle me-2"></i>
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary" :disabled="saving">
                  <i v-if="!saving" class="bi bi-check-circle me-2"></i>
                  <i v-else class="bi bi-arrow-clockwise me-2"></i>
                  {{ editMode ? 'Update Crop' : 'Add Crop' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <div v-if="showDetailsModal" class="modal fade show d-flex align-items-center justify-content-center" style="background-color: rgba(0,0,0,0.6);">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg">
          <div class="modal-header bg-gradient-primary text-white border-0">
            <h5 class="modal-title mb-0">
              <i class="bi bi-flower1 me-2"></i>
              Crop Details
            </h5>
            <button type="button" class="btn-close btn-close-white" @click="closeDetailsModal"></button>
          </div>
          <div class="modal-body p-4" v-if="selectedCrop">
            <div class="row">
              <div class="col-md-8">
                <h4>{{ selectedCrop.name }}</h4>
                <p class="text-muted">{{ selectedCrop.type }}</p>
                <div class="mb-3">
                  <span class="badge me-2" :class="getStatusClass(selectedCrop.status)">{{ selectedCrop.status }}</span>
                </div>
                <p>{{ selectedCrop.description || 'No description available' }}</p>
                <div class="row mt-3">
                  <div class="col-md-6">
                    <small class="text-muted">Planted:</small>
                    <div class="fw-medium">{{ formatDate(selectedCrop.planting_date) }}</div>
                  </div>
                  <div class="col-md-6">
                    <small class="text-muted">Expected Harvest:</small>
                    <div class="fw-medium">{{ formatDate(selectedCrop.expected_harvest_date) }}</div>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div v-if="selectedCrop.image_url" class="text-center">
                  <img :src="selectedCrop.image_url" :alt="selectedCrop.name" class="img-fluid rounded">
                </div>
                <div v-else class="text-center text-muted">
                  <i class="bi bi-image display-4"></i>
                  <p>No image available</p>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer bg-light border-0">
            <button type="button" class="btn btn-secondary" @click="closeDetailsModal">Close</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="successMessage" class="alert alert-success alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3" style="z-index: 1050;">
      {{ successMessage }}
      <button type="button" class="btn-close" @click="successMessage = ''"></button>
    </div>
    <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3" style="z-index: 1050;">
      {{ errorMessage }}
      <button type="button" class="btn-close" @click="errorMessage = ''"></button>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  name: 'CropManagement',
  data() {
    return {
      crops: [],
      filteredCrops: [],
      loading: false,
      searchQuery: '',
      statusFilter: '',
      typeFilter: '',
      viewMode: 'grid',
      showAddModal: false,
      editMode: false,
      editingCrop: null,
      saving: false,
      cropForm: {
        name: '',
        type: '',
        planting_date: '',
        expected_harvest_date: '',
        yield_estimate: '',
        status: 'planted',
        description: '',
        image_url: ''
      },
      successMessage: '',
      errorMessage: ''
    };
  },
  async mounted() {
    await this.loadCrops();
  },
  methods: {
    async loadCrops() {
      this.loading = true;
      try {
        const response = await axios.get('/crops/');
        this.crops = Array.isArray(response.data) ? response.data : [];
        this.filterCrops();
      } catch (error) {
        console.error('Error loading crops:', error);
        this.errorMessage = 'Failed to load crops. Please try again.';
      } finally {
        this.loading = false;
      }
    },

    filterCrops() {
      let filtered = this.crops;

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(crop => 
          crop.name.toLowerCase().includes(query) ||
          crop.type.toLowerCase().includes(query) ||
          crop.description.toLowerCase().includes(query)
        );
      }

      if (this.statusFilter) {
        filtered = filtered.filter(crop => crop.status === this.statusFilter);
      }

      if (this.typeFilter) {
        filtered = filtered.filter(crop => crop.type === this.typeFilter);
      }

      this.filteredCrops = filtered;
    },

    getStatusClass(status) {
      const statusClasses = {
        'planted': 'bg-secondary',
        'growing': 'bg-primary',
        'harvested': 'bg-success'
      };
      return statusClasses[status] || 'bg-secondary';
    },

    formatDate(dateString) {
      if (!dateString) return 'Not set';
      return new Date(dateString).toLocaleDateString();
    },

    editCrop(crop) {
      this.editMode = true;
      this.editingCrop = crop;
      this.cropForm = {
        ...crop,
        planting_date: crop.planting_date ? crop.planting_date.split('T')[0] : '',
        expected_harvest_date: crop.expected_harvest_date ? crop.expected_harvest_date.split('T')[0] : ''
      };
    },

    async saveCrop() {
      if (!this.cropForm.name || !this.cropForm.type || !this.cropForm.planting_date) {
        this.errorMessage = 'Please fill in all required fields';
        return;
      }

      this.saving = true;
      try {
        const formData = new FormData();
        
        Object.keys(this.cropForm).forEach(key => {
          if (key !== 'image_url' && key !== 'farmer') {
            let value = this.cropForm[key];
            // Handle empty values properly
            if (value === '' || value === null || value === undefined) {
              formData.append(key, '');
            } else {
              formData.append(key, value);
            }
          }
        });

        const imageFile = this.$refs.cropImageInput.files[0];
        if (imageFile) {
          formData.append('image', imageFile);
        }

        let response;
        if (this.editMode) {
          response = await axios.patch(`/crops/${this.editingCrop.id}/`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
        } else {
          response = await axios.post('/crops/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
        }

        if (response.data) {
          this.successMessage = this.editMode ? 'Crop updated successfully!' : 'Crop added successfully!';
          setTimeout(() => this.successMessage = '', 3000);
          this.closeModal();
          await this.loadCrops();
        }
      } catch (error) {
        console.error('Error saving crop:', error);
        console.error('Error response:', error.response?.data);
        this.errorMessage = error.response?.data?.detail || error.response?.data?.error || 'Failed to save crop. Please try again.';
      } finally {
        this.saving = false;
      }
    },

    async deleteCrop(crop) {
      if (confirm(`Are you sure you want to delete ${crop.name}? This action cannot be undone.`)) {
        try {
          await axios.delete(`/crops/${crop.id}/`);
          this.successMessage = 'Crop deleted successfully!';
          setTimeout(() => this.successMessage = '', 3000);
          await this.loadCrops();
        } catch (error) {
          console.error('Error deleting crop:', error);
          this.errorMessage = 'Failed to delete crop. Please try again.';
        }
      }
    },

    viewCropDetails(crop) {
      console.log('View details for:', crop);
    },

    closeModal() {
      this.showAddModal = false;
      this.editMode = false;
      this.editingCrop = null;
      this.resetForm();
    },

    resetForm() {
      this.cropForm = {
        name: '',
        type: '',
        planting_date: '',
        expected_harvest_date: '',
        yield_estimate: '',
        status: 'planted',
        description: '',
        image_url: ''
      };
    },

    handleImageUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        this.cropForm.image_url = e.target.result;
      };
      reader.readAsDataURL(file);
    },

    removeImage() {
      this.cropForm.image_url = '';
      this.$refs.cropImageInput.value = '';
    },

    async saveCrop() {
      if (!this.cropForm.name || !this.cropForm.type || !this.cropForm.planting_date) {
        this.errorMessage = 'Please fill in all required fields';
        return;
      }

      this.saving = true;
      try {
        const formData = new FormData();
        
        Object.keys(this.cropForm).forEach(key => {
          if (key !== 'image_url') {
            formData.append(key, this.cropForm[key]);
          }
        });

        const imageFile = this.$refs.cropImageInput.files[0];
        if (imageFile) {
          formData.append('image', imageFile);
        }

        let response;
        if (this.editMode) {
          response = await axios.patch(`/crops/${this.editingCrop.id}/`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
        } else {
          response = await axios.post('/crops/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
        }

        if (response.data) {
          this.successMessage = this.editMode ? 'Crop updated successfully!' : 'Crop added successfully!';
          setTimeout(() => this.successMessage = '', 3000);
          this.closeModal();
          await this.loadCrops();
        }
      } catch (error) {
        console.error('Error saving crop:', error);
        this.errorMessage = error.response?.data?.error || 'Failed to save crop. Please try again.';
      } finally {
        this.saving = false;
      }
    }
  }
};
</script>

<style scoped>
.crop-management {
}

.display-6 {
  font-size: 2.5rem;
  font-weight: 300;
}

/* Crop Cards */
.crop-card {
  transition: all 0.3s ease;
  border-radius: 1rem;
  overflow: hidden;
}

.crop-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.crop-image-container {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.crop-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.crop-image:hover {
  transform: scale(1.05);
}

.crop-image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(45deg, #f8f9fa 0%, #e9ecef 100%);
  color: #6c757d;
}

.crop-status-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0.5rem 0.75rem;
  border-radius: 2rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Crop Details */
.crop-details {
  margin-top: 1rem;
}

.detail-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  padding: 0.5rem 0;
  background: rgba(248, 249, 250, 0.5);
  border-radius: 0.5rem;
  transition: all 0.2s ease;
}

.detail-item:hover {
  background: rgba(233, 236, 239, 0.8);
}

.detail-item i {
  width: 16px;
  height: 16px;
  margin-right: 0.5rem;
}

/* List View */
.crop-list {
  max-width: 100%;
}

.crop-item {
  transition: all 0.3s ease;
  border-radius: 1rem;
}

.crop-item:hover {
  transform: translateX(5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.crop-image-container-small {
  width: 80px;
  height: 80px;
  border-radius: 0.5rem;
  overflow: hidden;
  flex-shrink: 0;
}

.crop-image-small {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.crop-image-placeholder-small {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(45deg, #f8f9fa 0%, #e9ecef 100%);
  color: #6c757d;
  border-radius: 0.5rem;
}

.crop-details-small {
  margin-left: 1rem;
}

.crop-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-group-vertical {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* Modal Enhancements */
.modal-dialog-centered {
  display: flex;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
}

.modal-xl {
  max-width: 800px;
}

.image-upload-area {
  border: 2px dashed #dee2e6;
  border-radius: 0.5rem;
  padding: 2rem;
  text-align: center;
  background: #f8f9fa;
  transition: all 0.3s ease;
}

.image-upload-area:hover {
  border-color: #28a745;
  background: #f1f8f9;
}

.upload-placeholder {
  padding: 2rem;
}

.image-preview {
  max-width: 200px;
  max-height: 200px;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: 10px;
  right: 10px;
}

/* Hover Effects */
.hover-lift {
  transition: all 0.3s ease;
}

.hover-lift:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.hover-scale {
  transition: all 0.2s ease;
}

.hover-scale:hover {
  transform: scale(1.05);
}

/* Status Classes */
.bg-secondary {
  background-color: #6c757d !important;
}

.bg-primary {
  background-color: #0d6efd !important;
}

.bg-success {
  background-color: #198754 !important;
}

/* Transitions */
.transition-all {
  transition: all 0.3s ease;
}

/* Responsive */
@media (max-width: 768px) {
  .modal-dialog-centered {
    padding: 0.5rem;
  }
  
  .modal-xl {
    max-width: 95%;
  }
  
  .crop-image-container {
    height: 150px;
  }
  
  .detail-item {
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
  }
}

@media (max-width: 576px) {
  .hero-section {
    padding: 2rem 1rem;
  }
  
  .display-6 {
    font-size: 2rem;
  }
  
  .crop-card {
    margin-bottom: 1rem;
  }
}

/* Loading States */
.spinner-border {
  border-width: 3px;
}

/* Badge Enhancements */
.badge {
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.5rem 0.75rem;
  border-radius: 2rem;
}

/* Form Enhancements */
.form-control-lg {
  font-size: 1.1rem;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  border: 2px solid #e9ecef;
  transition: all 0.2s ease;
}

.form-control-lg:focus {
  border-color: #28a745;
  box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25);
}

.form-select-lg {
  font-size: 1.1rem;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  border: 2px solid #e9ecef;
}

/* Button Enhancements */
.btn-close-white {
  color: white;
  opacity: 0.8;
  transition: opacity 0.2s ease;
}

.btn-close-white:hover {
  opacity: 1;
}

/* Gradient Backgrounds */
.bg-gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.bg-light {
  background-color: #f8f9fa !important;
}
</style>
