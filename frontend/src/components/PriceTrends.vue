<template>
  <div class="container py-4">
    <div class="card shadow-sm">
      <div class="card-header bg-success text-white">
        <h5 class="mb-0">
          <i class="bi bi-pie-chart-fill me-2"></i>
          Price Trends
        </h5>
      </div>

      <div class="card-body">
        <!-- Crop Selector -->
        <div class="mb-3">
          <label for="cropSelect" class="form-label fw-semibold">Select Crop:</label>
          <select
            id="cropSelect"
            v-model="selectedCrop"
            @change="fetchTrends"
            class="form-select"
          >
            <option v-for="crop in crops" :key="crop.id" :value="crop.id">
              {{ crop.name }}
            </option>
          </select>
        </div>

        <!-- Chart -->
        <div class="d-flex justify-content-center">
          <canvas ref="trendChart" style="max-width: 500px;"></canvas>
        </div>
      </div>
    </div>
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

    if (chart.value) chart.value.destroy();

    const ctx = trendChart.value.getContext('2d');
    chart.value = new Chart(ctx, {
      type: 'pie',
      data: {
        labels,
        datasets: [
          {
            label: 'Average Price',
            data: prices,
            backgroundColor: [
              'rgba(4, 15, 10, 0.7)',   // Bootstrap green
              'rgba(13, 110, 253, 0.7)',  // Bootstrap blue
              'rgba(255, 193, 7, 0.7)',   // Bootstrap yellow
              'rgba(220, 53, 69, 0.7)',   // Bootstrap red
              'rgba(108, 117, 125, 0.7)'  // Bootstrap gray
            ],
            borderColor: '#fff',
            borderWidth: 2
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { font: { size: 14 } }
          },
          tooltip: { enabled: true }
        }
      }
    });
  } catch (err) {
    console.error('Error fetching price trends:', err);
  }
}
</script>

<style scoped>
.card {
  border-radius: 0.5rem;
}
</style>
