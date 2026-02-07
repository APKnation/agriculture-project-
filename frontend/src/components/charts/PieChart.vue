<template>
  <canvas ref="chartCanvas"></canvas>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import {
  Chart,
  CategoryScale,
  LinearScale,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

// Register Chart.js components
Chart.register(
  CategoryScale,
  LinearScale,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

export default {
  name: 'PieChart',
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
          display: true,
          position: 'right',
          labels: {
            usePointStyle: true,
            padding: 20,
            generateLabels: function(chart) {
              const data = chart.data
              if (data.labels.length && data.datasets.length) {
                const dataset = data.datasets[0]
                const total = dataset.data.reduce((a, b) => a + b, 0)
                return data.labels.map((label, i) => {
                  const value = dataset.data[i]
                  const percentage = ((value / total) * 100).toFixed(1)
                  return {
                    text: `${label} (${percentage}%)`,
                    fillStyle: dataset.backgroundColor[i],
                    hidden: false,
                    index: i
                  }
                })
              }
              return []
            }
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
              const label = context.label || ''
              const value = context.parsed
              const total = context.dataset.data.reduce((a, b) => a + b, 0)
              const percentage = ((value / total) * 100).toFixed(1)
              return `${label}: ${new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD'
              }).format(value)} (${percentage}%)`
            }
          }
        }
      },
      animation: {
        animateRotate: true,
        animateScale: false,
        duration: 1000,
        easing: 'easeInOutQuart'
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
          type: 'pie',
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
