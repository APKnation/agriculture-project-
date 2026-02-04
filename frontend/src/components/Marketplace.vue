<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Farmer Marketplace</h2>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-blue-500" role="status"></div>
      <p class="mt-2 text-gray-500">Loading marketplace posts...</p>
    </div>

    <div v-else-if="error" class="text-red-500 py-5 text-center">
      {{ error }}
    </div>

    <table v-else class="table-auto w-full border border-gray-300">
      <thead>
        <tr class="bg-gray-100">
          <th class="px-2 py-1 border">Farmer</th>
          <th class="px-2 py-1 border">Crop</th>
          <th class="px-2 py-1 border">Quantity</th>
          <th class="px-2 py-1 border">Price</th>
          <th class="px-2 py-1 border">Contact</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="post in posts" :key="post.id" class="hover:bg-gray-50">
          <td class="px-2 py-1 border">{{ post.farmer_username }}</td>
          <td class="px-2 py-1 border">{{ post.crop_name }}</td>
          <td class="px-2 py-1 border">{{ post.quantity }}</td>
          <td class="px-2 py-1 border">{{ post.price }}</td>
          <td class="px-2 py-1 border text-center">
            <button @click="contactFarmer(post.contact)" 
                    class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded transition">
              Contact Farmer
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const posts = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/marketplace/')
    posts.value = res.data
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load marketplace posts.'
  } finally {
    loading.value = false
  }
})

const contactFarmer = (contact) => {
  // This could be replaced with real messaging or email integration
  alert(`Contact this farmer at: ${contact}`)
}
</script>

<style scoped>
/* Optional hover effect for rows */
tbody tr:hover {
  background-color: rgba(59, 130, 246, 0.1);
  transition: background-color 0.2s;
}
</style>
m