<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 via-white to-accent-50">
    <!-- Hero Section -->
    <div class="relative overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div class="text-center">
          <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Welcome to <span class="text-primary-600">AgriConnect</span>
          </h1>
          <p class="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Connect with your agricultural community, manage crops, track prices, and make informed farming decisions
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <router-link to="/login" class="btn-primary text-lg px-8 py-3">
              Sign In
            </router-link>
            <router-link to="/register" class="btn-secondary text-lg px-8 py-3">
              Create Account
            </router-link>
          </div>
        </div>
      </div>
      
      <!-- Background decoration -->
      <div class="absolute top-0 right-0 -translate-y-12 translate-x-12">
        <div class="w-96 h-96 bg-primary-200 rounded-full opacity-20 blur-3xl"></div>
      </div>
      <div class="absolute bottom-0 left-0 translate-y-12 -translate-x-12">
        <div class="w-96 h-96 bg-accent-200 rounded-full opacity-20 blur-3xl"></div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
      <div class="text-center mb-16">
        <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
          Complete Agricultural Management
        </h2>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          Everything you need to manage your farming operations in one platform
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- Crop Management -->
        <div class="card p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 mb-2">Crop Management</h3>
          <p class="text-gray-600 mb-4">
            Track your crops from planting to harvest. Monitor growth stages, yields, and manage your agricultural inventory.
          </p>
          <router-link to="/crops" class="text-primary-600 hover:text-primary-700 font-medium">
            Explore Crops →
          </router-link>
        </div>

        <!-- Marketplace -->
        <div class="card p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17a1 1 0 001-1v-2a2 2 0 00-2-2H9a2 2 0 00-2 2v2c0 .28.216.5.484.576M7 17h10"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 mb-2">Marketplace</h3>
          <p class="text-gray-600 mb-4">
            Buy and sell agricultural products. Connect with buyers and sellers in your local markets.
          </p>
          <router-link to="/marketplace" class="text-primary-600 hover:text-primary-700 font-medium">
            Visit Marketplace →
          </router-link>
        </div>

        <!-- Price Trends -->
        <div class="card p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 mb-2">Price Trends</h3>
          <p class="text-gray-600 mb-4">
            Track market prices and trends. Get insights on when to sell your crops for the best prices.
          </p>
          <router-link to="/price-trends" class="text-primary-600 hover:text-primary-700 font-medium">
            View Trends →
          </router-link>
        </div>

        <!-- Weather Dashboard -->
        <div class="card p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 mb-2">Weather Dashboard</h3>
          <p class="text-gray-600 mb-4">
            Get real-time weather information and farming recommendations based on current conditions.
          </p>
          <router-link to="/weather" class="text-primary-600 hover:text-primary-700 font-medium">
            Check Weather →
          </router-link>
        </div>

        <!-- Analytics -->
        <div class="card p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 mb-2">Advanced Analytics</h3>
          <p class="text-gray-600 mb-4">
            Comprehensive analytics and reporting. Make data-driven decisions for your farming operations.
          </p>
          <router-link to="/analytics" class="text-primary-600 hover:text-primary-700 font-medium">
            View Analytics →
          </router-link>
        </div>

        <!-- Notifications -->
        <div class="card p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 mb-2">Notifications</h3>
          <p class="text-gray-600 mb-4">
            Stay updated with important alerts, price changes, weather warnings, and market opportunities.
          </p>
          <router-link to="/notifications" class="text-primary-600 hover:text-primary-700 font-medium">
            View Notifications →
          </router-link>
        </div>
      </div>
    </div>

    <!-- User Roles Section -->
    <div class="bg-gray-50 py-24">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Designed for Every Role
          </h2>
          <p class="text-xl text-gray-600 max-w-2xl mx-auto">
            Whether you're a farmer, market officer, or administrator, AgriConnect has tools for you
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Farmer -->
          <div class="text-center">
            <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">Farmers</h3>
            <p class="text-gray-600">
              Manage crops, track prices, get weather insights, and connect with markets
            </p>
          </div>

          <!-- Market Officer -->
          <div class="text-center">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">Market Officers</h3>
            <p class="text-gray-600">
              Monitor markets, analyze trends, manage pricing, and provide market insights
            </p>
          </div>

          <!-- Admin -->
          <div class="text-center">
            <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">Administrators</h3>
            <p class="text-gray-600">
              Manage users, oversee operations, access analytics, and maintain system health
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
      <div class="text-center">
        <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
          Ready to Transform Your Farming Experience?
        </h2>
        <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Join thousands of farmers and agricultural professionals using AgriConnect
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link to="/register" class="btn-primary text-lg px-8 py-3">
            Get Started Free
          </router-link>
          <router-link to="/login" class="btn-secondary text-lg px-8 py-3">
            Sign In to Your Account
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LandingPage'
}
</script>
