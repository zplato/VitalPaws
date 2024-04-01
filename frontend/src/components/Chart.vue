<script setup>
defineProps({
  data: {
    type: Array,
    required: false
  }
})
</script>

<template>
  <Line v-if="chartData.datasets[0]?.data.length>0" id="my-chart-id" :options="chartOptions" :data="chartData" />
</template>

<script>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineController, LineElement, PointElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, LineController, LineElement, PointElement)

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
        responsive: true 
      }
    }
  },
  methods: {
    async getSampleData() {
      return import("../sampleData.json")
    }
  },
  async mounted() {
    const data = this.data || this.getSampleData()
    let x = data.map(d => d.x)
    let y = data.map(d => d.y)
    let z = data.map(d => d.z)
    let abs = data.map(d => d.abs)
    let time = data.map(d => d.time)
    console.log(x)
    this.chartData.labels = time
    this.chartData.datasets.push({
        label: 'X',
        data: x,
        borderColor: 'green',
        backgroundColor: 'green',
        fill: false
    })
    this.chartData.datasets.push({
      label: 'Y',
      data: y,
      borderColor: 'blue',
      backgroundColor: 'blue',
      fill: false
    })
    this.chartData.datasets.push({
      label: 'Z',
      data: z,
      borderColor: 'yellow',
      backgroundColor: 'yellow',
      fill: false
    })
    this.chartData.datasets.push({
      label: 'ABS',
      data: abs,
      borderColor: 'gray',
      backgroundColor: 'gray',
      fill: false
    })
    // this.chartData.labels = await db.pet.toArray()
    // this.chartData.datasets[0].data = (await db.recordings.get(6)).records
    // console.log((await db.recordings.get(6)).records)
  }
}
</script>
<style scoped>

</style>
