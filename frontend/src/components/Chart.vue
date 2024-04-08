<script setup>
defineProps({
  data: {
    type: Array,
    required: false
  },

})
</script>

<template>
  <Line v-if="chartData.datasets[0]?.data.length>0" id="my-chart-id" :options="chartOptions" :data="chartData" />
</template>

<script>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineController, LineElement, PointElement, CategoryScale, LinearScale, Colors} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, LineController, LineElement, PointElement, Colors)

export default {
  name: 'Chart',
  components: { Line },
  data() {
    return {
      chartData: {
        // labels: ['January', 'February', 'March'],
        datasets: []
      },
      chartOptions: {
        plugins: {
          colors: {
            enabled: true
          }
        },
        responsive: true,
        scales: {
          x: {
            title: {
              text: "Time (s)",
              display: true
            }
          },
          y: {
            title: {
              text: "Acceleration (g)",
              display: true
            }
          }
        }
      }
    }
  },
  methods: {
    async getSampleData() {
      return import("../sampleData.json")
    },
    labels(config){
      var cfg = config || {};
      var min = cfg.min || 0;
      var max = cfg.max || 100;
      var count = cfg.count || 8;
      var step = (max - min) / count;
      var decimals = cfg.decimals || 8;
      var dfactor = Math.pow(10, decimals) || 0;
      var prefix = cfg.prefix || '';
      var values = [];
      var i;

      for (i = min; i < max; i += step) {
        values.push(prefix + Math.round(dfactor * i) / dfactor);
      }

      return values;
    }
  },
  async mounted() {
    const data = this.data || this.getSampleData()

    const end = Math.ceil(this.data[this.data.length-1].time)


    let x = data.map(d => d.x)
    let y = data.map(d => d.y)
    let z = data.map(d => d.z)
    let abs = data.map(d => d.abs)
    // let time = data.map(d => d.time)
    this.chartData.labels = this.labels({max: end})


    this.chartData.datasets.push({
        label: 'X',
        data: x,
        fill: false
    })
    this.chartData.datasets.push({
      label: 'Y',
      data: y,
      fill: false
    })
    this.chartData.datasets.push({
      label: 'Z',
      data: z,
      fill: false
    })
    this.chartData.datasets.push({
      label: 'ABS',
      data: abs,
      fill: false
    })
  }
}
</script>
<style scoped>

</style>
