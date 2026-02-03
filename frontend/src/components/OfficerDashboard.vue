<template>
  <div>
    <h2>📊 Market Officer Dashboard</h2>
    <p>Welcome, {{ user.username }} (Region: {{ user.region }})</p>
    <h3>Manage Price Records</h3>
    <form @submit.prevent="addPriceRecord">
      <select v-model="cropId">
        <option v-for="crop in crops" :key="crop.id" :value="crop.id">{{ crop.name }}</option>
      </select>
      <input v-model="region" placeholder="Region" />
      <input v-model="price" type="number" placeholder="Price" />
      <button type="submit">Add Record</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return { user: {}, crops: [], cropId: null, region: '', price: '' };
  },
  async mounted() {
    const userRes = await axios.get('http://127.0.0.1:8000/api/users/2/'); // example officer
    this.user = userRes.data;
    const cropsRes = await axios.get('http://127.0.0.1:8000/api/crops/');
    this.crops = cropsRes.data;
  },
  methods: {
    async addPriceRecord() {
      await axios.post('http://127.0.0.1:8000/api/price-records/', {
        crop: this.cropId,
        region: this.region,
        price: this.price
      });
      alert('Price record added!');
    }
  }
};
</script>
