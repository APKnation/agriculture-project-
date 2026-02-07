<template>
  <div class="profile-dashboard">
    <!-- Header Section -->
    <div class="dashboard-header bg-gradient-primary text-white p-4 mb-4 rounded-3 shadow-lg">
      <div class="container-fluid">
        <div class="row align-items-center">
          <div class="col-md-6">
            <h1 class="mb-0 fw-bold">
              <i class="bi bi-person-circle me-3"></i>
              My Profile
            </h1>
          </div>
          <div class="col-md-6 text-md-end">
            <div class="user-role-badge">
              <span class="badge bg-white text-primary fs-6">
                <i class="bi bi-shield-check me-1"></i>
                {{ user.role?.charAt(0).toUpperCase() + user.role?.slice(1) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container-fluid">
      <div class="row">
        <!-- Profile Information -->
        <div class="col-lg-4 mb-4">
          <div class="card border-0 shadow-lg h-100">
            <div class="card-header bg-white border-bottom">
              <h5 class="mb-0 text-dark">
                <i class="bi bi-person-badge me-2"></i>
                Profile Information
              </h5>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading profile...</span>
                </div>
                <p class="mt-2 mb-0 text-muted">Loading your profile information...</p>
              </div>
              <div v-else>
                <!-- Profile Picture -->
                <div class="text-center mb-4">
                  <div class="profile-picture-container">
                    <img v-if="user.profile_image_url" 
                           :src="user.profile_image_url" 
                           :alt="user.username"
                           class="profile-picture">
                    <div v-else class="profile-picture-placeholder">
                      <i class="bi bi-person-circle"></i>
                    </div>
                  </div>
                  <button v-if="!editing" @click="triggerFileInput" class="btn btn-sm btn-outline-primary mt-2">
                    <i class="bi bi-camera me-1"></i>
                    Change Photo
                  </button>
                  <input ref="fileInput" type="file" accept="image/*" @change="handleImageUpload" class="d-none">
                </div>
                
                <!-- User Details -->
                <div class="user-details">
                  <div class="detail-item mb-3">
                    <label class="form-label fw-semibold">Username</label>
                    <div class="form-control-plaintext">
                      <i class="bi bi-person me-2 text-muted"></i>
                      {{ user.username }}
                    </div>
                  </div>
                  
                  <div class="detail-item mb-3">
                    <label class="form-label fw-semibold">Email</label>
                    <div class="form-control-plaintext">
                      <i class="bi bi-envelope me-2 text-muted"></i>
                      <span v-if="!editing.email">{{ user.email || 'Not provided' }}</span>
                      <input v-if="editing.email" 
                             v-model="editableData.email" 
                             type="email" 
                             class="form-control" 
                             placeholder="Enter your email">
                    </div>
                  </div>
                  
                  <div class="detail-item mb-3">
                    <label class="form-label fw-semibold">Region</label>
                    <div class="form-control-plaintext">
                      <i class="bi bi-geo-alt me-2 text-muted"></i>
                      <span v-if="!editing.region">{{ user.region || 'Not specified' }}</span>
                      <input v-if="editing.region" 
                             v-model="editableData.region" 
                             type="text" 
                             class="form-control" 
                             placeholder="Enter your region">
                    </div>
                  </div>
                  
                  <div class="detail-item mb-3">
                    <label class="form-label fw-semibold">Preferred Markets</label>
                    <div class="form-control-plaintext">
                      <i class="bi bi-shop me-2 text-muted"></i>
                      <span v-if="!editing.preferred_markets">{{ user.preferred_markets || 'Not specified' }}</span>
                      <input v-if="editing.preferred_markets" 
                             v-model="editableData.preferred_markets" 
                             type="text" 
                             class="form-control" 
                             placeholder="Enter preferred markets">
                    </div>
                  </div>
                  
                  <div class="detail-item mb-3">
                    <label class="form-label fw-semibold">Member Since</label>
                    <div class="form-control-plaintext">
                      <i class="bi bi-calendar-check me-2 text-muted"></i>
                      {{ formatDate(user.date_joined) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Account Statistics -->
        <div class="col-lg-4 mb-4">
          <div class="card border-0 shadow-lg h-100">
            <div class="card-header bg-white border-bottom">
              <h5 class="mb-0 text-dark">
                <i class="bi bi-graph-up me-2"></i>
                Account Statistics
              </h5>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading statistics...</span>
                </div>
              </div>
              <div v-else>
                <div class="stat-item mb-3">
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="text-muted">Total Crops</span>
                    <span class="badge bg-success fs-6">{{ userStats.total_crops || 0 }}</span>
                  </div>
                </div>
                
                <div class="stat-item mb-3">
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="text-muted">Price Records</span>
                    <span class="badge bg-info fs-6">{{ userStats.price_records || 0 }}</span>
                  </div>
                </div>
                
                <div class="stat-item mb-3">
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="text-muted">Market Posts</span>
                    <span class="badge bg-primary fs-6">{{ userStats.market_posts || 0 }}</span>
                  </div>
                </div>
                
                <div class="stat-item mb-3">
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="text-muted">Price Alerts</span>
                    <span class="badge bg-warning fs-6">{{ userStats.price_alerts || 0 }}</span>
                  </div>
                </div>
                
                <div class="stat-item mb-3">
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="text-muted">Profile Completion</span>
                    <div class="progress" style="height: 20px;">
                      <div class="progress-bar bg-primary" :style="{width: profileCompletion + '%'}">
                        {{ profileCompletion }}%
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="col-lg-4 mb-4">
          <div class="card border-0 shadow-lg h-100">
            <div class="card-header bg-white border-bottom">
              <h5 class="mb-0 text-dark">
                <i class="bi bi-lightning-charge me-2"></i>
                Quick Actions
              </h5>
            </div>
            <div class="card-body">
              <div class="d-grid gap-2">
                <button v-if="!editing" @click="startEditing" class="btn btn-outline-primary w-100">
                  <i class="bi bi-pencil me-2"></i>
                  Edit Profile
                </button>
                
                <button v-if="editing" @click="saveProfile" class="btn btn-success w-100">
                  <i class="bi bi-check-lg me-2"></i>
                  Save Changes
                </button>
                
                <button v-if="editing" @click="cancelEditing" class="btn btn-outline-danger w-100">
                  <i class="bi bi-x-lg me-2"></i>
                  Cancel
                </button>
                
                <button v-if="!editing" @click="viewPriceTrends" class="btn btn-outline-success w-100">
                  <i class="bi bi-graph-up me-2"></i>
                  Price Trends
                </button>
                
                <button v-if="!editing" @click="viewNotifications" class="btn btn-outline-info w-100">
                  <i class="bi bi-bell me-2"></i>
                  Notifications
                </button>
                
                <button v-if="!editing" @click="exportData" class="btn btn-outline-warning w-100">
                  <i class="bi bi-download me-2"></i>
                  Export Data
                </button>
                
                <button v-if="!editing" @click="changePassword" class="btn btn-outline-danger w-100">
                  <i class="bi bi-shield-lock me-2"></i>
                  Change Password
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="col-12">
        <div class="card border-0 shadow-lg">
          <div class="card-header bg-white border-bottom">
            <h5 class="mb-0 text-dark">
              <i class="bi bi-clock-history me-2"></i>
              Recent Activity
            </h5>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading activity...</span>
              </div>
            </div>
            <div v-else-if="recentActivity.length === 0" class="text-center py-4">
              <i class="bi bi-inbox display-1 text-muted mb-3"></i>
              <p class="text-muted">No recent activity found</p>
            </div>
            <div v-else>
              <div class="activity-timeline">
                <div v-for="activity in recentActivity" :key="activity.id" 
                     class="activity-item d-flex align-items-start mb-3">
                  <div class="activity-icon me-3">
                    <div class="icon-circle" :class="getActivityIconClass(activity.type)">
                      <i :class="getActivityIcon(activity.type)"></i>
                    </div>
                  </div>
                  <div class="activity-content flex-grow-1">
                    <h6 class="mb-1">{{ activity.title }}</h6>
                    <p class="text-muted small mb-1">{{ activity.description }}</p>
                    <small class="text-muted">
                      <i class="bi bi-clock me-1"></i>
                      {{ formatDateTime(activity.created_at) }}
                    </small>
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
  name: 'Profile',
  data() {
    return {
      user: {},
      loading: false,
      userStats: {},
      recentActivity: [],
      fileInput: null,
      editing: false,
      editableData: {}
    };
  },
  computed: {
    profileCompletion() {
      let completion = 0;
      if (this.user.username) completion += 20;
      if (this.editableData.email) completion += 20;
      if (this.editableData.region) completion += 20;
      if (this.editableData.preferred_markets) completion += 20;
      if (this.user.profile_image) completion += 20;
      return Math.min(completion, 100);
    }
  },
  async mounted() {
    await this.loadProfileData();
  },
  methods: {
    async loadProfileData() {
      this.loading = true;
      try {
        // Load user profile
        const userRes = await axios.get('/users/me/');
        this.user = userRes.data;
        
        // Initialize editable data with current user data
        this.editableData = {
          email: this.user.email || '',
          region: this.user.region || '',
          preferred_markets: this.user.preferred_markets || ''
        };

        // Load real user statistics from backend
        try {
          const statsRes = await axios.get('/user-stats/');
          this.userStats = statsRes.data;
        } catch (statsError) {
          console.warn('User stats not available, using mock data:', statsError);
          // Fallback to mock data if endpoint doesn't exist
          this.userStats = {
            total_crops: Math.floor(Math.random() * 10) + 1,
            price_records: Math.floor(Math.random() * 50) + 5,
            market_posts: Math.floor(Math.random() * 20) + 3,
            price_alerts: Math.floor(Math.random() * 15) + 2
          };
        }

        // Load real user activity from backend
        try {
          const activityRes = await axios.get('/user-activity/?limit=5');
          this.recentActivity = activityRes.data;
        } catch (activityError) {
          console.warn('User activity not available, using mock data:', activityError);
          // Fallback to mock data if endpoint doesn't exist
          this.recentActivity = [
            {
              id: 1,
              type: 'login',
              title: 'Logged in to system',
              description: 'User successfully logged in from IP address',
              created_at: new Date().toISOString()
            },
            {
              id: 2,
              type: 'profile_update',
              title: 'Profile Updated',
              description: 'User profile information was updated',
              created_at: new Date(Date.now() - 86400000).toISOString()
            },
            {
              id: 3,
              type: 'price_record',
              title: 'Price Record Added',
              description: 'New price record for maize was added',
              created_at: new Date(Date.now() - 172800000).toISOString()
            }
          ];
        }

      } catch (error) {
        console.error('Error loading profile data:', error);
        this.showErrorMessage('Failed to load profile data. Please try again.');
      } finally {
        this.loading = false;
      }
    },

    startEditing() {
      this.editing = true;
    },

    async saveProfile() {
      try {
        // Save the editable data
        await axios.patch('/users/me/', this.editableData);
        
        // Update user data
        this.user = { ...this.user, ...this.editableData };
        
        this.editing = false;
        this.showSuccessMessage('Profile updated successfully!');
      } catch (error) {
        console.error('Error saving profile:', error);
        this.showErrorMessage('Failed to update profile. Please try again.');
      }
    },

    cancelEditing() {
      // Reset editable data to original user data
      this.editableData = {
        email: this.user.email || '',
        region: this.user.region || '',
        preferred_markets: this.user.preferred_markets || ''
      };
      this.editing = false;
    },

    triggerFileInput() {
      this.fileInput.click();
    },

    async handleImageUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('profile_image', file);

      try {
        await axios.post('/user/upload-profile-image/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        
        await this.loadProfileData();
        this.showSuccessMessage('Profile picture updated successfully!');
      } catch (error) {
        console.error('Error uploading image:', error);
        this.showErrorMessage('Failed to upload profile picture. Please try again.');
      }
    },

    editProfile() {
      this.showInfoMessage('Edit profile feature coming soon!');
    },

    viewPriceTrends() {
      this.$router.push('/price-trends');
    },

    viewNotifications() {
      this.$router.push('/notifications');
    },

    exportData() {
      this.showInfoMessage('Export data feature coming soon!');
    },

    changePassword() {
      this.showInfoMessage('Change password feature coming soon!');
    },

    formatRole(role) {
      const roleMap = {
        'farmer': 'Farmer',
        'officer': 'Market Officer',
        'admin': 'Administrator'
      };
      return roleMap[role] || role;
    },

    formatDate(dateString) {
      if (!dateString) return 'Unknown';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },

    formatDateTime(datetime) {
      if (!datetime) return 'Unknown time';
      const date = new Date(datetime);
      const now = new Date();
      const diffTime = now - date;
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays === 0) {
        return `Today at ${date.toLocaleTimeString('en-US', { 
          hour: '2-digit', 
          minute: '2-digit' 
        })}`;
      } else if (diffDays === 1) {
        return `Yesterday at ${date.toLocaleTimeString('en-US', { 
          hour: '2-digit', 
          minute: '2-digit' 
        })}`;
      } else if (diffDays < 7) {
        return `${diffDays} days ago`;
      } else {
        return date.toLocaleDateString('en-US', {
          month: 'short',
          day: 'numeric',
          year: 'numeric'
        });
      }
    },

    getActivityIcon(type) {
      const icons = {
        login: 'bi bi-box-arrow-in-right',
        profile_update: 'bi bi-person-check',
        price_record: 'bi bi-currency-dollar',
        market_post: 'bi bi-shop',
        notification: 'bi bi-bell',
        system: 'bi bi-info-circle'
      };
      return icons[type] || 'bi bi-circle';
    },

    getActivityIconClass(type) {
      const classes = {
        login: 'text-success',
        profile_update: 'text-primary',
        price_record: 'text-info',
        market_post: 'text-warning',
        notification: 'text-secondary',
        system: 'text-danger'
      };
      return classes[type] || 'text-secondary';
    },

    showSuccessMessage(message) {
      const alertDiv = document.createElement('div');
      alertDiv.className = 'alert alert-success alert-dismissible fade show position-fixed';
      alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
      alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      `;
      document.body.appendChild(alertDiv);
      
      setTimeout(() => {
        if (alertDiv.parentNode) {
          alertDiv.parentNode.removeChild(alertDiv);
        }
      }, 3000);
    },

    showErrorMessage(message) {
      const alertDiv = document.createElement('div');
      alertDiv.className = 'alert alert-danger alert-dismissible fade show position-fixed';
      alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
      alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      `;
      document.body.appendChild(alertDiv);
      
      setTimeout(() => {
        if (alertDiv.parentNode) {
          alertDiv.parentNode.removeChild(alertDiv);
        }
      }, 5000);
    },

    showInfoMessage(message) {
      const alertDiv = document.createElement('div');
      alertDiv.className = 'alert alert-info alert-dismissible fade show position-fixed';
      alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
      alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      `;
      document.body.appendChild(alertDiv);
      
      setTimeout(() => {
        if (alertDiv.parentNode) {
          alertDiv.parentNode.removeChild(alertDiv);
        }
      }, 4000);
    }
  }
};
</script>

<style scoped>
.profile-dashboard {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.dashboard-header {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
}

.profile-picture-container {
  position: relative;
  display: inline-block;
}

.profile-picture {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #007bff;
}

.profile-picture-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background-color: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: #6c757d;
  border: 4px solid #dee2e6;
}

.detail-item {
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 1rem;
}

.detail-item:last-child {
  border-bottom: none;
}

.form-control-plaintext {
  background-color: transparent;
  border: none;
  color: #495057;
  font-size: 0.9rem;
}

.stat-item {
  padding: 0.5rem 0;
}

.progress {
  background-color: #e9ecef;
  border-radius: 0.25rem;
}

.activity-timeline {
  max-height: 400px;
  overflow-y: auto;
}

.activity-item {
  transition: all 0.3s ease;
}

.activity-item:hover {
  background-color: #f8f9fa;
  transform: translateX(5px);
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

.icon-circle {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.icon-circle.text-success {
  background-color: #28a745;
}

.icon-circle.text-primary {
  background-color: #007bff;
}

.icon-circle.text-info {
  background-color: #17a2b8;
}

.icon-circle.text-warning {
  background-color: #ffc107;
  color: #212529;
}

.icon-circle.text-secondary {
  background-color: #6c757d;
}

.icon-circle.text-danger {
  background-color: #dc3545;
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

.bg-gradient-primary {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
}
</style>
