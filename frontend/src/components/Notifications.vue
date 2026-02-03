<template>
  <div class="notifications-wrapper">
    <div class="container py-5">
      <!-- Header Section -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex align-items-center justify-content-between flex-wrap gap-3">
            <div>
              <h2 class="fw-bold mb-2">
                <i class="bi bi-bell-fill text-primary me-2"></i>
                Smart Selling-Time Notifications
              </h2>
              <p class="text-muted mb-0">
                <i class="bi bi-info-circle me-1"></i>
                Stay updated on the best times to sell your crops
              </p>
            </div>
            <div class="d-flex gap-2">
              <span class="badge bg-primary rounded-pill px-3 py-2">
                <i class="bi bi-envelope me-1"></i>
                {{ unreadCount }} Unread
              </span>
              <span class="badge bg-secondary rounded-pill px-3 py-2">
                <i class="bi bi-envelope-open me-1"></i>
                {{ notifications.length }} Total
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="text-muted mt-3">Loading notifications...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle-fill me-2"></i>
        {{ error }}
      </div>

      <!-- Empty State -->
      <div v-else-if="notifications.length === 0" class="text-center py-5">
        <div class="empty-state">
          <i class="bi bi-bell-slash display-1 text-muted mb-3"></i>
          <h4 class="text-muted">No Notifications Yet</h4>
          <p class="text-muted">You'll receive notifications when it's the optimal time to sell your crops.</p>
        </div>
      </div>

      <!-- Notifications Table -->
      <div v-else class="card border-0 shadow-sm">
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th class="px-4 py-3">
                    <i class="bi bi-flower1 me-2 text-success"></i>Crop
                  </th>
                  <th class="px-4 py-3">
                    <i class="bi bi-chat-left-text me-2 text-info"></i>Message
                  </th>
                  <th class="px-4 py-3">
                    <i class="bi bi-calendar-event me-2 text-warning"></i>Created At
                  </th>
                  <th class="px-4 py-3 text-center">
                    <i class="bi bi-eye me-2 text-primary"></i>Status
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="note in notifications" 
                  :key="note.id"
                  :class="{ 'table-active': !note.read }"
                  class="notification-row"
                >
                  <td class="px-4 py-3">
                    <div class="d-flex align-items-center">
                      <div class="crop-icon me-3">
                        <i class="bi bi-grain"></i>
                      </div>
                      <div>
                        <div class="fw-semibold">{{ note.crop.name }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-4 py-3">
                    <div class="message-text">
                      {{ note.message }}
                    </div>
                  </td>
                  <td class="px-4 py-3">
                    <div class="d-flex flex-column">
                      <span class="fw-medium">
                        {{ formatDate(note.created_at) }}
                      </span>
                      <small class="text-muted">
                        {{ formatTime(note.created_at) }}
                      </small>
                    </div>
                  </td>
                  <td class="px-4 py-3 text-center">
                    <span 
                      v-if="note.read" 
                      class="badge bg-success-subtle text-success border border-success-subtle rounded-pill px-3 py-2"
                    >
                      <i class="bi bi-check-circle-fill me-1"></i>Read
                    </span>
                    <span 
                      v-else 
                      class="badge bg-primary-subtle text-primary border border-primary-subtle rounded-pill px-3 py-2"
                    >
                      <i class="bi bi-circle-fill me-1" style="font-size: 0.5rem;"></i>Unread
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Pagination (if needed) -->
      <div v-if="notifications.length > 0" class="row mt-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <p class="text-muted mb-0">
              Showing {{ notifications.length }} notification{{ notifications.length !== 1 ? 's' : '' }}
            </p>
            <button class="btn btn-outline-primary">
              <i class="bi bi-arrow-clockwise me-2"></i>Refresh
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return { 
      notifications: [],
      loading: true,
      error: null
    };
  },
  computed: {
    unreadCount() {
      return this.notifications.filter(n => !n.read).length;
    }
  },
  async mounted() {
    await this.fetchNotifications();
  },
  methods: {
    async fetchNotifications() {
      this.loading = true;
      this.error = null;
      
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/notifications/');
        console.log('Notifications from API:', res.data);
        this.notifications = res.data;
      } catch (err) {
        console.error('Error fetching notifications:', err);
        this.error = 'Failed to load notifications. Please try again later.';
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric', 
        year: 'numeric' 
      });
    },
    formatTime(dateString) {
      const date = new Date(dateString);
      return date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit'
      });
    }
  }
};
</script>

<style scoped>
.notifications-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Card Styling */
.card {
  border-radius: 15px;
  overflow: hidden;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Table Header */
.table-light {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white !important;
}

.table-light th {
  color: white !important;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.875rem;
  letter-spacing: 0.5px;
  border: none !important;
}

/* Table Rows */
.notification-row {
  transition: all 0.3s ease;
  cursor: pointer;
}

.notification-row:hover {
  background-color: rgba(102, 126, 234, 0.05) !important;
  transform: translateX(5px);
}

.table-active {
  background-color: rgba(13, 110, 253, 0.05);
  border-left: 4px solid #0d6efd;
}

/* Crop Icon */
.crop-icon {
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.25rem;
}

/* Message Text */
.message-text {
  color: #495057;
  line-height: 1.6;
  max-width: 400px;
}

/* Badges */
.badge {
  font-weight: 500;
  font-size: 0.85rem;
}

.bg-primary-subtle {
  background-color: rgba(13, 110, 253, 0.1) !important;
}

.bg-success-subtle {
  background-color: rgba(25, 135, 84, 0.1) !important;
}

/* Empty State */
.empty-state {
  padding: 3rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.empty-state i {
  opacity: 0.3;
}

/* Responsive Table */
@media (max-width: 768px) {
  .table-responsive {
    font-size: 0.875rem;
  }
  
  .px-4 {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
  }
  
  .crop-icon {
    width: 35px;
    height: 35px;
    font-size: 1rem;
  }
  
  .message-text {
    font-size: 0.85rem;
  }
}

/* Button Styling */
.btn-outline-primary {
  border-width: 2px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(13, 110, 253, 0.2);
}

/* Table Borders */
.table > :not(caption) > * > * {
  border-bottom-width: 1px;
  border-color: #e9ecef;
}

tbody tr:last-child td {
  border-bottom: none;
}
</style>