import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from './axios'
import './assets/css/tailwind.css'

const app = createApp(App)
const pinia = createPinia()

// Register axios globally
app.config.globalProperties.$axios = axios

app.use(pinia)
app.use(router)

app.mount('#app')