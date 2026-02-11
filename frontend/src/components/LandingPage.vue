<template>
  <div class="min-h-screen bg-gradient-secondary overflow-hidden">
    <!-- Hero Section with Modern Design -->
    <div class="relative">
      <!-- Animated Background Elements -->
      <div class="absolute inset-0 overflow-hidden">
        <div class="absolute -top-40 -right-40 w-96 h-96 bg-gradient-to-br from-primary-400 to-accent-500 rounded-full opacity-20 blur-3xl animate-float"></div>
        <div class="absolute -bottom-40 -left-40 w-96 h-96 bg-gradient-to-br from-modern-purple-400 to-modern-blue-500 rounded-full opacity-20 blur-3xl animate-float" style="animation-delay: 2s;"></div>
        <div class="absolute top-1/2 left-1/4 w-64 h-64 bg-gradient-to-br from-modern-emerald-400 to-modern-blue-500 rounded-full opacity-10 blur-2xl animate-pulse-slow"></div>
      </div>

      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div class="text-center">
          <h1 class="text-5xl md:text-7xl font-bold text-modern-slate-900 mb-8 animate-scale-in">
            Welcome to <span class="text-gradient bg-clip-text">AgriConnect</span>
          </h1>
          <p class="text-xl md:text-2xl text-modern-slate-600 mb-12 max-w-4xl mx-auto leading-relaxed animate-slide-up" style="animation-delay: 0.2s;">
            Connect with your agricultural community, manage crops, track prices, and make informed farming decisions with cutting-edge technology
          </p>
          <div class="flex flex-col sm:flex-row gap-6 justify-center animate-slide-up" style="animation-delay: 0.4s;">
            <router-link to="/login" class="btn-primary text-lg px-8 py-4 shadow-glow">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h18m-4-8a2 2 0 00-2-2H6a2 2 0 00-2 2v8a2 2 0 002 2h10a2 2 0 002-2V6a2 2 0 00-2-2z"></path>
              </svg>
              Sign In
            </router-link>
            <router-link to="/register" class="btn-outline text-lg px-8 py-4">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v-3m0 3h3m-3 0h-3m2-2h-4a2 2 0 00-2-2v-4a2 2 0 012-2h4a2 2 0 012 2v4m-6 9l6 6m-6-6V6a2 2 0 012-2h4a2 2 0 012 2v12"></path>
              </svg>
              Create Account
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section with Modern Cards -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
      <div class="text-center mb-20">
        <h2 class="text-4xl md:text-5xl font-bold text-modern-slate-900 mb-6 animate-scale-in" style="animation-delay: 0.6s;">
          Advanced Agricultural Platform
        </h2>
        <p class="text-xl text-modern-slate-600 max-w-3xl mx-auto leading-relaxed animate-slide-up" style="animation-delay: 0.8s;">
          Cutting-edge technology meets traditional farming for maximum productivity and sustainability
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
        <!-- Crop Management Card -->
        <div class="card group hover:shadow-xl transform transition-all duration-500 animate-slide-up" style="animation-delay: 1s;">
          <div class="p-8">
            <div class="flex items-center mb-6">
              <div class="w-16 h-16 bg-gradient-to-br from-modern-emerald-400 to-modern-emerald-600 rounded-2xl flex items-center justify-center shadow-glow group-hover:scale-110 transition-transform duration-300">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-2xl font-bold text-modern-slate-900 mb-2">Crop Management</h3>
                <p class="text-modern-slate-600">Smart farming solutions</p>
              </div>
            </div>
            <p class="text-modern-slate-600 leading-relaxed mb-6">
              Track your crops from planting to harvest. Monitor growth stages, yields, and manage your agricultural inventory with AI-powered insights.
            </p>
            <router-link to="/crops" class="inline-flex items-center text-modern-emerald-600 hover:text-modern-emerald-700 font-semibold group-hover:text-modern-emerald-800 transition-colors duration-300">
              Explore Crops
              <svg class="w-5 h-5 ml-2 transform group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4-4m4 4v10l-4 4m-6-0a2 2 0 00-2-2H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2V6a2 2 0 00-2-2z"></path>
              </svg>
            </router-link>
          </div>
        </div>

        <!-- Marketplace Card -->
        <div class="card group hover:shadow-glow transform transition-all duration-500 animate-slide-up" style="animation-delay: 1.2s;">
          <div class="p-8">
            <div class="flex items-center mb-6">
              <div class="w-16 h-16 bg-gradient-to-br from-modern-blue-400 to-modern-blue-600 rounded-2xl flex items-center justify-center shadow-glow group-hover:scale-110 transition-transform duration-300">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707L7 13m0 0l2.293 2.293c.63.63.184 1.707.707L7 13m-6 0a1 1 0 001-1v-2a2 2 0 00-2-2H5a2 2 0 00-2 2v2a1 1 0 001 1h2m-6 0a1 1 0 001-1v-2a2 2 0 00-2-2H5a2 2 0 00-2 2v2a1 1 0 001 1h2"></path>
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-2xl font-bold text-modern-slate-900 mb-2">Marketplace</h3>
                <p class="text-modern-slate-600">Digital trading hub</p>
              </div>
            </div>
            <p class="text-modern-slate-600 leading-relaxed mb-6">
              Connect with buyers and sellers in real-time. Access global markets, compare prices, and maximize your profits with intelligent trading tools.
            </p>
            <router-link to="/marketplace" class="inline-flex items-center text-modern-blue-600 hover:text-modern-blue-700 font-semibold group-hover:text-modern-blue-800 transition-colors duration-300">
              Visit Marketplace
              <svg class="w-5 h-5 ml-2 transform group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4-4m4 4v10l-4 4m-6-0a2 2 0 00-2-2H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2V6a2 2 0 00-2-2z"></path>
              </svg>
            </router-link>
          </div>
        </div>

        <!-- Price Trends Card -->
        <div class="card group hover:shadow-glow transform transition-all duration-500 animate-slide-up" style="animation-delay: 1.4s;">
          <div class="p-8">
            <div class="flex items-center mb-6">
              <div class="w-16 h-16 bg-gradient-to-br from-modern-amber-400 to-modern-amber-600 rounded-2xl flex items-center justify-center shadow-glow group-hover:scale-110 transition-transform duration-300">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-2xl font-bold text-modern-slate-900 mb-2">Price Analytics</h3>
                <p class="text-modern-slate-600">Market intelligence</p>
              </div>
            </div>
            <p class="text-modern-slate-600 leading-relaxed mb-6">
              Track price movements and market trends with advanced analytics. Get AI-powered predictions and optimal selling times for maximum returns.
            </p>
            <router-link to="/price-trends" class="inline-flex items-center text-modern-amber-600 hover:text-modern-amber-700 font-semibold group-hover:text-modern-amber-800 transition-colors duration-300">
              View Analytics
              <svg class="w-5 h-5 ml-2 transform group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4-4m4 4v10l-4 4m-6-0a2 2 0 00-2-2H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2V6a2 2 0 00-2-2z"></path>
              </svg>
            </router-link>
          </div>
        </div>

        <!-- Weather Dashboard Card -->
        <div class="card group hover:shadow-glow transform transition-all duration-500 animate-slide-up" style="animation-delay: 1.6s;">
          <div class="p-8">
            <div class="flex items-center mb-6">
              <div class="w-16 h-16 bg-gradient-to-br from-modern-purple-400 to-modern-purple-600 rounded-2xl flex items-center justify-center shadow-glow group-hover:scale-110 transition-transform duration-300">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path>
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-2xl font-bold text-modern-slate-900 mb-2">Weather Intelligence</h3>
                <p class="text-modern-slate-600">Climate insights</p>
              </div>
            </div>
            <p class="text-modern-slate-600 leading-relaxed mb-6">
              Get real-time weather data and farming recommendations based on current conditions. Optimize planting schedules with predictive climate analytics.
            </p>
            <router-link to="/weather" class="inline-flex items-center text-modern-purple-600 hover:text-modern-purple-700 font-semibold group-hover:text-modern-purple-800 transition-colors duration-300">
              Check Weather
              <svg class="w-5 h-5 ml-2 transform group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4-4m4 4v10l-4 4m-6-0a2 2 0 00-2-2H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2V6a2 2 0 00-2-2z"></path>
              </svg>
            </router-link>
          </div>
        </div>

        <!-- Advanced Analytics Card -->
        <div class="card group hover:shadow-glow transform transition-all duration-500 animate-slide-up" style="animation-delay: 1.8s;">
          <div class="p-8">
            <div class="flex items-center mb-6">
              <div class="w-16 h-16 bg-gradient-to-br from-accent-400 to-accent-600 rounded-2xl flex items-center justify-center shadow-glow group-hover:scale-110 transition-transform duration-300">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-2xl font-bold text-modern-slate-900 mb-2">Advanced Analytics</h3>
                <p class="text-modern-slate-600">Data-driven insights</p>
              </div>
            </div>
            <p class="text-modern-slate-600 leading-relaxed mb-6">
              Comprehensive analytics and reporting for your farm. Make data-driven decisions with AI-powered insights and predictive modeling.
            </p>
            <router-link to="/analytics" class="inline-flex items-center text-accent-600 hover:text-accent-700 font-semibold group-hover:text-accent-800 transition-colors duration-300">
              View Analytics
              <svg class="w-5 h-5 ml-2 transform group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4-4m4 4v10l-4 4m-6-0a2 2 0 00-2-2H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2V6a2 2 0 00-2-2z"></path>
              </svg>
            </router-link>
          </div>
        </div>

        <!-- Notifications Card -->
        <div class="card group hover:shadow-glow transform transition-all duration-500 animate-slide-up" style="animation-delay: 2s;">
          <div class="p-8">
            <div class="flex items-center mb-6">
              <div class="w-16 h-16 bg-gradient-to-br from-modern-red-400 to-modern-red-600 rounded-2xl flex items-center justify-center shadow-glow group-hover:scale-110 transition-transform duration-300">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-2xl font-bold text-modern-slate-900 mb-2">Smart Alerts</h3>
                <p class="text-modern-slate-600">Real-time updates</p>
              </div>
            </div>
            <p class="text-modern-slate-600 leading-relaxed mb-6">
              Stay updated with important alerts, price changes, weather warnings, and market opportunities. Never miss critical information with intelligent notifications.
            </p>
            <router-link to="/notifications" class="inline-flex items-center text-modern-red-600 hover:text-modern-red-700 font-semibold group-hover:text-modern-red-800 transition-colors duration-300">
              View Notifications
              <svg class="w-5 h-5 ml-2 transform group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4-4m4 4v10l-4 4m-6-0a2 2 0 00-2-2H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2V6a2 2 0 00-2-2z"></path>
              </svg>
            </router-link>
          </div>
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

    <!-- CTA Section with Modern Design -->
    <div class="bg-gradient-to-br from-modern-slate-900 via-modern-slate-800 to-modern-slate-900 py-32">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h2 class="text-4xl md:text-5xl font-bold text-white mb-8 animate-scale-in">
            Ready to Transform Your Farming Experience?
          </h2>
          <p class="text-xl md:text-2xl text-modern-slate-300 mb-12 max-w-4xl mx-auto leading-relaxed animate-slide-up" style="animation-delay: 0.2s;">
            Join thousands of farmers and agricultural professionals using AgriConnect's cutting-edge platform
          </p>
          <div class="flex flex-col sm:flex-row gap-6 justify-center animate-slide-up" style="animation-delay: 0.4s;">
            <router-link to="/register" class="btn-accent text-lg px-10 py-4 shadow-glow group-hover:scale-105">
              <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v-3m0 3h3m-3 0h-3m2-2h-4a2 2 0 00-2-2v-4a2 2 0 012-2h4a2 2 0 012 2v4m-6 9l6 6m-6-6V6a2 2 0 012-2h4a2 2 0 012 2v12"></path>
              </svg>
              Get Started Free
            </router-link>
            <router-link to="/login" class="btn-outline text-lg px-10 py-4 border-white/20 text-white hover:bg-white/10 group-hover:scale-105">
              <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m4 4v10l-4 4m-6 0a2 2 0 00-2-2H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2V6a2 2 0 00-2-2z"></path>
              </svg>
              Sign In to Your Account
            </router-link>
          </div>
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
