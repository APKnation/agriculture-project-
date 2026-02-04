<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Average Prices by Region</h2>

    <ul>
      <li v-for="r in regions" :key="r.region">
        Region: {{ r.region }} – Avg Price: {{ r.avg_price }}
      </li>
    </ul>
  </div>
</template>

<!-- 👇 THIS IS EXACTLY WHERE YOUR CODE GOES -->
<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const regions = ref([])

onMounted(async () => {
  const res = await axios.get('http://localhost:8000/api/prices/regions/')
  regions.value = res.data
})
</script>
