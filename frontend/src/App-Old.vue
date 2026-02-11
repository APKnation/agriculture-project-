<template>
  <div id="app">
    <AppNavbar />
    <main class="min-h-screen">
      <router-view />
    </main>
  </div>
</template>

<script>
import AppNavbar from './components/AppNavbar.vue'

export default {
  name: 'App',
  components: {
    AppNavbar
  }
}
</script>

<style>
/* Remove all existing styles and use Tailwind CSS */
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
