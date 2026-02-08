import axios from 'axios';
import router from './router';

// Determine API base URL based on environment
const getBaseURL = () => {
  if (import.meta.env.PROD) {
    // Production: Use the deployed backend URL
    return 'https://agriculture-project-9-nvhd.onrender.com/api/';
  } else {
    // Development: Use proxy
    return '/api/';
  }
};

const apiClient = axios.create({
  baseURL: getBaseURL(),
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
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
    console.log('🚨 Axios Error Interceptor:');
    console.log('Status:', error.response?.status);
    console.log('URL:', error.config?.url);
    console.log('Headers sent:', error.config?.headers);
    
    if (error.response && error.response.status === 401) {
      console.log('❌ 401 Unauthorized - Removing token and redirecting');
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
      router.push('/login');
    }
    return Promise.reject(error);
  }
);

export default apiClient;