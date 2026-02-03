<template>
  <div class="profile-container py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="card profile-card border-0 shadow-lg overflow-hidden">
            
            <div class="profile-header d-flex align-items-end p-4">
              <div class="profile-avatar-wrapper shadow">
                <div class="profile-avatar bg-white d-flex align-items-center justify-content-center">
                  <i class="bi bi-person-fill text-success"></i>
                </div>
              </div>
              <div class="ms-4 mb-2 text-white">
                <h2 class="fw-bold mb-0">{{ user.username }}</h2>
                <span class="badge bg-light text-success text-uppercase">{{ user.role }}</span>
              </div>
            </div>

            <div class="card-body p-4 p-md-5">
              <div class="row g-4 mb-5">
                <div class="col-sm-6">
                  <div class="info-box p-3 rounded-3 border">
                    <small class="text-muted d-block text-uppercase fw-bold">Region</small>
                    <span class="fs-5"><i class="bi bi-geo-alt-fill text-danger me-2"></i>{{ user.region }}</span>
                  </div>
                </div>
                <div class="col-sm-6">
                  <div class="info-box p-3 rounded-3 border">
                    <small class="text-muted d-block text-uppercase fw-bold">Preferred Markets</small>
                    <span class="fs-5"><i class="bi bi-shop text-primary me-2"></i>{{ user.preferred_markets }}</span>
                  </div>
                </div>
              </div>

              <div class="crops-section">
                <h5 class="fw-bold mb-4 d-flex align-items-center">
                  <span class="section-line me-3"></span>
                  My Active Crops
                </h5>
                <div class="row g-3">
                  <div v-for="crop in user.crops" :key="crop.id" class="col-md-6">
                    <div class="crop-pill d-flex align-items-center p-3 rounded-pill border transition-hover">
                      <div class="crop-icon-sm bg-success-subtle text-success me-3">
                        <i class="bi bi-flower2"></i>
                      </div>
                      <span class="fw-medium text-dark">{{ crop.name }}</span>
                      <i class="bi bi-chevron-right ms-auto text-muted"></i>
                    </div>
                  </div>
                  <div v-if="!user.crops || user.crops.length === 0" class="col-12 text-center py-4">
                    <p class="text-muted italic">No crops listed yet.</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="card-footer bg-light border-0 py-3 text-center">
              <button class="btn btn-outline-success btn-sm px-4 rounded-pill me-2">
                <i class="bi bi-pencil-square me-2"></i>Edit Profile
              </button>
              <p class="text-muted mt-3 mb-0" style="font-size: 0.75rem;">
                Last synced: {{ lastUpdated }}
              </p>
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
      user: {
        crops: [] // Initialize to prevent template errors
      },
      lastUpdated: new Date().toLocaleTimeString()
    };
  },
  async mounted() {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/users/1/'); 
      this.user = res.data;
    } catch (error) {
      console.error("Error fetching user:", error);
    }
  }
};
</script>

<style scoped>
/* Main Container */
.profile-container {
  background-color: #f0f4f1;
  min-height: 100vh;
}

/* Header Styling */
.profile-header {
  height: 180px;
  background: linear-gradient(135deg, #198754 0%, #20c997 100%);
  position: relative;
}

/* Avatar Box */
.profile-avatar-wrapper {
  width: 120px;
  height: 120px;
  border-radius: 25px;
  padding: 5px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(5px);
  margin-bottom: -40px;
  z-index: 2;
}

.profile-avatar {
  width: 100%;
  height: 100%;
  border-radius: 20px;
  font-size: 3rem;
}

/* Info Cards */
.info-box {
  background-color: #ffffff;
  transition: all 0.3s ease;
}
.info-box:hover {
  border-color: #198754 !important;
  background-color: #f8fffb;
}

/* Section Title Line */
.section-line {
  display: inline-block;
  width: 40px;
  height: 4px;
  background-color: #198754;
  border-radius: 2px;
}

/* Crop Pills */
.crop-pill {
  background: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
}

.crop-pill:hover {
  transform: translateX(5px);
  background: #f8fffb;
  border-color: #198754 !important;
}

.crop-icon-sm {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Button Styling */
.btn-outline-success {
  border-width: 2px;
  font-weight: 600;
}
</style>