<template>
  <div class="login-wrapper">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-11 col-sm-10 col-md-8 col-lg-6 col-xl-5">
          <div class="card shadow-lg border-0 overflow-hidden">
            <div class="card-header text-white text-center bg-gradient-success p-4 p-md-5">
              <div class="logo-circle mx-auto mb-3">
                <i class="bi bi-patch-check-fill"></i>
              </div>
              <h1 class="fw-bold mb-2 display-5">AgroConnect</h1>
              <p class="subtitle mb-0 lead">Sign in to your dashboard</p>
            </div>
            
            <div class="card-body p-4 p-md-5">
              <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                {{ errorMessage }}
                <button type="button" class="btn-close" @click="errorMessage = ''"></button>
              </div>

              <form @submit.prevent="handleLogin">
                <div class="mb-4">
                  <label for="username" class="form-label fw-semibold text-secondary fs-5">
                    <i class="bi bi-person me-2"></i>Username
                  </label>
                  <div class="input-group input-group-lg">
                    <span class="input-group-text bg-light border-end-0">
                      <i class="bi bi-person text-success"></i>
                    </span>
                    <input 
                      id="username"
                      v-model="username" 
                      type="text" 
                      class="form-control border-start-0" 
                      placeholder="Enter your username" 
                      required 
                      :disabled="loading" 
                    />
                  </div>
                </div>

                <div class="mb-4">
                  <label for="password" class="form-label fw-semibold text-secondary fs-5">
                    <i class="bi bi-lock me-2"></i>Password
                  </label>
                  <div class="input-group input-group-lg">
                    <span class="input-group-text bg-light border-end-0">
                      <i class="bi bi-lock text-success"></i>
                    </span>
                    <input 
                      id="password"
                      v-model="password" 
                      type="password" 
                      class="form-control border-start-0" 
                      placeholder="Enter your password" 
                      required 
                      :disabled="loading" 
                    />
                  </div>
                </div>

                <div class="d-grid gap-3 mt-4">
                  <button 
                    type="submit" 
                    class="btn btn-success btn-lg fw-semibold shadow" 
                    :disabled="loading"
                  >
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                    <span v-else>
                      <i class="bi bi-box-arrow-in-right me-2"></i>Login to Account
                    </span>
                  </button>
                  
                  <div class="text-center">
                    <small class="text-muted">Forgot your password?</small>
                    <a href="#" class="text-decoration-none ms-1">Reset here</a>
                  </div>
                </div>
              </form>

              <div class="text-center mt-4 border-top pt-4">
                <router-link to="/create-profile" class="text-decoration-none">
                  <div class="d-flex align-items-center justify-content-center">
                    <i class="bi bi-person-plus me-2 text-success"></i>
                    <div>
                      <small class="text-muted d-block">New here?</small>
                      <strong class="text-success">Create a Profile</strong>
                    </div>
                  </div>
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
import axios from '../axios';

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
        console.log('🔐 Attempting login with:', this.username);
        const res = await axios.post('/auth/login/', {
          username: this.username,
          password: this.password
        });
        
        console.log('✅ Login response:', res.data);
        console.log('🔑 Access token:', res.data.token);
        console.log('🔑 Refresh token:', res.data.refresh);
        
        // 1. Store the Token
        localStorage.setItem('token', res.data.token);
        console.log('💾 Token stored in localStorage:', localStorage.getItem('token'));
        
        // Store the Role (Crucial for your Router Guard)
        // Ensure your Backend returns 'role' in the token response
        const userRole = res.data.role || 'farmer'; 
        localStorage.setItem('role', userRole.toLowerCase());
        console.log('💾 Role stored:', userRole);
        
        // Reset loading state
        this.loading = false;
        console.log('⏹️ Loading reset');
        
        // Redirect to appropriate dashboard based on role
        const dashboardPath = this.getDashboardByRole(userRole);
        console.log('🚀 Redirecting to:', dashboardPath);
        this.$router.push(dashboardPath);
        
      } catch (err) {
        console.error('❌ Login error:', err);
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
  background: linear-gradient(135deg, #f4f7f5 0%, #e8f5e8 100%);
  display: flex;
  align-items: center;
  padding: 2rem 0;
}

.bg-gradient-success {
  background: linear-gradient(135deg, #198754 0%, #20c997 100%);
}

.logo-circle {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.logo-circle:hover {
  transform: scale(1.05);
  background: rgba(255, 255, 255, 0.3);
}

.card {
  border-radius: 1rem;
  overflow: hidden;
  transition: all 0.3s ease;
  border: none;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.form-control {
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  border: 2px solid #e9ecef;
}

.form-control:focus {
  border-color: #198754;
  box-shadow: 0 0 0 0.2rem rgba(25, 135, 84, 0.25);
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

.btn-success {
  background: linear-gradient(135deg, #198754 0%, #20c997 100%);
  border: none;
  font-weight: 600;
  transition: all 0.3s ease;
  padding: 0.75rem 1.5rem;
}

.btn-success:hover {
  background: linear-gradient(135deg, #157347 0%, #1ea085 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(25, 135, 84, 0.3);
}

.btn-success:disabled {
  opacity: 0.6;
  transform: none;
  box-shadow: none;
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

.form-label {
  margin-bottom: 0.5rem;
  color: #495057;
}

.text-decoration-none {
  transition: all 0.3s ease;
}

.text-decoration-none:hover {
  transform: translateY(-1px);
}

/* Mobile Responsive Enhancements */
@media (max-width: 768px) {
  .login-wrapper {
    padding: 1rem 0;
  }
  
  .logo-circle {
    width: 60px;
    height: 60px;
    font-size: 2rem;
  }
  
  .display-5 {
    font-size: 2rem !important;
  }
  
  .lead {
    font-size: 1rem !important;
  }
  
  .card-body {
    padding: 2rem !important;
  }
}

@media (max-width: 576px) {
  .login-wrapper {
    padding: 0.5rem 0;
  }
  
  .logo-circle {
    width: 50px;
    height: 50px;
    font-size: 1.5rem;
  }
  
  .display-5 {
    font-size: 1.75rem !important;
  }
  
  .card-body {
    padding: 1.5rem !important;
  }
  
  .btn-lg {
    padding: 0.5rem 1rem;
    font-size: 1rem;
  }
}
</style>