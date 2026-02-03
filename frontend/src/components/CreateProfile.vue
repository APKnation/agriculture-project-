<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <!-- Card wrapper -->
        <div class="card shadow-sm">
          <div class="card-header bg-success text-white text-center">
            <h4 class="mb-0">Create Profile</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="createProfile">
              <!-- Username -->
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input
                  id="username"
                  v-model="username"
                  type="text"
                  class="form-control"
                  placeholder="Enter your username"
                  required
                />
              </div>

              <!-- Password -->
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input
                  id="password"
                  v-model="password"
                  type="password"
                  class="form-control"
                  placeholder="Enter your password"
                  required
                />
              </div>

              <!-- Submit button -->
              <div class="d-grid">
                <button type="submit" class="btn btn-success fw-bold">
                  Create Account
                </button>
              </div>
            </form>
          </div>
          <div class="card-footer text-center">
            <small class="text-muted">Already have an account? <router-link to="/login">Login here</router-link></small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import router from '../router';

export default {
  data() {
    return { username: '', password: '' };
  },
  methods: {
    async createProfile() {
      await axios.post('http://127.0.0.1:8000/api/users/', {
        username: this.username,
        password: this.password
      });
      // login immediately
      const res = await axios.post('http://127.0.0.1:8000/api/token/', {
        username: this.username,
        password: this.password
      });
      localStorage.setItem('token', res.data.access);
      router.push('/farmer-dashboard'); // default redirect
    }
  }
};
</script>
