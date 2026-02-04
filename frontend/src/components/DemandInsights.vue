<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Supply & Demand Insights</h2>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-blue-500" role="status"></div>
      <p class="mt-2 text-gray-500">Loading demand insights...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-red-500 py-5 text-center">
      {{ error }}
    </div>

    <!-- Table -->
    <table v-else class="table-auto w-full border border-gray-300">
      <thead>
        <tr class="bg-gray-100">
          <th class="px-2 py-1 border">Crop</th>
          <th class="px-2 py-1 border">Market</th>
          <th class="px-2 py-1 border">Demand Level</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="d in demand" :key="d.id" class="hover:bg-gray-50">
          <td class="px-2 py-1 border">{{ d.crop__name }}</td>
          <td class="px-2 py-1 border">{{ d.market }}</td>
          <td class="px-2 py-1 border">{{ d.records }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const demand = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/demand/')
    demand.value = res.data
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load demand insights.'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
tbody tr:hover {
  background-color: rgba(59, 130, 246, 0.1);
  transition: background-color 0.2s;
}
</style>
