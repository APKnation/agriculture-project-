<template>
  <div id="app">
    <!-- Mobile Navigation -->
    <MobileNavigation />

    <!-- Desktop Navbar -->
    <nav v-if="showNavbar" class="navbar navbar-expand-lg navbar-dark shadow-lg d-none d-lg-block" style="background: var(--gradient-primary);">
      <div class="container">
        <router-link to="/dashboard" class="navbar-brand fw-bold fs-4 text-white">
          Smart Agri-Market
        </router-link>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <!-- Common Links -->
            <li class="nav-item">
              <router-link to="/dashboard" class="nav-link text-white">
                Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/marketplace" class="nav-link text-white">
                Marketplace
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/price-trends" class="nav-link text-white">
                Price Trends
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/demand" class="nav-link text-white">
                Supply & Demand
              </router-link>
            </li>

            <!-- Role-based Links -->
            <li v-if="userRole === 'farmer'" class="nav-item dropdown">
              <a class="nav-link dropdown-toggle text-white" href="#" role="button" data-bs-toggle="dropdown">
                Farming Tools
              </a>
              <ul class="dropdown-menu dropdown-menu-dark">
                <li><router-link class="dropdown-item" to="/recommendations">
                  Recommendations
                </router-link></li>
                <li><router-link class="dropdown-item" to="/weather">
                  Weather
                </router-link></li>
              </ul>
            </li>
            <li v-if="userRole === 'officer'" class="nav-item dropdown">
              <a class="nav-link dropdown-toggle text-white" href="#" role="button" data-bs-toggle="dropdown">
                Analytics
              </a>
              <ul class="dropdown-menu dropdown-menu-dark">
                <li><router-link class="dropdown-item" to="/reports">
                  Market Reports
                </router-link></li>
                <li><router-link class="dropdown-item" to="/analytics">
                  Advanced Analytics
                </router-link></li>
              </ul>
            </li>
            <li v-if="userRole === 'admin'" class="nav-item">
              <router-link to="/admin-panel" class="nav-link text-white">
                Admin Panel
              </router-link>
            </li>

            <!-- Notifications & Profile -->
            <li class="nav-item">
              <router-link to="/notifications" class="nav-link position-relative text-white">
                Notifications
                <span v-if="unreadCount > 0" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                  {{ unreadCount }}
                </span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/profile" class="nav-link text-white">
                My Profile
              </router-link>
            </li>

            <!-- Logout -->
            <li class="nav-item">
              <button @click="logout" class="btn btn-sm btn-outline-light ms-2">
                Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
      <div class="container-fluid py-4">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'
import { useNotificationsStore } from './stores/notifications'
import MobileNavigation from './components/MobileNavigation.vue'

export default {
  name: "App",
  components: {
    MobileNavigation
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const notificationsStore = useNotificationsStore()

    const userRole = computed(() => authStore.userRole)
    const unreadCount = computed(() => notificationsStore.unreadCount)

    const showNavbar = computed(() => {
      return router.currentRoute.value.path !== "/login"
    })

    const logout = async () => {
      await authStore.logout()
      router.push("/login")
    }

    onMounted(() => {
      // Initialize auth state
      authStore.initializeAuth()
      
      // Initialize notifications if authenticated
      if (authStore.isAuthenticated) {
        notificationsStore.fetchNotifications(authStore.currentUser?.id)
      }
    })

    return {
      userRole,
      unreadCount,
      showNavbar,
      logout
    }
  }
};
</script>

<style>
#app { 
  min-height: 100vh; 
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

body { 
  margin: 0; 
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
}

.main-content {
  min-height: calc(100vh - 76px); /* Subtract navbar height */
  padding-top: 1rem;
}

/* Enhanced Navbar Styling */
.navbar {
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.bg-gradient-success {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
}

.navbar-brand {
  transition: all 0.3s ease;
}

.navbar-brand:hover {
  transform: scale(1.05);
  color: #fff !important;
}

.nav-link { 
  transition: all 0.3s ease; 
  cursor: pointer; 
  padding: 0.5rem 1rem !important;
  border-radius: 0.375rem;
  margin: 0 0.25rem;
  position: relative;
}

.nav-link:hover { 
  transform: translateY(-2px); 
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff !important;
}

.router-link-active { 
  font-weight: 600; 
  background-color: rgba(255, 255, 255, 0.15);
  color: #fff !important;
}

/* Dropdown Menu Styling */
.dropdown-menu {
  border: none;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-radius: 0.5rem;
  margin-top: 0.5rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

.dropdown-item {
  transition: all 0.3s ease;
  padding: 0.75rem 1.5rem;
  border-radius: 0.25rem;
  margin: 0.125rem 0;
}

.dropdown-item:hover {
  background-color: #28a745;
  color: #fff;
  transform: translateX(4px);
}

.dropdown-item.router-link-active {
  background-color: #20c997;
  color: #fff;
}

/* Badge Styling */
.badge {
  font-size: 0.7rem;
  padding: 0.25rem 0.5rem;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

/* Button Styling */
.btn {
  transition: all 0.3s ease;
  border-radius: 0.375rem;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Mobile Responsive Enhancements */
@media (max-width: 991.98px) {
  .main-content {
    min-height: calc(100vh - 60px);
    padding-top: 0.5rem;
  }
}

@media (max-width: 768px) {
  .navbar-brand {
    font-size: 1.25rem !important;
  }
  
  .nav-link {
    padding: 0.75rem 1rem !important;
    margin: 0.125rem 0;
  }
  
  .btn-sm {
    padding: 0.375rem 0.75rem;
    font-size: 0.875rem;
  }
}

@media (max-width: 576px) {
  .main-content {
    padding-top: 0.25rem;
  }
  
  .container-fluid {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
