<template>
  <div class="notifications-dashboard">
    <!-- Header Section -->
    <div class="dashboard-header text-white p-4 mb-4 rounded-3 shadow-lg" style="background: var(--gradient-info);">
      <div class="container-fluid">
        <div class="row align-items-center">
          <div class="col-md-6">
            <h1 class="mb-0 fw-bold">
              
              Notifications Center
            </h1>
          </div>
          <div class="col-md-6 text-md-end">
            <div class="notification-stats d-flex gap-3 justify-content-md-end">
              <div class="text-center">
                <div class="badge bg-white text-info fs-6 mb-1">
                  
                  {{ totalNotifications }}
                </div>
                <small class="text-white-50">Total</small>
              </div>
              <div class="text-center">
                <div class="badge bg-white text-warning fs-6 mb-1">
                  
                  {{ unreadCount }}
                </div>
                <small class="text-white-50">Unread</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container-fluid">
      <!-- Filter and Actions -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-md-4">
                  <label class="form-label fw-semibold">
                    <i class="bi bi-funnel me-2"></i>
                    Filter by Type
                  </label>
                  <select v-model="selectedType" class="form-select">
                    <option value="">All Notifications</option>
                    <option value="price_alert">Price Alerts</option>
                    <option value="market_update">Market Updates</option>
                    <option value="system">System Messages</option>
                    <option value="weather">Weather Updates</option>
                  </select>
                </div>
                <div class="col-md-4">
                  <label class="form-label fw-semibold">
                    <i class="bi bi-calendar me-2"></i>
                    Time Period
                  </label>
                  <select v-model="timeFilter" class="form-select">
                    <option value="">All Time</option>
                    <option value="today">Today</option>
                    <option value="week">This Week</option>
                    <option value="month">This Month</option>
                  </select>
                </div>
                <div class="col-md-4">
                  <label class="form-label fw-semibold">
                    <i class="bi bi-search me-2"></i>
                    Search
                  </label>
                  <div class="input-group">
                    <input v-model="searchQuery" type="text" class="form-control" 
                           placeholder="Search notifications...">
                    <button class="btn btn-outline-secondary" @click="clearSearch">
                      <i class="bi bi-x-lg"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Notifications List -->
      <div class="row">
        <div class="col-12">
          <div class="card border-0 shadow-lg">
            <div class="card-header bg-white border-bottom">
              <div class="row align-items-center">
                <div class="col-md-6">
                  <h5 class="mb-0 text-dark">
                    <i class="bi bi-list-ul me-2"></i>
                    Recent Notifications
                  </h5>
                </div>
                <div class="col-md-6 text-md-end">
                  <div class="btn-group" role="group">
                    <button @click="markAllAsRead" 
                            class="btn btn-sm btn-outline-success"
                            :disabled="unreadCount === 0">
                      <i class="bi bi-check-all me-1"></i>
                      Mark All Read
                    </button>
                    <button @click="refreshNotifications" 
                            class="btn btn-sm btn-outline-primary"
                            :disabled="loading">
                      <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
                      <i class="bi bi-arrow-clockwise me-1"></i>
                      Refresh
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div class="card-body p-0">
              <!-- Loading State -->
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading notifications...</span>
                </div>
                <p class="mt-3 mb-0 text-muted">Loading your notifications...</p>
              </div>

              <!-- Empty State -->
              <div v-else-if="filteredNotifications.length === 0" class="text-center py-5">
                <div class="empty-state">
                  <i class="bi bi-inbox display-1 text-muted mb-3"></i>
                  <h5 class="text-muted">No notifications found</h5>
                  <p class="text-muted">
                    {{ searchQuery ? 'No notifications match your search criteria.' : 'You\'re all caught up!' }}
                  </p>
                  <button v-if="searchQuery || selectedType || timeFilter" 
                          @click="clearFilters" 
                          class="btn btn-outline-primary mt-3">
                    <i class="bi bi-arrow-clockwise me-2"></i>
                    Clear Filters
                  </button>
                </div>
              </div>

              <!-- Notifications List -->
              <div v-else class="notifications-list">
                <div v-for="notification in filteredNotifications" :key="notification.id"
                     class="notification-item border-bottom"
                     :class="{
                       'unread': !notification.read,
                       'bg-light': !notification.read,
                       'hover-effect': true
                     }">
                  <div class="notification-content p-3">
                    <div class="row align-items-start">
                      <!-- Notification Icon and Type -->
                      <div class="col-auto">
                        <div class="notification-icon me-3"
                             :class="getNotificationIconClass(notification.type)">
                          <i :class="getNotificationIcon(notification.type)"></i>
                        </div>
                      </div>

                      <!-- Notification Content -->
                      <div class="col">
                        <div class="d-flex justify-content-between align-items-start">
                          <div class="flex-grow-1">
                            <h6 class="mb-1" :class="{'fw-bold': !notification.read}">
                              {{ notification.title || notification.message }}
                            </h6>
                            <p class="mb-1 text-muted small">
                              {{ notification.message }}
                            </p>
                          </div>
                          <div class="notification-actions">
                            <button v-if="!notification.read" 
                                    @click="markAsRead(notification.id)"
                                    class="btn btn-sm btn-outline-success me-2"
                                    title="Mark as read">
                              <i class="bi bi-check"></i>
                            </button>
                            <button @click="deleteNotification(notification.id)"
                                    class="btn btn-sm btn-outline-danger"
                                    title="Delete notification">
                              <i class="bi bi-trash"></i>
                            </button>
                          </div>
                        </div>
                        <div class="text-muted small mt-1">
                          <i class="bi bi-clock me-1"></i>
                          {{ formatDateTime(notification.created_at) }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  name: 'Notifications',
  data() {
    return {
      notifications: [],
      loading: false,
      selectedType: '',
      timeFilter: '',
      searchQuery: '',
      totalNotifications: 0,
      unreadCount: 0
    };
  },
  computed: {
    filteredNotifications() {
      let filtered = this.notifications;

      // Filter by type
      if (this.selectedType) {
        filtered = filtered.filter(n => n.type === this.selectedType);
      }

      // Filter by time
      if (this.timeFilter) {
        const now = new Date();
        filtered = filtered.filter(n => {
          const notificationDate = new Date(n.created_at);
          switch (this.timeFilter) {
            case 'today':
              return notificationDate.toDateString() === now.toDateString();
            case 'week':
              const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
              return notificationDate >= weekAgo;
            case 'month':
              const monthAgo = new Date(now.getFullYear(), now.getMonth(), 1);
              return notificationDate >= monthAgo;
            default:
              return true;
          }
        });
      }

      // Filter by search query
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(n => 
          n.message.toLowerCase().includes(query) ||
          (n.title && n.title.toLowerCase().includes(query))
        );
      }

      return filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    }
  },
  async mounted() {
    await this.fetchNotifications();
  },
  methods: {
    async fetchNotifications() {
      this.loading = true;
      try {
        const response = await axios.get('/notifications/');
        this.notifications = response.data;
        this.updateCounts();
      } catch (error) {
        console.error('Error fetching notifications:', error);
        this.showErrorAlert('Failed to load notifications. Please try again.');
      } finally {
        this.loading = false;
      }
    },

    updateCounts() {
      this.totalNotifications = this.notifications.length;
      this.unreadCount = this.notifications.filter(n => !n.read).length;
    },

    async markAsRead(notificationId) {
      try {
        await axios.patch(`/notifications/${notificationId}/`, { read: true });
        const notification = this.notifications.find(n => n.id === notificationId);
        if (notification) {
          notification.read = true;
        }
        this.updateCounts();
        this.showSuccessAlert('Notification marked as read');
      } catch (error) {
        console.error('Error marking notification as read:', error);
        this.showErrorAlert('Failed to update notification.');
      }
    },

    async markAllAsRead() {
      try {
        const unreadIds = this.notifications.filter(n => !n.read).map(n => n.id);
        for (const id of unreadIds) {
          await axios.patch(`/notifications/${id}/`, { read: true });
        }
        this.notifications.forEach(n => n.read = true);
        this.updateCounts();
        this.showSuccessAlert(`Marked ${unreadIds.length} notifications as read`);
      } catch (error) {
        console.error('Error marking all as read:', error);
        this.showErrorAlert('Failed to mark notifications as read.');
      }
    },

    async deleteNotification(notificationId) {
      if (!confirm('Are you sure you want to delete this notification?')) {
        return;
      }
      
      try {
        await axios.delete(`/notifications/${notificationId}/`);
        this.notifications = this.notifications.filter(n => n.id !== notificationId);
        this.updateCounts();
        this.showSuccessAlert('Notification deleted successfully');
      } catch (error) {
        console.error('Error deleting notification:', error);
        this.showErrorAlert('Failed to delete notification.');
      }
    },

    async refreshNotifications() {
      await this.fetchNotifications();
      this.showSuccessAlert('Notifications refreshed');
    },

    clearFilters() {
      this.selectedType = '';
      this.timeFilter = '';
      this.searchQuery = '';
    },

    clearSearch() {
      this.searchQuery = '';
    },

    getNotificationIcon(type) {
      const icons = {
        price_alert: 'bi bi-currency-dollar',
        market_update: 'bi bi-graph-up',
        system: 'bi bi-info-circle',
        weather: 'bi bi-cloud-sun',
        default: 'bi bi-bell'
      };
      return icons[type] || icons.default;
    },

    getNotificationIconClass(type) {
      const classes = {
        price_alert: 'text-warning',
        market_update: 'text-success',
        system: 'text-info',
        weather: 'text-primary',
        default: 'text-secondary'
      };
      return classes[type] || classes.default;
    },

    formatDateTime(datetime) {
      if (!datetime) return 'Unknown time';
      
      const date = new Date(datetime);
      const now = new Date();
      const diffTime = now - date;
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays === 0) {
        return `Today at ${date.toLocaleTimeString('en-US', { 
          hour: '2-digit', 
          minute: '2-digit' 
        })}`;
      } else if (diffDays === 1) {
        return `Yesterday at ${date.toLocaleTimeString('en-US', { 
          hour: '2-digit', 
          minute: '2-digit' 
        })}`;
      } else if (diffDays < 7) {
        return `${diffDays} days ago`;
      } else {
        return date.toLocaleDateString('en-US', {
          month: 'short',
          day: 'numeric',
          year: 'numeric'
        });
      }
    },

    showSuccessAlert(message) {
      const alertDiv = document.createElement('div');
      alertDiv.className = 'alert alert-success alert-dismissible fade show position-fixed';
      alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
      alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      `;
      document.body.appendChild(alertDiv);
      
      setTimeout(() => {
        if (alertDiv.parentNode) {
          alertDiv.parentNode.removeChild(alertDiv);
        }
      }, 3000);
    },

    showErrorAlert(message) {
      const alertDiv = document.createElement('div');
      alertDiv.className = 'alert alert-danger alert-dismissible fade show position-fixed';
      alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
      alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      `;
      document.body.appendChild(alertDiv);
      
      setTimeout(() => {
        if (alertDiv.parentNode) {
          alertDiv.parentNode.removeChild(alertDiv);
        }
      }, 5000);
    }
  }
};
</script>

<style scoped>
.notifications-dashboard {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.dashboard-header {
  background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
}

.notification-item {
  transition: all 0.3s ease;
  cursor: pointer;
}

.notification-item:hover {
  background-color: #f1f3f5;
  transform: translateX(5px);
}

.notification-item.unread {
  border-left: 4px solid #17a2b8;
  background-color: #f8f9ff;
}

.notification-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.notification-icon.text-warning {
  background-color: #fff3cd;
  color: #856404;
}

.notification-icon.text-success {
  background-color: #d4edda;
  color: #155724;
}

.notification-icon.text-info {
  background-color: #d1ecf1;
  color: #0c5460;
}

.notification-icon.text-primary {
  background-color: #cfe2ff;
  color: #084298;
}

.notification-icon.text-secondary {
  background-color: #e2e3e5;
  color: #6c757d;
}

.notification-actions .btn {
  transition: all 0.2s ease;
}

.notification-actions .btn:hover {
  transform: scale(1.05);
}

.empty-state {
  max-width: 400px;
  margin: 0 auto;
}

.card {
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
}

.position-fixed {
  position: fixed;
}

.badge {
  font-size: 0.8em;
}

.bg-gradient-info {
  background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
}

.hover-effect {
  position: relative;
}

.hover-effect::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(23, 162, 184, 0.1), transparent);
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}

.hover-effect:hover::after {
  transform: translateX(0);
}
</style>