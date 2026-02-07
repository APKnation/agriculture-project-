import axios from 'axios';
import router from './router';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add token to every request
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    console.log('🔧 Axios interceptor - Token:', token ? 'Present' : 'Missing');
    console.log('🔧 Axios interceptor - URL:', config.url);
    console.log('🔧 Axios interceptor - Method:', config.method);
    console.log('🔧 Axios interceptor - Headers before:', JSON.stringify(config.headers));
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('🔧 Axios interceptor - Header added:', config.headers.Authorization);
    }
    console.log('🔧 Axios interceptor - Final headers:', JSON.stringify(config.headers));
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle 401 errors (token expired)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
      router.push('/login');
    }
    return Promise.reject(error);
  }
);

export default apiClient;