import { defineStore } from 'pinia'
import axios from '../axios'

export const useNotificationsStore = defineStore('notifications', {
  state: () => ({
    notifications: [],
    unreadCount: 0,
    loading: false,
    error: null,
    priceAlerts: [],
    wsConnection: null
  }),

  getters: {
    allNotifications: (state) => state.notifications,
    unreadNotifications: (state) => state.notifications.filter(n => !n.read),
    hasUnread: (state) => state.unreadCount > 0,
    allPriceAlerts: (state) => state.priceAlerts,
    isConnected: (state) => !!state.wsConnection
  },

  actions: {
    async fetchNotifications(userId) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`/api/notifications/?user=${userId}`)
        this.notifications = response.data
        this.unreadCount = this.notifications.filter(n => !n.read).length
      } catch (error) {
        this.error = 'Failed to fetch notifications'
        console.error('Notifications fetch error:', error)
      } finally {
        this.loading = false
      }
    },

    async markAsRead(notificationId) {
      try {
        await axios.patch(`/api/notifications/${notificationId}/`, { read: true })
        const notification = this.notifications.find(n => n.id === notificationId)
        if (notification && !notification.read) {
          notification.read = true
          this.unreadCount = Math.max(0, this.unreadCount - 1)
        }
        return { success: true }
      } catch (error) {
        this.error = 'Failed to mark notification as read'
        return { success: false, error: this.error }
      }
    },

    async markAllAsRead(userId) {
      try {
        const unreadIds = this.unreadNotifications.map(n => n.id)
        await Promise.all(unreadIds.map(id => this.markAsRead(id)))
        return { success: true }
      } catch (error) {
        this.error = 'Failed to mark all notifications as read'
        return { success: false, error: this.error }
      }
    },

    async deleteNotification(notificationId) {
      try {
        await axios.delete(`/api/notifications/${notificationId}/`)
        const index = this.notifications.findIndex(n => n.id === notificationId)
        if (index !== -1) {
          const notification = this.notifications[index]
          if (!notification.read) {
            this.unreadCount = Math.max(0, this.unreadCount - 1)
          }
          this.notifications.splice(index, 1)
        }
        return { success: true }
      } catch (error) {
        this.error = 'Failed to delete notification'
        return { success: false, error: this.error }
      }
    },

    async fetchPriceAlerts(userId) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`/api/price-alerts/?user=${userId}`)
        this.priceAlerts = response.data
      } catch (error) {
        this.error = 'Failed to fetch price alerts'
        console.error('Price alerts fetch error:', error)
      } finally {
        this.loading = false
      }
    },

    async createPriceAlert(alertData) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post('/api/price-alerts/', alertData)
        this.priceAlerts.push(response.data)
        return { success: true, alert: response.data }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to create price alert'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async updatePriceAlert(alertId, alertData) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.put(`/api/price-alerts/${alertId}/`, alertData)
        const index = this.priceAlerts.findIndex(alert => alert.id === alertId)
        if (index !== -1) {
          this.priceAlerts[index] = response.data
        }
        return { success: true, alert: response.data }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update price alert'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async deletePriceAlert(alertId) {
      this.loading = true
      this.error = null
      try {
        await axios.delete(`/api/price-alerts/${alertId}/`)
        this.priceAlerts = this.priceAlerts.filter(alert => alert.id !== alertId)
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to delete price alert'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    initWebSocket(userId) {
      if (this.wsConnection) {
        this.wsConnection.close()
      }

      const wsUrl = `ws://localhost:8000/ws/notifications/${userId}/`
      this.wsConnection = new WebSocket(wsUrl)

      this.wsConnection.onopen = () => {
        console.log('WebSocket connected')
      }

      this.wsConnection.onmessage = (event) => {
        const data = JSON.parse(event.data)
        if (data.type === 'notification') {
          this.notifications.unshift(data.notification)
          if (!data.notification.read) {
            this.unreadCount += 1
          }
        } else if (data.type === 'price_alert') {
          const existingAlert = this.priceAlerts.find(alert => alert.id === data.alert.id)
          if (existingAlert) {
            Object.assign(existingAlert, data.alert)
          } else {
            this.priceAlerts.push(data.alert)
          }
        }
      }

      this.wsConnection.onerror = (error) => {
        console.error('WebSocket error:', error)
      }

      this.wsConnection.onclose = () => {
        console.log('WebSocket disconnected')
        this.wsConnection = null
      }
    },

    closeWebSocket() {
      if (this.wsConnection) {
        this.wsConnection.close()
        this.wsConnection = null
      }
    },

    addNotification(notification) {
      this.notifications.unshift(notification)
      if (!notification.read) {
        this.unreadCount += 1
      }
    },

    clearError() {
      this.error = null
    }
  }
})
