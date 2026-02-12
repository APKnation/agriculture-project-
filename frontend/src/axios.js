import axios from 'axios'
import router from './router'

// Use localhost for development, production URL for production
const isDevelopment = import.meta.env.DEV
const baseURL = isDevelopment 
  ? 'http://localhost:8000/api/'
: 'https://apknation.pythonanywhere.com/api/'

const apiClient = axios.create({
  baseURL: baseURL,
  timeout: 60000, // Increased timeout to 60 seconds for Render cold starts
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add JWT token
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle token expiration
apiClient.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = localStorage.getItem('refresh')
      if (refreshToken) {
        try {
          const response = await axios.post('https://apknation.pythonanywhere.com/api/token/refresh/', { refresh: refreshToken })
          const newToken = response.data.access
          localStorage.setItem('token', newToken)
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
          return apiClient(originalRequest)
        } catch (e) {
          console.error('Refresh token failed', e)
          localStorage.clear()
          router.push('/login')
        }
      } else {
        localStorage.clear()
        router.push('/login')
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient