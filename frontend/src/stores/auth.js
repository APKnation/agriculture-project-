import { defineStore } from 'pinia'
import axios from '../axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    role: localStorage.getItem('role') || null,
    isAuthenticated: false,
    loading: false,
    error: null
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoggedIn: (state) => !!state.token,
    userRole: (state) => state.role,
    authError: (state) => state.error
  },

  actions: {
    async login(credentials) {
      this.loading = true
      this.error = null
      try {
        console.log('Attempting login to:', axios.defaults.baseURL + 'login/')
        const response = await axios.post('/login/', credentials)
        const { token, user, role } = response.data
        
        this.token = token
        this.user = user
        this.role = role
        this.isAuthenticated = true
        
        localStorage.setItem('token', token)
        localStorage.setItem('role', role)
        
        console.log('Login successful!')
        return { success: true }
      } catch (error) {
        console.error('Login error details:', error)
        
        let errorMessage = 'Login failed'
        if (error.code === 'ECONNABORTED') {
          errorMessage = 'Connection timeout. Please check your internet connection and try again.'
        } else if (error.code === 'ERR_NETWORK') {
          errorMessage = 'Network error. Backend server may be down. Please try again later.'
        } else if (error.response) {
          errorMessage = error.response.data?.error || error.response.data?.message || 'Invalid credentials'
        } else if (error.request) {
          errorMessage = 'No response from server. Please check your connection.'
        }
        
        this.error = errorMessage
        return { success: false, error: errorMessage }
      } finally {
        this.loading = false
      }
    },

    async logout() {
      this.loading = true
      try {
        await axios.post('/logout/')
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.token = null
        this.user = null
        this.role = null
        this.isAuthenticated = false
        this.error = null
        
        localStorage.removeItem('token')
        localStorage.removeItem('role')
        
        this.loading = false
      }
    },

    async fetchUserProfile() {
      if (!this.token) return
      
      this.loading = true
      try {
        const response = await axios.get('/users/me/')
        this.user = response.data
        this.isAuthenticated = true
      } catch (error) {
        this.error = 'Failed to fetch user profile'
        console.error('Profile fetch error:', error)
      } finally {
        this.loading = false
      }
    },

    initializeAuth() {
      if (this.token) {
        this.fetchUserProfile()
      }
    }
  }
})
