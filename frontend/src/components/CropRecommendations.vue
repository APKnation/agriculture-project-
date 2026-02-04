<template>
  <div class="p-4">
    <h3 class="text-lg font-bold mb-4">Recommended Crops</h3>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-3">
      <div class="spinner-border text-green-500" role="status"></div>
      <p class="mt-2 text-gray-500">Loading crop recommendations...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-red-500 py-3 text-center">
      {{ error }}
    </div>

    <!-- List of Recommendations -->
    <ul v-else class="list-disc pl-5 space-y-1">
      <li v-for="c in crops" :key="c.crop__name" class="text-gray-700">
        {{ c.crop__name }}
      </li>
    </ul>

    <!-- Empty State -->
    <div v-if="!loading && crops.length === 0" class="text-gray-500 py-3 text-center">
      No crop recommendations available at the moment.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const crops = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/recommendations/')
    crops.value = res.data
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load crop recommendations.'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.spinner-border {
  width: 2rem;
  height: 2rem;
  border-width: 0.25rem;
}
</style>
