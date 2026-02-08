<template>
  <div class="register-wrapper">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-11 col-sm-10 col-md-8 col-lg-6 col-xl-5">
          <div class="card shadow-lg border-0 overflow-hidden">
            <div class="card-header text-white text-center p-4 p-md-5" style="background: var(--gradient-primary);">
              <div class="logo-circle mx-auto mb-3">
                <span class="logo-text">AM</span>
              </div>
              <h1 class="fw-bold mb-2 display-5">AgroConnect</h1>
              <p class="subtitle mb-0 lead">Create your account</p>
            </div>
            <div class="card-body p-4 p-md-5">
              <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
                {{ errorMessage }}
                <button type="button" class="btn-close" @click="errorMessage = ''"></button>
              </div>

              <form @submit.prevent="handleRegister">
                <!-- User Information -->
                <div class="mb-4">
                  <label class="form-label fw-semibold text-secondary fs-5">Full Name</label>
                  <div class="input-group input-group-lg">
                    <input 
                      v-model="fullName" 
                      type="text" 
                      class="form-control" 
                      placeholder="Enter your full name" 
                      required 
                      :disabled="loading" 
                    />
                  </div>
                </div>

                <div class="mb-4">
                  <label class="form-label fw-semibold text-secondary fs-5">Username</label>
                  <div class="input-group input-group-lg">
                    <input 
                      v-model="username" 
                      type="text" 
                      class="form-control" 
                      placeholder="Choose a username" 
                      required 
                      :disabled="loading" 
                    />
                  </div>
                </div>

                <div class="mb-4">
                  <label class="form-label fw-semibold text-secondary fs-5">Email</label>
                  <div class="input-group input-group-lg">
                    <input 
                      v-model="email" 
                      type="email" 
                      class="form-control" 
                      placeholder="Enter your email" 
                      required 
                      :disabled="loading" 
                    />
                  </div>
                </div>

                <div class="mb-4">
                  <label class="form-label fw-semibold text-secondary fs-5">Phone Number</label>
                  <div class="input-group input-group-lg">
                    <input 
                      v-model="phoneNumber" 
                      type="tel" 
                      class="form-control" 
                      placeholder="Enter your phone number" 
                      required 
                      :disabled="loading" 
                    />
                  </div>
                </div>

                <div class="mb-4">
                  <label class="form-label fw-semibold text-secondary fs-5">Region</label>
                  <div class="input-group input-group-lg">
                    <select 
                      v-model="region" 
                      class="form-select" 
                      required 
                      :disabled="loading" 
                    >
                      <option value="">Select your region</option>
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
                </div>

                <!-- Role Selection -->
                <div class="mb-4">
                  <label class="form-label fw-semibold text-secondary fs-5">Account Type</label>
                  <div class="input-group input-group-lg">
                    <select 
                      v-model="role" 
                      class="form-select" 
                      required 
                      :disabled="loading" 
                    >
                      <option value="">Select account type</option>
                      <option value="farmer">Farmer</option>
                      <option value="officer">Agricultural Officer</option>
                      <option value="admin">Administrator</option>
                    </select>
                  </div>
                </div>

                <!-- Password Fields -->
                <div class="mb-4">
                  <label class="form-label fw-semibold text-secondary fs-5">Password</label>
                  <div class="input-group input-group-lg">
                    <input 
                      v-model="password" 
                      type="password" 
                      class="form-control" 
                      placeholder="Create a password" 
                      required 
                      :disabled="loading" 
                    />
                  </div>
                </div>

                <div class="mb-4">
                  <label class="form-label fw-semibold text-secondary fs-5">Confirm Password</label>
                  <div class="input-group input-group-lg">
                    <input 
                      v-model="confirmPassword" 
                      type="password" 
                      class="form-control" 
                      placeholder="Confirm your password" 
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
                    <span v-else>Create Account</span>
                  </button>
                </div>
              </form>

              <div class="text-center mt-4 border-top pt-4">
                <p class="mb-0">Already have an account? <router-link to="/login" class="text-decoration-none">Sign in</router-link></p>
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
  name: 'Register',
  data() {
    return {
      fullName: '',
      username: '',
      email: '',
      phoneNumber: '',
      region: '',
      role: '',
      password: '',
      confirmPassword: '',
      loading: false,
      errorMessage: ''
    };
  },
  methods: {
    async handleRegister() {
      // Validation
      if (!this.fullName || !this.username || !this.email || !this.phoneNumber || !this.region || !this.role) {
        this.errorMessage = 'Please fill in all required fields';
        return;
      }

      if (this.password !== this.confirmPassword) {
        this.errorMessage = 'Passwords do not match';
        return;
      }

      if (this.password.length < 6) {
        this.errorMessage = 'Password must be at least 6 characters long';
        return;
      }

      this.loading = true;
      try {
        const response = await axios.post('/auth/register/', {
          username: this.username,
          email: this.email,
          full_name: this.fullName,
          phone_number: this.phoneNumber,
          region: this.region,
          role: this.role,
          password: this.password
        });

        if (response.data.token) {
          console.log('🎉 Registration successful - Token:', response.data.token);
          console.log('👤 User role:', response.data.role);
          
          localStorage.setItem('token', response.data.token);
          localStorage.setItem('role', response.data.role);
          localStorage.setItem('user', JSON.stringify(response.data.user));
          
          this.$router.push('/dashboard');
        } else {
          this.errorMessage = response.data.message || 'Registration failed';
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.error || 'Registration failed. Please try again.';
        console.error('Registration error:', error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.register-wrapper {
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
