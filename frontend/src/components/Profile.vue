<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Monthly Price Trends</h2>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { Chart } from 'chart.js/auto'
import axios from 'axios'
import { onMounted, ref } from 'vue'

const chartCanvas = ref(null)
const prices = ref([])

onMounted(async () => {
  const res = await axios.get(
    'http://localhost:8000/api/prices/trends/1/?period=monthly'
  )

  prices.value = res.data

  new Chart(chartCanvas.value, {
    type: 'line',
    data: {
      labels: prices.value.map(p => p.date),
      datasets: [
        {
          label: 'Price',
          data: prices.value.map(p => p.price),
          fill: false
        }
      ]
    }
  })
})
</script>
