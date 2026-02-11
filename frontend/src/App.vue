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
</style>
