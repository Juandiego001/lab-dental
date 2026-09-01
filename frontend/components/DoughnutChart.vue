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

const emit = defineEmits(['setFilter'])

// 1. Registrar los módulos de Chart.js necesarios para un diagrama circular
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

// 2. Mockup Data: Diferenciando el Valor X y el Valor Y
const chartData = ref({
  labels: props.labels,
  datasets: [
    {
      // Colores para diferenciar visualmente los sectores
      backgroundColor: props.backgroundColor,
      hoverBackgroundColor: props.hoverBackgroundColor, // Cambio sutil al pasar el cursor,
      data: props.data, // Aquí defines los valores de X e Y
      borderWidth: 2,
      borderColor: '#ffffff'
    }
  ]
})

// 3. Configuración del diagrama y la ventana flotante (Tooltip)
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  onClick: (event, elements, chart) => {
    // 1. Verificamos si el clic ocurrió directamente sobre un sector (y no en el espacio en blanco)
    if (elements.length > 0) {
      // 2. Tomamos el primer elemento detectado bajo el cursor
      const clickedElement = elements[0];

      // 3. Obtenemos el índice del sector clickeado
      const dataIndex = clickedElement.index;
      const datasetIndex = clickedElement.datasetIndex;

      // 4. Extraemos la etiqueta y el valor exacto desde los datos del gráfico
      const label = chart.data.labels[dataIndex];
      const value = chart.data.datasets[datasetIndex].data[dataIndex];

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
    // Configuración de la ventana flotante al pasar el cursor
    tooltip: {
      enabled: true,
      backgroundColor: 'rgba(15, 23, 42, 0.9)', // Fondo oscuro y semitransparente
      titleFont: { size: 14, family: 'sans-serif' },
      bodyFont: { size: 14, family: 'sans-serif' },
      padding: 12,
      cornerRadius: 8,
      callbacks: {
        // Personalizamos el texto que aparece en la ventana flotante
        label: function (context) {
          const label = context.label || '';
          const value = context.raw || 0;
          return ` ${label}: ${value} unidades`;
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