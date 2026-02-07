<template>
  <div class="mobile-navigation">
    <!-- Mobile Navigation Toggle -->
    <button class="mobile-nav-toggle d-md-none" @click="toggleMobileMenu">
      <i class="bi bi-list fs-4"></i>
    </button>

    <!-- Mobile Navigation Menu -->
    <div class="mobile-nav-menu" :class="{ active: isMobileMenuOpen }">
      <div class="mobile-nav-header">
        <div class="d-flex justify-content-between align-items-center p-3">
          <h5 class="mb-0">
            <i class="bi bi-tree-fill me-2"></i>
            Smart Agri-Market
          </h5>
          <button class="btn btn-sm btn-outline-secondary" @click="toggleMobileMenu">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
      </div>

      <div class="mobile-nav-body">
        <!-- User Profile Section -->
        <div class="mobile-user-profile p-3 border-bottom">
          <div class="d-flex align-items-center">
            <div class="mobile-avatar me-3">
              <img v-if="user.profile_image_url" 
                   :src="user.profile_image_url" 
                   :alt="user.username"
                   class="rounded-circle"
                   style="width: 40px; height: 40px; object-fit: cover;">
              <div v-else class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center"
                   style="width: 40px; height: 40px;">
                <i class="bi bi-person"></i>
              </div>
            </div>
            <div class="mobile-user-info flex-grow-1">
              <div class="fw-semibold">{{ user.username }}</div>
              <div class="text-muted small">{{ user.role }}</div>
            </div>
          </div>
        </div>

        <!-- Navigation Links -->
        <nav class="mobile-nav-links p-3">
          <div class="nav-section mb-4">
            <h6 class="nav-section-title text-muted small text-uppercase mb-2">Main</h6>
            <div class="nav-items">
              <router-link to="/dashboard" 
                           @click="toggleMobileMenu"
                           class="mobile-nav-link d-flex align-items-center p-2 rounded">
                <i class="bi bi-grid me-3"></i>
                <span>Dashboard</span>
              </router-link>
              <router-link to="/marketplace" 
                           @click="toggleMobileMenu"
                           class="mobile-nav-link d-flex align-items-center p-2 rounded">
                <i class="bi bi-shop me-3"></i>
                <span>Marketplace</span>
              </router-link>
              <router-link to="/price-trends" 
                           @click="toggleMobileMenu"
                           class="mobile-nav-link d-flex align-items-center p-2 rounded">
                <i class="bi bi-graph-up me-3"></i>
                <span>Price Trends</span>
              </router-link>
              <router-link to="/demand" 
                           @click="toggleMobileMenu"
                           class="mobile-nav-link d-flex align-items-center p-2 rounded">
                <i class="bi bi-bar-chart me-3"></i>
                <span>Supply & Demand</span>
              </router-link>
            </div>
          </div>

          <!-- Role-specific links -->
          <div v-if="userRole === 'farmer'" class="nav-section mb-4">
            <h6 class="nav-section-title text-muted small text-uppercase mb-2">Farmer Tools</h6>
            <div class="nav-items">
              <router-link to="/recommendations" 
                           @click="toggleMobileMenu"
                           class="mobile-nav-link d-flex align-items-center p-2 rounded">
                <i class="bi bi-lightbulb me-3"></i>
                <span>Recommendations</span>
              </router-link>
              <router-link to="/weather" 
                           @click="toggleMobileMenu"
                           class="mobile-nav-link d-flex align-items-center p-2 rounded">
                <i class="bi bi-cloud-sun me-3"></i>
                <span>Weather</span>
              </router-link>
            </div>
          </div>

          <div v-if="userRole === 'officer'" class="nav-section mb-4">
            <h6 class="nav-section-title text-muted small text-uppercase mb-2">Officer Tools</h6>
            <div class="nav-items">
              <router-link to="/reports" 
                           @click="toggleMobileMenu"
                           class="mobile-nav-link d-flex align-items-center p-2 rounded">
                <i class="bi bi-file-earmark-text me-3"></i>
                <span>Market Reports</span>
              </router-link>
              <router-link to="/analytics" 
                           @click="toggleMobileMenu"
                           class="mobile-nav-link d-flex align-items-center p-2 rounded">
                <i class="bi bi-graph-up-arrow me-3"></i>
                <span>Analytics</span>
              </router-link>
            </div>
          </div>

          <div v-if="userRole === 'admin'" class="nav-section mb-4">
            <h6 class="nav-section-title text-muted small text-uppercase mb-2">Admin Tools</h6>
            <div class="nav-items">
              <router-link to="/admin-panel" 
                           @click="toggleMobileMenu"
                           class="mobile-nav-link d-flex align-items-center p-2 rounded">
                <i class="bi bi-gear me-3"></i>
                <span>Admin Panel</span>
              </router-link>
            </div>
          </div>

          <!-- Other links -->
          <div class="nav-section mb-4">
            <h6 class="nav-section-title text-muted small text-uppercase mb-2">Account</h6>
            <div class="nav-items">
              <router-link to="/notifications" 
                           @click="toggleMobileMenu"
                           class="mobile-nav-link d-flex align-items-center p-2 rounded">
                <i class="bi bi-bell me-3"></i>
                <span>Notifications</span>
                <span v-if="unreadCount > 0" class="badge bg-warning text-dark ms-auto">
                  {{ unreadCount }}
                </span>
              </router-link>
              <router-link to="/profile" 
                           @click="toggleMobileMenu"
                           class="mobile-nav-link d-flex align-items-center p-2 rounded">
                <i class="bi bi-person me-3"></i>
                <span>Profile</span>
              </router-link>
            </div>
          </div>
        </nav>

        <!-- Logout Button -->
        <div class="mobile-nav-footer p-3 border-top">
          <button @click="handleLogout" class="btn btn-outline-danger w-100">
            <i class="bi bi-box-arrow-right me-2"></i>
            Logout
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Navigation Overlay -->
    <div class="mobile-nav-overlay" 
         :class="{ active: isMobileMenuOpen }"
         @click="toggleMobileMenu"></div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useNotificationsStore } from '../stores/notifications'

export default {
  name: 'MobileNavigation',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const notificationsStore = useNotificationsStore()

    const isMobileMenuOpen = ref(false)
    const isMobile = ref(false)

    const user = computed(() => authStore.currentUser || {})
    const userRole = computed(() => authStore.userRole)
    const unreadCount = computed(() => notificationsStore.unreadCount)

    const toggleMobileMenu = () => {
      isMobileMenuOpen.value = !isMobileMenuOpen.value
      
      // Prevent body scroll when menu is open
      if (isMobileMenuOpen.value) {
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = ''
      }
    }

    const handleLogout = async () => {
      await authStore.logout()
      toggleMobileMenu()
      router.push('/login')
    }

    const checkMobile = () => {
      isMobile.value = window.innerWidth < 768
    }

    const handleResize = () => {
      checkMobile()
      // Close mobile menu if switching to desktop
      if (window.innerWidth >= 768 && isMobileMenuOpen.value) {
        toggleMobileMenu()
      }
    }

    // Close menu on route change
    router.afterEach(() => {
      if (isMobileMenuOpen.value) {
        toggleMobileMenu()
      }
    })

    onMounted(() => {
      checkMobile()
      window.addEventListener('resize', handleResize)
      
      // Initialize notifications count
      if (authStore.isAuthenticated) {
        notificationsStore.fetchNotifications(authStore.currentUser?.id)
      }
    })

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      // Restore body scroll
      document.body.style.overflow = ''
    })

    return {
      isMobileMenuOpen,
      isMobile,
      user,
      userRole,
      unreadCount,
      toggleMobileMenu,
      handleLogout
    }
  }
}
</script>

<style scoped>
.mobile-navigation {
  position: relative;
}

.mobile-nav-toggle {
  background: none;
  border: none;
  color: inherit;
  padding: 0.5rem;
  border-radius: 0.25rem;
  transition: background-color 0.2s ease;
}

.mobile-nav-toggle:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.mobile-nav-menu {
  position: fixed;
  top: 0;
  left: -100%;
  width: 80%;
  max-width: 300px;
  height: 100vh;
  background: white;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1050;
  transition: left 0.3s ease;
  overflow-y: auto;
}

.mobile-nav-menu.active {
  left: 0;
}

.mobile-nav-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1040;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease, visibility 0.3s ease;
}

.mobile-nav-overlay.active {
  opacity: 1;
  visibility: visible;
}

.mobile-nav-header {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
}

.mobile-nav-body {
  flex: 1;
  overflow-y: auto;
}

.mobile-user-profile {
  background-color: #f8f9fa;
}

.mobile-nav-link {
  color: #333;
  text-decoration: none;
  transition: background-color 0.2s ease;
  margin-bottom: 0.25rem;
}

.mobile-nav-link:hover,
.mobile-nav-link.router-link-active {
  background-color: #e9ecef;
  color: #28a745;
}

.mobile-nav-link.router-link-active {
  font-weight: 600;
}

.nav-section-title {
  font-weight: 600;
  letter-spacing: 0.5px;
}

.nav-items {
  display: flex;
  flex-direction: column;
}

.mobile-nav-footer {
  background-color: #f8f9fa;
}

/* Mobile-specific adjustments */
@media (max-width: 480px) {
  .mobile-nav-menu {
    width: 90%;
  }
}

/* Touch-friendly adjustments */
@media (hover: none) and (pointer: coarse) {
  .mobile-nav-link {
    min-height: 44px;
  }
  
  .mobile-nav-toggle {
    min-height: 44px;
    min-width: 44px;
  }
}

/* Animation for menu items */
.mobile-nav-link {
  transform: translateX(0);
  transition: transform 0.2s ease, background-color 0.2s ease;
}

.mobile-nav-link:active {
  transform: translateX(2px);
}

/* Badge styling in mobile menu */
.mobile-nav-link .badge {
  font-size: 0.625rem;
  padding: 0.25rem 0.5rem;
}

/* Smooth scroll for mobile menu body */
.mobile-nav-body {
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

/* Focus states for accessibility */
.mobile-nav-link:focus,
.mobile-nav-toggle:focus {
  outline: 2px solid #28a745;
  outline-offset: 2px;
}

/* Dark mode support (if implemented) */
@media (prefers-color-scheme: dark) {
  .mobile-nav-menu {
    background: #2d3748;
    color: white;
  }
  
  .mobile-nav-link {
    color: white;
  }
  
  .mobile-nav-link:hover,
  .mobile-nav-link.router-link-active {
    background-color: #4a5568;
    color: #48bb78;
  }
  
  .mobile-user-profile,
  .mobile-nav-footer {
    background-color: #4a5568;
  }
  
  .nav-section-title {
    color: #a0aec0;
  }
}
</style>
