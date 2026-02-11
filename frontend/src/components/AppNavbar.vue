<template>
  <nav class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo Section -->
        <div class="flex items-center">
          <router-link to="/" class="flex-shrink-0 flex items-center">
            <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-sm">AC</span>
            </div>
            <span class="ml-3 text-xl font-bold text-gray-900">AgriConnect</span>
          </router-link>
        </div>
        
        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-8">
          <router-link to="/dashboard" class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
            Dashboard
          </router-link>
          <router-link to="/crops" class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
            Crops
          </router-link>
          <router-link to="/marketplace" class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
            Marketplace
          </router-link>
          <router-link to="/weather" class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
            Weather
          </router-link>
          <router-link to="/analytics" class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
            Analytics
          </router-link>
        </div>
        
        <!-- Right Section -->
        <div class="flex items-center space-x-4">
          <!-- Notifications -->
          <button class="relative p-2 text-gray-600 hover:text-gray-900 transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
            </svg>
            <span class="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-400"></span>
          </button>
          
          <!-- User Menu -->
          <div class="relative">
            <button @click="showUserMenu = !showUserMenu" class="flex items-center space-x-3 text-sm rounded-lg p-2 hover:bg-gray-100 transition-colors">
              <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center">
                <span class="text-white font-medium">{{ userInitials }}</span>
              </div>
              <div class="text-left">
                <p class="font-medium text-gray-900">{{ user?.first_name }} {{ user?.last_name }}</p>
                <p class="text-xs text-gray-500 capitalize">{{ user?.role }}</p>
              </div>
              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
              </svg>
            </button>
            
            <!-- Dropdown Menu -->
            <div v-if="showUserMenu" class="absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50">
              <div class="py-1">
                <router-link to="/profile" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors">
                  Profile
                </router-link>
                <router-link to="/settings" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors">
                  Settings
                </router-link>
                <button @click="logout" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors">
                  Sign out
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Mobile menu button -->
        <div class="md:hidden flex items-center">
          <button @click="showMobileMenu = !showMobileMenu" class="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500">
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Mobile menu -->
    <div v-if="showMobileMenu" class="md:hidden">
      <div class="px-2 pt-2 pb-3 space-y-1">
        <router-link to="/dashboard" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 transition-colors">
          Dashboard
        </router-link>
        <router-link to="/crops" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 transition-colors">
          Crops
        </router-link>
        <router-link to="/marketplace" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 transition-colors">
          Marketplace
        </router-link>
        <router-link to="/weather" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 transition-colors">
          Weather
        </router-link>
        <router-link to="/analytics" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 transition-colors">
          Analytics
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AppNavbar',
  data() {
    return {
      showUserMenu: false,
      showMobileMenu: false,
      user: null
    }
  },
  computed: {
    userInitials() {
      if (this.user) {
        return `${this.user.first_name?.[0]}${this.user.last_name?.[0]}`.toUpperCase()
      }
      return 'U'
    }
  },
  methods: {
    async fetchUser() {
      try {
        const token = localStorage.getItem('token')
        if (token) {
          const response = await this.$axios.get('/user/')
          this.user = response.data
        }
      } catch (error) {
        console.error('Error fetching user data:', error)
      }
    },
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  },
  mounted() {
    this.fetchUser()
    // Close menus when clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.relative')) {
        this.showUserMenu = false
        this.showMobileMenu = false
      }
    })
  }
}
</script>
