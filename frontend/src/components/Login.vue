<template>
  <div class="login-wrapper">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-11 col-sm-10 col-md-8 col-lg-6 col-xl-5">
          <div class="card shadow-lg border-0">
            <div class="card-header text-white text-center bg-agro-green">
              <div class="logo-circle mx-auto mb-3">
                <i class="bi bi-patch-check-fill"></i>
              </div>
              <h2 class="fw-bold mb-2">AgroConnect</h2>
              <p class="subtitle mb-0">Sign in to your dashboard</p>
            </div>
            
            <div class="card-body p-4 p-md-5">
              <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                {{ errorMessage }}
                <button type="button" class="btn-close" @click="errorMessage = ''"></button>
              </div>

              <form @submit.prevent="handleLogin">
                <div class="mb-4">
                  <label class="form-label fw-semibold text-secondary">Username</label>
                  <div class="input-group input-group-lg">
                    <span class="input-group-text bg-white"><i class="bi bi-person text-success"></i></span>
                    <input v-model="username" type="text" class="form-control" placeholder="Username" required :disabled="loading" />
                  </div>
                </div>

                <div class="mb-4">
                  <label class="form-label fw-semibold text-secondary">Password</label>
                  <div class="input-group input-group-lg">
                    <span class="input-group-text bg-white"><i class="bi bi-lock text-success"></i></span>
                    <input v-model="password" type="password" class="form-control" placeholder="Password" required :disabled="loading" />
                  </div>
                </div>

                <div class="d-grid mt-4">
                  <button type="submit" class="btn btn-agro btn-lg shadow-sm" :disabled="loading">
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                    <span v-else>Login to Account</span>
                  </button>
                </div>
              </form>

             <div class="text-center mt-4 border-top pt-3">
          <router-link to="/create-profile" class="text-decoration-none">
            <small class="text-muted">
              New here? <strong class="text-success">Create a Profile</strong>
            </small>
          </router-link>
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
  name: 'Login',
  data() {
    return { 
      username: '', 
      password: '',
      loading: false,
      errorMessage: '',
    };
  },
  methods: {
    // Helper to match your router logic
    getDashboardByRole(role) {
      const r = role?.toLowerCase();
      if (r === 'admin') return '/admin-dashboard';
      if (r === 'officer') return '/officer-dashboard';
      return '/farmer-dashboard'; // Default
    },

    async handleLogin() {
      this.errorMessage = '';
      this.loading = true;
      
      try {
        const res = await axios.post('http://127.0.0.1:8000/api/token/', {
          username: this.username,
          password: this.password
        });
        
        // 1. Store the Token
        localStorage.setItem('token', res.data.access);
        
        // 2. Store the Role (Crucial for your Router Guard)
        // Ensure your Backend returns 'role' in the token response
        const userRole = res.data.role || 'farmer'; 
        localStorage.setItem('role', userRole.toLowerCase());
        
        
        this.$router.push('/dashboard');
        
      } catch (err) {
        this.loading = false;
        if (err.response && err.response.status === 401) {
          this.errorMessage = 'Invalid credentials. Please try again.';
        } else {
          this.errorMessage = 'Connection error. Is the backend running?';
        }
      }
    }
  }
};
</script>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  background: #f4f7f5; /* Light grey-green background */
  display: flex;
  align-items: center;
}

.bg-agro-green {
  background: linear-gradient(135deg, #198754 0%, #146c43 100%);
}

.btn-agro {
  background: #198754;
  color: white;
  border: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-agro:hover {
  background: #146c43;
  transform: translateY(-1px);
}

.logo-circle {
  width: 70px;
  height: 70px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.card {
  border-radius: 15px;
}
</style>