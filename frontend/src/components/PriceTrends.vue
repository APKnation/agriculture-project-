<template>
  <div>
    <h2>Price Trends</h2>
    <select v-model="selectedCrop" @change="fetchTrends">
      <option v-for="crop in crops" :key="crop.id" :value="crop.id">{{ crop.name }}</option>
    </select>
    <canvas id="trendChart"></canvas>
  </div>
</template>

<script>
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
  data() {
    return { crops: [], selectedCrop: null, chart: null };
  },
  async mounted() {
    const res = await axios.get('http://127.0.0.1:8000/api/crops/');
    this.crops = res.data;
  },
  methods: {
    async fetchTrends() {
      const res = await axios.get(
        `http://127.0.0.1:8000/api/price-records/trends/?crop=${this.selectedCrop}&period=monthly`
      );
      const labels = res.data.map(r => r.region);
      const prices = res.data.map(r => r.avg_price);

      if (this.chart) this.chart.destroy();
      const ctx = document.getElementById('trendChart').getContext('2d');
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [{ label: 'Average Price', data: prices }]
        }
      });
    }
  }
};
</script>
