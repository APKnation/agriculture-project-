<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation Header -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0 flex items-center">
              <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
                <span class="text-white font-bold text-sm">AC</span>
              </div>
              <span class="ml-3 text-xl font-bold text-gray-900">AgriConnect</span>
            </div>
          </div>
          
          <div class="flex items-center space-x-4">
            <!-- Notifications -->
            <button class="relative p-2 text-gray-600 hover:text-gray-900">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
              </svg>
              <span class="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-400"></span>
            </button>
            
            <!-- User Menu -->
            <div class="relative">
              <button @click="showUserMenu = !showUserMenu" class="flex items-center space-x-3 text-sm rounded-lg p-2 hover:bg-gray-100">
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
                  <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Profile</a>
                  <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Settings</a>
                  <button @click="logout" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Sign out</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Welcome Section -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Welcome back, {{ user?.first_name }}!</h1>
        <p class="text-gray-600 mt-2">Here's what's happening with your agricultural activities today.</p>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="card p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-primary-100 rounded-lg p-3">
              <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-gray-900">Total Crops</h3>
              <p class="text-2xl font-bold text-primary-600">{{ stats.totalCrops }}</p>
            </div>
          </div>
        </div>

        <div class="card p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-green-100 rounded-lg p-3">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-gray-900">Harvested</h3>
              <p class="text-2xl font-bold text-green-600">{{ stats.harvestedCrops }}</p>
            </div>
          </div>
        </div>

        <div class="card p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-yellow-100 rounded-lg p-3">
              <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-gray-900">Growing</h3>
              <p class="text-2xl font-bold text-yellow-600">{{ stats.growingCrops }}</p>
            </div>
          </div>
        </div>

        <div class="card p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-purple-100 rounded-lg p-3">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c1.11 0 2.08.402 2.599 1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-gray-900">Market Value</h3>
              <p class="text-2xl font-bold text-purple-600">${{ stats.marketValue }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Recent Crops -->
        <div class="card">
          <div class="card-header">
            <h2 class="text-lg font-medium text-gray-900">Recent Crops</h2>
            <router-link to="/crops" class="text-sm text-primary-600 hover:text-primary-700">View all</router-link>
          </div>
          <div class="card-body">
            <div class="space-y-4">
              <div v-for="crop in recentCrops" :key="crop.id" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div class="flex items-center">
                  <div class="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                    <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                    </svg>
                  </div>
                  <div class="ml-3">
                    <p class="font-medium text-gray-900">{{ crop.name }}</p>
                    <p class="text-sm text-gray-500">{{ crop.type }} • {{ crop.status }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <p class="text-sm font-medium text-gray-900">{{ crop.yield_estimate }}kg</p>
                  <p class="text-xs text-gray-500">{{ formatDate(crop.planting_date) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="card">
          <div class="card-header">
            <h2 class="text-lg font-medium text-gray-900">Quick Actions</h2>
          </div>
          <div class="card-body">
            <div class="grid grid-cols-2 gap-4">
              <button class="p-4 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors">
                <svg class="w-8 h-8 text-primary-600 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                </svg>
                <p class="text-sm font-medium text-gray-900">Add Crop</p>
              </button>
              
              <button class="p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
                <svg class="w-8 h-8 text-green-600 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
                <p class="text-sm font-medium text-gray-900">View Market</p>
              </button>
              
              <button class="p-4 bg-yellow-50 rounded-lg hover:bg-yellow-100 transition-colors">
                <svg class="w-8 h-8 text-yellow-600 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path>
                </svg>
                <p class="text-sm font-medium text-gray-900">Weather</p>
              </button>
              
              <button class="p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
                <svg class="w-8 h-8 text-purple-600 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                <p class="text-sm font-medium text-gray-900">Reports</p>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      showUserMenu: false,
      user: null,
      stats: {
        totalCrops: 0,
        harvestedCrops: 0,
        growingCrops: 0,
        marketValue: 0
      },
      recentCrops: []
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
    async fetchDashboardData() {
      try {
        // Fetch user data
        const userResponse = await this.$axios.get('/user/')
        this.user = userResponse.data

        // Fetch crops data
        const cropsResponse = await this.$axios.get('/crops/')
        const crops = cropsResponse.data
        
        this.stats.totalCrops = crops.length
        this.stats.harvestedCrops = crops.filter(c => c.status === 'harvested').length
        this.stats.growingCrops = crops.filter(c => c.status === 'growing').length
        this.stats.marketValue = crops.reduce((sum, crop) => sum + (crop.yield_estimate || 0), 0)
        
        this.recentCrops = crops.slice(0, 5)
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString()
    },
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  },
  mounted() {
    this.fetchDashboardData()
  }
}
</script>
