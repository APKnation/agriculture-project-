<template>
  <div class="login-wrapper">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-11 col-sm-10 col-md-8 col-lg-6 col-xl-5">
          <div class="card shadow-lg border-0 overflow-hidden">
            <div class="card-header text-white text-center p-4 p-md-5" style="background: var(--gradient-primary);">
              <div class="logo-circle mx-auto mb-3">
                <span class="logo-text">AM</span>
              </div>
              <h1 class="fw-bold mb-2 display-5">AgroConnect</h1>
              <p class="subtitle mb-0 lead">Sign in to your dashboard</p>
            </div>
            <div class="card-body p-4 p-md-5">
              <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
                <button type="button" class="btn-close" @click="errorMessage = ''"></button>
              </div>

              <form @submit.prevent="handleLogin">
                <div class="mb-4">
                  <label for="username" class="form-label fw-semibold text-secondary fs-5">
                    Username
                  </label>
                  <div class="input-group input-group-lg">
                    <input 
                      id="username"
                      v-model="username" 
                      type="text" 
                      class="form-control" 
                      placeholder="Enter your username" 
                      required 
                      :disabled="loading" 
                    />
                  </div>
                </div>

                <div class="mb-4">
                  <label for="password" class="form-label fw-semibold text-secondary fs-5">
                    Password
                  </label>
                  <div class="input-group input-group-lg">
                    <input 
                      id="password"
                      v-model="password" 
                      type="password" 
                      class="form-control" 
                      placeholder="Enter your password" 
                      required 
                      :disabled="loading" 
                    />
                  </div>
                </div>

                <div class="d-grid gap-3 mt-4">
                  <button 
                    type="submit" 
                    class="btn btn-lg fw-semibold shadow" 
                    style="background: var(--gradient-primary); border: none; color: white;" 
                    :disabled="loading" 
                  >
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                    <span v-else>Login to Account</span>
                  </button>
                </div>
              </form>

              <div class="text-center mt-4 border-top pt-4">
                <p class="mb-0">Don't have an account? <router-link to="/register" class="text-decoration-none">Sign up</router-link></p>
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
      errorMessage: ''
    };
  },
  methods: {
    async handleLogin() {
      console.log('🔑 Login button clicked!');
      console.log('👤 Username:', this.username);
      console.log('🔑 Password:', this.password ? '***' : 'empty');
      
      if (!this.username || !this.password) {
        this.errorMessage = 'Please enter both username and password';
        return;
      }

      this.loading = true;
      try {
        console.log('🌐 Making API call to: /login/');
        const response = await axios.post('/login/', {
          username: this.username,
          password: this.password
        });
        
        console.log('📨 API Response:', response);
        console.log('📨 Response data:', response.data);
        console.log('📨 Response status:', response.status);

        if (response.data.token) {
          console.log('🔑 Login successful - Token:', response.data.token);
          console.log('👤 User role:', response.data.role);
          localStorage.setItem('token', response.data.token);
          localStorage.setItem('role', response.data.role);
          console.log('💾 Token stored in localStorage');
          console.log('🔍 Checking stored token:', localStorage.getItem('token'));
          this.$router.push('/dashboard');
        } else {
          console.log('❌ Login failed - No token in response');
          this.errorMessage = response.data.message || 'Login failed';
        }
      } catch (error) {
        console.log('💥 Login error details:', error);
        console.log('💥 Error message:', error.message);
        console.log('💥 Error response:', error.response);
        console.log('💥 Error status:', error.response?.status);
        console.log('💥 Error data:', error.response?.data);
        
        this.errorMessage = 'Login failed. Please try again.';
        console.error('Login error:', error);
      } finally {
        this.loading = false;
        console.log('🏁 Login process completed');
      }
    }
  }
};
</script>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.card {
  border-radius: 1rem;
  border: none;
}

.logo-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.logo-text {
  font-size: 2rem;
  font-weight: bold;
  color: var(--primary-color);
}

.form-control:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.btn {
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}
</style>
