<template>
  <div class="chart-wrapper">
    <ClientOnly>
      <Doughnut :data="chartData" :options="chartOptions" />

      <template #fallback>
        <v-progress-circular :size="100" :width="15" color="primary" indeterminate />
      </template>
    </ClientOnly>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'vue-chartjs'

const { t } = useI18n();
const emit = defineEmits(['setFilter'])

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  labels: {
    type: Array,
    required: true,
    default: ['W', 'X']
  },
  data: {
    type: Array,
    required: true,
    default: [65, 35]
  },
  filters: {
    type: Array,
    required: true,
    default: ['connected', 'disconnected']
  },
  backgroundColor: {
    type: Array,
    required: false,
    default: ['#3b82f6', '#f43f5e']
  },
  hoverBackgroundColor: {
    type: Array,
    required: false,
    default: ['#2563eb', '#e11d48']
  }
})

const chartData = ref({
  labels: props.labels,
  datasets: [
    {
      backgroundColor: props.backgroundColor,
      hoverBackgroundColor: props.hoverBackgroundColor,
      data: props.data,
      borderWidth: 2,
      borderColor: '#ffffff'
    }
  ]
})

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  onClick: (event, elements, chart) => {
    if (elements.length > 0) {
      const clickedElement = elements[0];
      emit('setFilter', props.filters[clickedElement.index]);
    }
  },
  onHover: (event, chartElement) => {
    if (chartElement.length > 0) {
      event.native.target.style.cursor = 'pointer';
    } else {
      event.native.target.style.cursor = 'default';
    }
  },
  plugins: {
    tooltip: {
      enabled: true,
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      titleFont: { size: 14, family: 'sans-serif' },
      bodyFont: { size: 14, family: 'sans-serif' },
      padding: 12,
      cornerRadius: 8,
      callbacks: {
        label: function (context) {
          const label = context.label || '';
          const value = context.raw || 0;
          return ` ${label}: ${value} ${t('aligners.units')}`;
        }
      }
    },
    legend: {
      position: 'bottom',
      labels: {
        font: { size: 14 }
      }
    },
  },
})
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  max-width: 300px;
  /* Tamaño máximo del diagrama */
  height: 400px;
  margin: 0 auto;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>