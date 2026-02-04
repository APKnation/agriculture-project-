<template>
  <div id="app">
    <!-- Navbar -->
    <nav v-if="showNavbar" class="navbar navbar-expand-lg navbar-dark bg-success shadow-sm">
      <div class="container-fluid">
        <router-link to="/dashboard" class="navbar-brand fw-bold">
          <i class="bi bi-tree-fill me-2"></i>
          Smart Agri-Market
        </router-link>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
            </li>

            <li class="nav-item">
              <router-link to="/marketplace" class="nav-link">Marketplace</router-link>
            </li>

            <li class="nav-item">
              <router-link to="/price-trends" class="nav-link">Price Trends</router-link>
            </li>

            <li class="nav-item">
              <router-link to="/demand" class="nav-link">Supply & Demand</router-link>
            </li>

            <li class="nav-item">
              <router-link to="/recommendations" class="nav-link">Recommendations</router-link>
            </li>

            <li class="nav-item">
              <router-link to="/notifications" class="nav-link">Notifications</router-link>
            </li>

            <li class="nav-item">
              <router-link to="/profile" class="nav-link">Profile</router-link>
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
  name: "App",
  computed: {
    showNavbar() {
      // Hide navbar only on login
      return this.$route.path !== "/login";
    },
  },
};
</script>

<style>
#app { min-height: 100vh; }
body { margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }

.nav-link { transition: all 0.3s ease; cursor: pointer; }
.nav-link:hover { transform: translateY(-2px); }

.router-link-active { font-weight: 600; border-bottom: 2px solid white; }
</style>
