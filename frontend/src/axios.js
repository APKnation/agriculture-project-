import axios from 'axios'
import router from './router'

// Always use the deployed backend URL for development and production
const apiClient = axios.create({
  baseURL: 'https://agriculture-project-9-nvhd.onrender.com/api/',
  timeout: 30000, // Increased timeout to 30 seconds
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
          const response = await axios.post('https://agriculture-project-9-nvhd.onrender.com/api/token/refresh/', { refresh: refreshToken })
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