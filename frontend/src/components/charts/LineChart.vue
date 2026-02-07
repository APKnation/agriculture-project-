<template>
  <canvas ref="chartCanvas"></canvas>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import 'chartjs-adapter-date-fns'

// Register Chart.js components
Chart.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

export default {
  name: 'LineChart',
  props: {
    data: {
      type: Object,
      required: true
    },
    options: {
      type: Object,
      default: () => ({})
    }
  },
  setup(props) {
    const chartCanvas = ref(null)
    let chartInstance = null

    const defaultOptions = {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        legend: {
          position: 'top',
          labels: {
            usePointStyle: true,
            padding: 20
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#fff',
          bodyColor: '#fff',
          borderColor: '#ddd',
          borderWidth: 1,
          padding: 12,
          displayColors: true,
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || ''
              if (label) {
                label += ': '
              }
              if (context.parsed.y !== null) {
                label += new Intl.NumberFormat('en-US', {
                  style: 'currency',
                  currency: 'USD'
                }).format(context.parsed.y)
              }
              return label
            }
          }
        }
      },
      scales: {
        x: {
          display: true,
          title: {
            display: true,
            text: 'Date'
          },
          grid: {
            display: false
          }
        },
        y: {
          display: true,
          title: {
            display: true,
            text: 'Price ($)'
          },
          beginAtZero: true,
          grid: {
            color: 'rgba(0, 0, 0, 0.05)'
          }
        }
      }
    }

    const createChart = () => {
      if (chartCanvas.value && props.data) {
        const ctx = chartCanvas.value.getContext('2d')
        
        // Destroy existing chart if it exists
        if (chartInstance) {
          chartInstance.destroy()
        }

        chartInstance = new Chart(ctx, {
          type: 'line',
          data: props.data,
          options: { ...defaultOptions, ...props.options }
        })
      }
    }

    // Watch for data changes
    watch(() => props.data, () => {
      createChart()
    }, { deep: true })

    // Watch for options changes
    watch(() => props.options, () => {
      if (chartInstance) {
        chartInstance.options = { ...defaultOptions, ...props.options }
        chartInstance.update()
      }
    }, { deep: true })

    onMounted(() => {
      createChart()
    })

    onUnmounted(() => {
      if (chartInstance) {
        chartInstance.destroy()
      }
    })

    return {
      chartCanvas
    }
  }
}
</script>

<style scoped>
canvas {
  max-height: 400px;
}
</style>
