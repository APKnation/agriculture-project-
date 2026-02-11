<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 via-white to-accent-50 flex items-center justify-center p-4">
    <!-- Background Pattern -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-primary-200 rounded-full opacity-20 blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-accent-200 rounded-full opacity-20 blur-3xl"></div>
    </div>

    <!-- Login Container -->
    <div class="relative w-full max-w-md">
      <!-- Logo Section -->
      <div class="text-center mb-8 animate-fade-in">
        <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl shadow-lg mb-4">
          <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">AgriConnect</h1>
        <p class="text-gray-600">Connect with your agricultural community</p>
      </div>

      <!-- Login Card -->
      <div class="card shadow-xl animate-slide-up">
        <div class="card-body p-8">
          <!-- Error Alert -->
          <div v-if="errorMessage" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start animate-slide-down">
            <svg class="w-5 h-5 text-red-500 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <div class="flex-1">
              <p class="text-red-800 font-medium">{{ errorMessage }}</p>
            </div>
            <button @click="errorMessage = ''" class="ml-3 text-red-500 hover:text-red-700">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <!-- Success Alert -->
          <div v-if="successMessage" class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-start animate-slide-down">
            <svg class="w-5 h-5 text-green-500 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <div class="flex-1">
              <p class="text-green-800 font-medium">{{ successMessage }}</p>
            </div>
          </div>

          <!-- Login Form -->
          <form @submit.prevent="handleLogin" class="space-y-6">
            <!-- Username Field -->
            <div>
              <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
                Username
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                </div>
                <input
                  id="username"
                  v-model="username"
                  type="text"
                  required
                  class="input-field pl-10"
                  :class="{ 'border-red-500 focus:ring-red-500': errorMessage && !username }"
                  placeholder="Enter your username"
                />
              </div>
            </div>

            <!-- Password Field -->
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                  </svg>
                </div>
                <input
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  class="input-field pl-10 pr-10"
                  :class="{ 'border-red-500 focus:ring-red-500': errorMessage && !password }"
                  placeholder="Enter your password"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center"
                >
                  <svg v-if="showPassword" class="w-5 h-5 text-gray-400 hover:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                  </svg>
                  <svg v-else class="w-5 h-5 text-gray-400 hover:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"></path>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Remember Me & Forgot Password -->
            <div class="flex items-center justify-between">
              <label class="flex items-center">
                <input type="checkbox" v-model="rememberMe" class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500">
                <span class="ml-2 text-sm text-gray-600">Remember me</span>
              </label>
              <a href="#" class="text-sm text-primary-600 hover:text-primary-700 font-medium">Forgot password?</a>
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              :disabled="loading"
              class="w-full btn-primary relative overflow-hidden group"
            >
              <span class="relative z-10 flex items-center justify-center">
                <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ loading ? 'Signing in...' : 'Sign in' }}
              </span>
              <div class="absolute inset-0 bg-gradient-to-r from-primary-600 to-primary-700 transform translate-y-full group-hover:translate-y-0 transition-transform duration-200"></div>
            </button>
          </form>

          <!-- Divider -->
          <div class="relative my-6">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white text-gray-500">New to AgriConnect?</span>
            </div>
          </div>

          <!-- Register Link -->
          <div class="text-center">
            <router-link
              to="/register"
              class="inline-flex items-center text-primary-600 hover:text-primary-700 font-medium"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM9 15a1 1 0 011-1h6a1 1 0 110 2h-6a1 1 0 01-1-1z"></path>
              </svg>
              Create an account
            </router-link>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="mt-8 text-center text-sm text-gray-500">
        <p>&copy; 2024 AgriConnect. All rights reserved.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      rememberMe: false,
      showPassword: false,
      loading: false,
      errorMessage: '',
      successMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      console.log('🔑 Login button clicked!')
      console.log('👤 Username:', this.username)
      console.log('🔑 Password:', this.password ? '***' : 'empty')
      
      if (!this.username || !this.password) {
        this.errorMessage = 'Please enter both username and password'
        return
      }

      this.loading = true
      this.errorMessage = ''
      this.successMessage = ''
      
      try {
        console.log('🌐 Making API call to login endpoint...')
        
        const response = await this.$axios.post('/login/', {
          username: this.username,
          password: this.password
        })
        
        console.log('📨 API Response:', response)
        console.log('📨 Response data:', response.data)
        console.log('📨 Response status:', response.status)

        if (response.data.token) {
          console.log('🔑 Login successful - Token:', response.data.token)
          console.log('👤 User role:', response.data.role)
          
          // Store authentication data
          localStorage.setItem('token', response.data.token)
          localStorage.setItem('refresh', response.data.refresh)
          localStorage.setItem('role', response.data.role)
          localStorage.setItem('user', JSON.stringify(response.data.user))
          
          if (this.rememberMe) {
            localStorage.setItem('rememberMe', 'true')
          }
          
          console.log('💾 Token stored in localStorage')
          console.log('🔍 Checking stored token:', localStorage.getItem('token'))
          
          this.successMessage = 'Login successful! Redirecting...'
          
          // Redirect to dashboard after a short delay
          setTimeout(() => {
            this.$router.push('/dashboard')
          }, 1000)
        } else {
          console.log('❌ Login failed - No token in response')
          this.errorMessage = response.data.message || 'Login failed'
        }
      } catch (error) {
        console.log('💥 Login error details:', error)
        console.log('💥 Error message:', error.message)
        console.log('💥 Error response:', error.response)
        console.log('💥 Error status:', error.response?.status)
        console.log('💥 Error data:', error.response?.data)
        
        // Show specific error message
        if (error.response?.data?.error) {
          this.errorMessage = error.response.data.error
        } else if (error.response?.data?.detail) {
          this.errorMessage = error.response.data.detail
        } else if (error.message === 'Network Error') {
          this.errorMessage = 'Cannot connect to server. Please check your internet connection.'
        } else {
          this.errorMessage = 'Login failed. Please try again.'
        }
      } finally {
        this.loading = false
        console.log('🏁 Login process completed')
      }
    }
  },
  mounted() {
    // Check if user is already logged in
    const token = localStorage.getItem('token')
    const user = localStorage.getItem('user')
    
    // In development, verify backend is available
    if (import.meta.env.DEV && token && user) {
      // Check if backend is running before auto-login
      this.$axios.get('/health/').then(() => {
        // Backend is running, proceed with auto-login
        this.$router.push('/dashboard')
      }).catch(() => {
        // Backend not running, clear cache and show login
        console.log('🚫 Backend not available, clearing cache')
        localStorage.clear()
      })
    } else if (token && user) {
      // Production or backend assumed available
      this.$router.push('/dashboard')
    }
    
    // Check for remember me
    const remembered = localStorage.getItem('rememberMe')
    if (remembered === 'true') {
      const savedUsername = localStorage.getItem('savedUsername')
      if (savedUsername) {
        this.username = savedUsername
        this.rememberMe = true
      }
    }
  },
  watch: {
    username(newVal) {
      if (this.rememberMe) {
        localStorage.setItem('savedUsername', newVal)
      }
    }
  }
}
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
