<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-bold text-dark">
        <i class="bi bi-bell-fill text-success me-2"></i>Notifications
      </h2>
      <span v-if="notifications.length" class="badge bg-secondary">
        Total: {{ notifications.length }}
      </span>
    </div>

    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-success" style="width: 3rem; height: 3rem;" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2 text-muted">Checking for updates...</p>
    </div>

    <div v-else>
      <div v-if="notifications.length === 0" class="card shadow-sm border-0">
        <div class="card-body text-center py-5">
          <i class="bi bi-mailbox2 display-4 text-muted"></i>
          <p class="mt-3 fs-5 text-secondary">No notifications available right now.</p>
        </div>
      </div>

      <div v-else class="card shadow-sm border-0">
        <div class="list-group list-group-flush">
          <div 
            v-for="notification in notifications" 
            :key="notification.id" 
            class="list-group-item list-group-item-action p-3 border-start border-4"
            :class="notification.read ? 'border-light' : 'border-success bg-light-success'"
          >
            <div class="d-flex justify-content-between align-items-start">
              <div class="me-3">
                <span v-if="!notification.read" class="badge rounded-circle p-1 bg-success mb-2">
                  <span class="visually-hidden">Unread</span>
                </span>
                <p class="mb-1 text-dark" :class="{'fw-bold': !notification.read}">
                  {{ notification.message }}
                </p>
                <small class="text-muted">
                  <i class="bi bi-clock me-1"></i>{{ formatDate(notification.created_at) }}
                </small>
              </div>
              
              <button class="btn btn-sm btn-outline-secondary rounded-pill">
                View Details
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Notifications",
  data() {
    return {
      notifications: [],
      loading: true,
    };
  },
  mounted() {
    this.fetchNotifications();
  },
  methods: {
    fetchNotifications() {
      this.loading = true;
      axios
        .get("http://localhost:8000/api/notifications/")
        .then((response) => {
          this.notifications = response.data;
        })
        .catch((error) => {
          console.error("Failed to load notifications:", error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    formatDate(datetime) {
      if (!datetime) return "Just now";
      const date = new Date(datetime);
      return date.toLocaleDateString([], { month: 'short', day: 'numeric' }) + " at " + 
             date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
  },
};
</script>

<style scoped>
/* Custom subtle green background for unread items */
.bg-light-success {
  background-color: #f8fff9;
}

/* Card hover effect */
.list-group-item-action:hover {
  background-color: #f1f3f5;
  transition: 0.3s;
}

.card {
  border-radius: 12px;
  overflow: hidden;
}
</style>