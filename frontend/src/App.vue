<template>
  <div id="app">
    <!-- Navigation Bar (shown on all pages except login) -->
    <nav v-if="showNavbar" class="navbar navbar-expand-lg navbar-dark bg-success shadow-sm">
      <div class="container-fluid">
        <router-link to="/farmer-dashboard" class="navbar-brand fw-bold">
          <i class="bi bi-tree-fill me-2"></i>
          Smart Agri-Market
        </router-link>
        
        <button 
          class="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link to="/farmer-dashboard" class="nav-link">
                <i class="bi bi-speedometer2 me-1"></i>
                Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/price-comparison" class="nav-link">
                <i class="bi bi-graph-up me-1"></i>
                Prices
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/notifications" class="nav-link">
                <i class="bi bi-bell me-1"></i>
                Notifications
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/profile" class="nav-link">
                <i class="bi bi-person-circle me-1"></i>
                Profile
              </router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link text-danger" href="#" @click.prevent="logout">
                <i class="bi bi-box-arrow-right me-1"></i>
                Logout
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    showNavbar() {
      // Hide navbar on login and create-profile pages
      return this.$route.path !== '/login' && this.$route.path !== '/create-profile';
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
      this.$router.push('/login');
    }
  }
};
</script>

<style>
#app {
  min-height: 100vh;
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.nav-link {
  transition: all 0.3s ease;
  cursor: pointer;
}

.nav-link:hover {
  transform: translateY(-2px);
}

.router-link-active {
  font-weight: 600;
  border-bottom: 2px solid white;
}
</style>