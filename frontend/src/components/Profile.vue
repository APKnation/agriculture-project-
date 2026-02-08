<template>
  <div class="profile-dashboard">
    <!-- Header Section -->
    <div class="dashboard-header text-white p-4 mb-4 rounded-3 shadow-lg" style="background: var(--gradient-primary);">
      <div class="container-fluid">
        <div class="row align-items-center">
          <div class="col-md-6">
            <h1 class="mb-0 fw-bold">
              {{ editMode ? 'Edit Profile' : 'My Profile' }}
            </h1>
          </div>
          <div class="col-md-6 text-md-end">
            <div class="user-role-badge">
              <span class="badge bg-white text-primary fs-6">
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
                  <div v-if="!editMode" class="mt-2">
                    <button @click="triggerFileUpload" class="btn btn-sm btn-outline-primary">
                      <i class="bi bi-camera me-1"></i>
                      Change Photo
                    </button>
                    <input ref="fileInput" type="file" @change="handleImageUpload" accept="image/*" style="display: none;">
                  </div>
                </div>

                <!-- User Details -->
                <div v-if="!editMode">
                  <div class="profile-info-item mb-3">
                    <label class="text-muted small">Username</label>
                    <p class="mb-0 fw-semibold">{{ user.username }}</p>
                  </div>
                  <div class="profile-info-item mb-3">
                    <label class="text-muted small">Full Name</label>
                    <p class="mb-0 fw-semibold">{{ user.full_name || 'Not set' }}</p>
                  </div>
                  <div class="profile-info-item mb-3">
                    <label class="text-muted small">Email</label>
                    <p class="mb-0 fw-semibold">{{ user.email || 'Not set' }}</p>
                  </div>
                  <div class="profile-info-item mb-3">
                    <label class="text-muted small">Phone</label>
                    <p class="mb-0 fw-semibold">{{ user.phone_number || 'Not set' }}</p>
                  </div>
                  <div class="profile-info-item mb-3">
                    <label class="text-muted small">Region</label>
                    <p class="mb-0 fw-semibold">{{ user.region || 'Not set' }}</p>
                  </div>
                </div>

                <!-- Edit Form -->
                <form v-else @submit.prevent="updateProfile">
                  <div class="mb-3">
                    <label class="form-label">Full Name</label>
                    <input v-model="editForm.full_name" type="text" class="form-control" required>
                  </div>
                  <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input v-model="editForm.email" type="email" class="form-control" required>
                  </div>
                  <div class="mb-3">
                    <label class="form-label">Phone Number</label>
                    <input v-model="editForm.phone_number" type="tel" class="form-control">
                  </div>
                  <div class="mb-3">
                    <label class="form-label">Region</label>
                    <select v-model="editForm.region" class="form-select">
                      <option value="">Select region</option>
                      <option value="Iringa">Iringa</option>
                      <option value="Dar es Salaam">Dar es Salaam</option>
                      <option value="Mwanza">Mwanza</option>
                      <option value="Arusha">Arusha</option>
                      <option value="Dodoma">Dodoma</option>
                      <option value="Tanga">Tanga</option>
                      <option value="Mbeya">Mbeya</option>
                      <option value="Morogoro">Morogoro</option>
                    </select>
                  </div>
                  <div class="d-grid gap-2">
                    <button type="submit" class="btn btn-primary" :disabled="saving">
                      <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
                      {{ saving ? 'Saving...' : 'Save Changes' }}
                    </button>
                    <button type="button" @click="cancelEdit" class="btn btn-secondary">Cancel</button>
                  </div>
                </form>

                <!-- Action Buttons -->
                <div v-if="!editMode" class="mt-3">
                  <button @click="enableEdit" class="btn btn-primary w-100">
                    <i class="bi bi-pencil me-2"></i>
                    Edit Profile
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Account Settings -->
        <div class="col-lg-8 mb-4">
          <div class="card border-0 shadow-lg h-100">
            <div class="card-header bg-white border-bottom">
              <h5 class="mb-0 text-dark">
                <i class="bi bi-gear me-2"></i>
                Account Settings
              </h5>
            </div>
            <div class="card-body">
              <!-- Password Change -->
              <div class="mb-4">
                <h6 class="mb-3">Change Password</h6>
                <form @submit.prevent="changePassword">
                  <div class="row">
                    <div class="col-md-4 mb-3">
                      <label class="form-label">Current Password</label>
                      <input v-model="passwordForm.current_password" type="password" class="form-control" required>
                    </div>
                    <div class="col-md-4 mb-3">
                      <label class="form-label">New Password</label>
                      <input v-model="passwordForm.new_password" type="password" class="form-control" required>
                    </div>
                    <div class="col-md-4 mb-3">
                      <label class="form-label">Confirm New Password</label>
                      <input v-model="passwordForm.confirm_password" type="password" class="form-control" required>
                    </div>
                  </div>
                  <button type="submit" class="btn btn-warning" :disabled="changingPassword">
                    <span v-if="changingPassword" class="spinner-border spinner-border-sm me-2"></span>
                    {{ changingPassword ? 'Changing...' : 'Change Password' }}
                  </button>
                </form>
              </div>

              <!-- Account Statistics -->
              <div class="mb-4">
                <h6 class="mb-3">Account Statistics</h6>
                <div class="row">
                  <div class="col-md-3 col-6 mb-3">
                    <div class="stat-card text-center p-3 border rounded">
                      <div class="stat-number text-primary fw-bold">{{ userStats.totalCrops || 0 }}</div>
                      <div class="stat-label small text-muted">Total Crops</div>
                    </div>
                  </div>
                  <div class="col-md-3 col-6 mb-3">
                    <div class="stat-card text-center p-3 border rounded">
                      <div class="stat-number text-success fw-bold">{{ userStats.totalPriceRecords || 0 }}</div>
                      <div class="stat-label small text-muted">Price Records</div>
                    </div>
                  </div>
                  <div class="col-md-3 col-6 mb-3">
                    <div class="stat-card text-center p-3 border rounded">
                      <div class="stat-number text-info fw-bold">{{ userStats.notifications || 0 }}</div>
                      <div class="stat-label small text-muted">Notifications</div>
                    </div>
                  </div>
                  <div class="col-md-3 col-6 mb-3">
                    <div class="stat-card text-center p-3 border rounded">
                      <div class="stat-number text-warning fw-bold">{{ userStats.daysActive || 0 }}</div>
                      <div class="stat-label small text-muted">Days Active</div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Danger Zone -->
              <div class="danger-zone">
                <h6 class="mb-3 text-danger">Danger Zone</h6>
                <div class="alert alert-warning">
                  <i class="bi bi-exclamation-triangle me-2"></i>
                  <strong>Warning:</strong> These actions cannot be undone.
                </div>
                <button @click="confirmDeleteAccount" class="btn btn-danger">
                  <i class="bi bi-trash me-2"></i>
                  Delete Account
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Success/Error Messages -->
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
  name: 'Profile',
  data() {
    return {
      user: {},
      loading: false,
      editMode: false,
      saving: false,
      changingPassword: false,
      editForm: {
        full_name: '',
        email: '',
        phone_number: '',
        region: ''
      },
      passwordForm: {
        current_password: '',
        new_password: '',
        confirm_password: ''
      },
      userStats: {
        totalCrops: 0,
        totalPriceRecords: 0,
        notifications: 0,
        daysActive: 0
      },
      successMessage: '',
      errorMessage: ''
    };
  },
  async mounted() {
    await this.loadProfile();
    await this.loadUserStats();
  },
  methods: {
    async loadProfile() {
      this.loading = true;
      try {
        const response = await axios.get('/users/me/');
        this.user = response.data;
        this.initializeEditForm();
      } catch (error) {
        console.error('Error loading profile:', error);
        this.errorMessage = 'Failed to load profile. Please try again.';
      } finally {
        this.loading = false;
      }
    },

    async loadUserStats() {
      try {
        const response = await axios.get('/user-stats/');
        this.userStats = response.data;
      } catch (error) {
        console.error('Error loading user stats:', error);
      }
    },

    initializeEditForm() {
      this.editForm = {
        full_name: this.user.full_name || '',
        email: this.user.email || '',
        phone_number: this.user.phone_number || '',
        region: this.user.region || ''
      };
    },

    enableEdit() {
      this.editMode = true;
      this.initializeEditForm();
    },

    cancelEdit() {
      this.editMode = false;
      this.initializeEditForm();
    },

    async updateProfile() {
      this.saving = true;
      try {
        const response = await axios.patch('/users/me/', this.editForm);
        this.user = { ...this.user, ...response.data };
        this.editMode = false;
        this.successMessage = 'Profile updated successfully!';
        setTimeout(() => this.successMessage = '', 3000);
      } catch (error) {
        console.error('Error updating profile:', error);
        this.errorMessage = error.response?.data?.error || 'Failed to update profile. Please try again.';
      } finally {
        this.saving = false;
      }
    },

    async changePassword() {
      if (this.passwordForm.new_password !== this.passwordForm.confirm_password) {
        this.errorMessage = 'New passwords do not match';
        return;
      }

      if (this.passwordForm.new_password.length < 6) {
        this.errorMessage = 'Password must be at least 6 characters long';
        return;
      }

      this.changingPassword = true;
      try {
        await axios.post('/auth/change-password/', this.passwordForm);
        this.successMessage = 'Password changed successfully!';
        this.passwordForm = {
          current_password: '',
          new_password: '',
          confirm_password: ''
        };
        setTimeout(() => this.successMessage = '', 3000);
      } catch (error) {
        console.error('Error changing password:', error);
        this.errorMessage = error.response?.data?.error || 'Failed to change password. Please try again.';
      } finally {
        this.changingPassword = false;
      }
    },

    triggerFileUpload() {
      this.$refs.fileInput.click();
    },

    async handleImageUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('profile_image', file);

      try {
        const response = await axios.post('/user/upload-profile-image/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        this.user.profile_image_url = response.data.profile_image_url;
        this.successMessage = 'Profile picture updated successfully!';
        setTimeout(() => this.successMessage = '', 3000);
      } catch (error) {
        console.error('Error uploading image:', error);
        this.errorMessage = 'Failed to upload profile picture. Please try again.';
      }
    },

    confirmDeleteAccount() {
      if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
        this.deleteAccount();
      }
    },

    async deleteAccount() {
      try {
        await axios.delete('/users/me/');
        localStorage.clear();
        this.$router.push('/login');
      } catch (error) {
        console.error('Error deleting account:', error);
        this.errorMessage = 'Failed to delete account. Please try again.';
      }
    }
  }
};
</script>

<style scoped>
.profile-dashboard {
  min-height: 100vh;
  background: #f8f9fa;
}

.profile-picture-container {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto;
}

.profile-picture {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.profile-picture-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: #6c757d;
  border: 4px solid #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.profile-info-item label {
  font-weight: 600;
  color: #6c757d;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
}

.stat-card {
  background: #fff;
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-number {
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
}

.danger-zone {
  border-top: 2px solid #dc3545;
  padding-top: 1rem;
  margin-top: 2rem;
}

.alert {
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.btn {
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}
</style>
