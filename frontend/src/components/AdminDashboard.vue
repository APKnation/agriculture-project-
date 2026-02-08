<template>
  <div>
    <h2> Admin Dashboard</h2>
    <p>Welcome, {{ user.username }}</p>
    <h3>Manage Users</h3>
    <ul>
      <li v-for="u in users" :key="u.id">{{ u.username }} ({{ u.role }})</li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return { user: {}, users: [] };
  },
  async mounted() {
    const userRes = await axios.get('/users/3/'); // example admin
    this.user = userRes.data;
    const usersRes = await axios.get('/users/');
    this.users = usersRes.data;
  }
};
</script>
