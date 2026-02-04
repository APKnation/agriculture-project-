<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Price Trends</h2>

    <div class="mb-4">
      <label for="cropSelect" class="me-2 font-semibold">Select Crop:</label>
      <select id="cropSelect" v-model="selectedCrop" @change="fetchTrends" class="border p-1 rounded">
        <option v-for="crop in crops" :key="crop.id" :value="crop.id">{{ crop.name }}</option>
      </select>
    </div>

    <canvas ref="trendChart"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';

const crops = ref([]);
const selectedCrop = ref(null);
const chart = ref(null);
const trendChart = ref(null);

onMounted(async () => {
  // Fetch crops from backend
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/crops/');
    crops.value = res.data;
    if (crops.value.length) {
      selectedCrop.value = crops.value[0].id;
      fetchTrends();
    }
  } catch (err) {
    console.error('Error fetching crops:', err);
  }
});

async function fetchTrends() {
  if (!selectedCrop.value) return;

  try {
    const res = await axios.get(
      `http://127.0.0.1:8000/api/price-records/trends/?crop=${selectedCrop.value}&period=monthly`
    );

    const labels = res.data.map(r => r.region);
    const prices = res.data.map(r => r.avg_price);

    // Destroy previous chart
    if (chart.value) chart.value.destroy();

    const ctx = trendChart.value.getContext('2d');
    chart.value = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'Average Price',
            data: prices,
            backgroundColor: 'rgba(34, 197, 94, 0.6)',
            borderColor: 'rgba(34, 197, 94, 1)',
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: true },
          tooltip: { enabled: true }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  } catch (err) {
    console.error('Error fetching price trends:', err);
  }
}
</script>

<style scoped>
/* Optional styling */
select {
  min-width: 200px;
}
</style>
