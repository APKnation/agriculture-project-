import { defineStore } from 'pinia'
import axios from '../axios'

export const useCropsStore = defineStore('crops', {
  state: () => ({
    crops: [],
    userCrops: [],
    loading: false,
    error: null,
    selectedCrop: null,
    priceRecords: [],
    marketPosts: [],
    recommendations: []
  }),

  getters: {
    allCrops: (state) => state.crops,
    myCrops: (state) => state.userCrops,
    cropById: (state) => (id) => state.crops.find(crop => crop.id === id),
    pricesForCrop: (state) => (cropId) => state.priceRecords.filter(record => record.crop === cropId),
    marketPostsForCrop: (state) => (cropId) => state.marketPosts.filter(post => post.crop === cropId),
    isLoading: (state) => state.loading,
    getError: (state) => state.error
  },

  actions: {
    async fetchAllCrops() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/api/crops/')
        this.crops = response.data
      } catch (error) {
        this.error = 'Failed to fetch crops'
        console.error('Crops fetch error:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchUserCrops(userId) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`/api/crops/?farmer=${userId}`)
        this.userCrops = response.data
      } catch (error) {
        this.error = 'Failed to fetch user crops'
        console.error('User crops fetch error:', error)
      } finally {
        this.loading = false
      }
    },

    async createCrop(cropData) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post('/api/crops/', cropData)
        this.userCrops.push(response.data)
        return { success: true, crop: response.data }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to create crop'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async updateCrop(cropId, cropData) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.put(`/api/crops/${cropId}/`, cropData)
        const index = this.userCrops.findIndex(crop => crop.id === cropId)
        if (index !== -1) {
          this.userCrops[index] = response.data
        }
        return { success: true, crop: response.data }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update crop'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async deleteCrop(cropId) {
      this.loading = true
      this.error = null
      try {
        await axios.delete(`/api/crops/${cropId}/`)
        this.userCrops = this.userCrops.filter(crop => crop.id !== cropId)
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to delete crop'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchPriceRecords(cropId, region = null) {
      this.loading = true
      this.error = null
      try {
        const params = cropId ? { crop: cropId } : {}
        if (region) params.region = region
        
        const response = await axios.get('/api/price-records/', { params })
        this.priceRecords = response.data
      } catch (error) {
        this.error = 'Failed to fetch price records'
        console.error('Price records fetch error:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchMarketPosts() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/api/market-posts/')
        this.marketPosts = response.data
      } catch (error) {
        this.error = 'Failed to fetch market posts'
        console.error('Market posts fetch error:', error)
      } finally {
        this.loading = false
      }
    },

    async createMarketPost(postData) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post('/api/market-posts/', postData)
        this.marketPosts.unshift(response.data)
        return { success: true, post: response.data }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to create market post'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchRecommendations(region = null) {
      this.loading = true
      this.error = null
      try {
        const params = region ? { region } : {}
        const response = await axios.get('/api/crop-recommendations/', { params })
        this.recommendations = response.data
      } catch (error) {
        this.error = 'Failed to fetch recommendations'
        console.error('Recommendations fetch error:', error)
      } finally {
        this.loading = false
      }
    },

    setSelectedCrop(crop) {
      this.selectedCrop = crop
    },

    clearError() {
      this.error = null
    }
  }
})
