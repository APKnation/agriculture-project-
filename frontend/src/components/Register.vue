<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 via-white to-accent-50 flex items-center justify-center p-4">
    <div class="relative w-full max-w-2xl">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Join AgriConnect</h1>
        <p class="text-gray-600">Create your account and start connecting</p>
      </div>

      <div class="card shadow-xl">
        <div class="card-body p-8">
          <div v-if="errorMessage" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-red-800">{{ errorMessage }}</p>
          </div>

          <div v-if="successMessage" class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <p class="text-green-800">{{ successMessage }}</p>
          </div>

          <form @submit.prevent="handleRegister" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Username *</label>
                <input v-model="formData.username" type="text" required class="input-field" placeholder="Choose a username">
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Email *</label>
                <input v-model="formData.email" type="email" required class="input-field" placeholder="your@email.com">
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">First Name *</label>
                <input v-model="formData.firstName" type="text" required class="input-field" placeholder="John">
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Last Name *</label>
                <input v-model="formData.lastName" type="text" required class="input-field" placeholder="Doe">
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Password *</label>
                <input v-model="formData.password" type="password" required class="input-field" placeholder="Create a strong password">
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Confirm Password *</label>
                <input v-model="formData.confirmPassword" type="password" required class="input-field" placeholder="Confirm your password">
                <p v-if="formData.confirmPassword && formData.password !== formData.confirmPassword" class="mt-2 text-sm text-red-600">
                  Passwords do not match
                </p>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">I am a *</label>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <label class="relative">
                  <input type="radio" v-model="formData.role" value="farmer" class="peer sr-only" required>
                  <div class="p-4 border-2 rounded-lg cursor-pointer transition-all peer-checked:border-primary-500 peer-checked:bg-primary-50 hover:border-gray-300">
                    <div class="text-center">
                      <h3 class="font-medium">Farmer</h3>
                      <p class="text-sm text-gray-500">Grow and sell crops</p>
                    </div>
                  </div>
                </label>

                <label class="relative">
                  <input type="radio" v-model="formData.role" value="officer" class="peer sr-only">
                  <div class="p-4 border-2 rounded-lg cursor-pointer transition-all peer-checked:border-primary-500 peer-checked:bg-primary-50 hover:border-gray-300">
                    <div class="text-center">
                      <h3 class="font-medium">Market Officer</h3>
                      <p class="text-sm text-gray-500">Manage markets</p>
                    </div>
                  </div>
                </label>

                <label class="relative">
                  <input type="radio" v-model="formData.role" value="admin" class="peer sr-only">
                  <div class="p-4 border-2 rounded-lg cursor-pointer transition-all peer-checked:border-primary-500 peer-checked:bg-primary-50 hover:border-gray-300">
                    <div class="text-center">
                      <h3 class="font-medium">Admin</h3>
                      <p class="text-sm text-gray-500">System administrator</p>
                    </div>
                  </div>
                </label>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Region</label>
              <select v-model="formData.region" class="input-field">
                <option value="">Select your region</option>
                <option value="iringa">Iringa</option>
                <option value="dar-es-salaam">Dar es Salaam</option>
                <option value="arusha">Arusha</option>
                <option value="mbeya">Mbeya</option>
                <option value="dodoma">Dodoma</option>
                <option value="mwanza">Mwanza</option>
                <option value="tanga">Tanga</option>
                <option value="morogoro">Morogoro</option>
              </select>
            </div>

            <div>
              <label class="flex items-start">
                <input type="checkbox" v-model="formData.agreeTerms" class="w-4 h-4 text-primary-600 border-gray-300 rounded mt-1">
                <span class="ml-2 text-sm text-gray-600">
                  I agree to the Terms and Conditions and Privacy Policy
                </span>
              </label>
            </div>

            <button type="submit" :disabled="loading || !isFormValid" class="w-full btn-primary">
              <span v-if="loading" class="flex items-center justify-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Creating Account...
              </span>
              <span v-else>Create Account</span>
            </button>
          </form>

          <div class="text-center mt-6 border-t pt-6">
            <p class="text-gray-600">
              Already have an account? 
              <router-link to="/login" class="text-primary-600 hover:text-primary-700 font-medium">
                Sign in
              </router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      loading: false,
      errorMessage: '',
      successMessage: '',
      formData: {
        username: '',
        email: '',
        firstName: '',
        lastName: '',
        password: '',
        confirmPassword: '',
        role: '',
        region: '',
        agreeTerms: false
      }
    }
  },
  computed: {
    isFormValid() {
      return this.formData.username && 
             this.formData.email && 
             this.formData.firstName && 
             this.formData.lastName && 
             this.formData.password && 
             this.formData.confirmPassword && 
             this.formData.password === this.formData.confirmPassword && 
             this.formData.role && 
             this.formData.agreeTerms
    }
  },
  methods: {
    async handleRegister() {
      if (!this.isFormValid) {
        this.errorMessage = 'Please fill in all required fields and agree to the terms'
        return
      }

      this.loading = true
      this.errorMessage = ''
      this.successMessage = ''
      
      try {
        console.log('📝 Registering new user...')
        
        const response = await this.$axios.post('/register/', {
          username: this.formData.username,
          email: this.formData.email,
          first_name: this.formData.firstName,
          last_name: this.formData.lastName,
          password: this.formData.password,
          role: this.formData.role,
          region: this.formData.region
        })
        
        console.log('📨 Registration Response:', response)
        
        if (response.data.id) {
          this.successMessage = 'Account created successfully! Redirecting to login...'
          
          setTimeout(() => {
            this.$router.push('/login')
          }, 2000)
        } else {
          this.errorMessage = 'Registration failed. Please try again.'
        }
      } catch (error) {
        console.log('💥 Registration error:', error)
        
        if (error.response?.data) {
          const errors = error.response.data
          if (typeof errors === 'object') {
            const errorMessages = Object.entries(errors).map(([field, messages]) => {
              return `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`
            })
            this.errorMessage = errorMessages.join('; ')
          } else {
            this.errorMessage = errors.detail || errors.error || 'Registration failed'
          }
        } else {
          this.errorMessage = 'Registration failed. Please try again.'
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
