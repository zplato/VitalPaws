<script setup>

import Chart from '../components/Chart.vue'

</script>

<template>
  <v-parallax :src="pet?.photo || 'https://placedog.net/1000?id=3'" height="200">
    <div class="d-flex flex-column fill-height justify-center align-center text-white">
      <h1 class="subheading shadow">
        {{ pet?.name || 'Unnamed Pet' }}
      </h1>
      <h4 class="font-weight-normal mb-4 shadow">
        {{ pet?.type || "Unspecified Type" }}, {{ pet?.breed || "Unspecified Breed" }}
      </h4>
    </div>
  </v-parallax>
  <v-container>
    <v-row>
      <v-col>
        <v-card class="mx-auto">
          <v-card-title>
            Record Vitals
          </v-card-title>
          <v-card-text>
            <div class="text--primary">
              Place the phone on your pet with the screen facing up. Press the record button to begin.
            </div>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" variant="flat" prepend-icon="mdi-record-circle" @click="startRecording">
              Record
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <!-- <v-row v-else>
      <v-col>
        <v-card class="mx-auto">
          <v-card-title>
            Permisson Required
          </v-card-title>
          <v-card-text>
            <div class="text--primary">
              Before you can record vitals, you must grant permission to access the phone's sensors.
            </div>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" prepend-icon="mdi-lock-open" @click="initializePermissionRequest">
              Grant Permission
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row> -->
    <v-row>
      <v-col>
        <v-card class="mx-auto">
          <v-card-title>
            Past Recordings
          </v-card-title>
          <v-card-text>
            <v-list lines="two" v-if="recordings?.length > 0">
              <v-list-item v-for="recording in recordings" :key="recording.id" :subtitle="`Recording #${recording.id}`">
                <p>{{ recording.records.length }} data points recorded.</p>
                <p>{{ new Date(recording.date).toLocaleString() }}</p>


                <template v-slot:append>
                  <v-btn color="grey-lighten-1" icon="mdi-download" variant="text"
                    @click="downloadDataAsCSV(recording)"></v-btn>
                  <v-btn color="grey-lighten-1" icon="mdi-chart-line" variant="text"
                    @click="showAlert('Coming soon!')"></v-btn>
                  <v-btn color="grey-lighten-1" icon="mdi-delete" variant="text"
                    @click="showDeleteConfirmation(recording.id)"></v-btn>
                </template>
              </v-list-item>
            </v-list>
            <p v-else>No recordings found</p>

          </v-card-text>
        </v-card>


        <v-card v-if="false" class="mx-auto">
          <v-card-title>
            Chart
          </v-card-title>
          <v-card-text>
            <!-- <Chart /> -->
          </v-card-text>
        </v-card>

      </v-col>

    </v-row>
  </v-container>
  <v-snackbar v-model="snackbar" vertical>
    <p>{{ snackbarMessage }}</p>
  </v-snackbar>
  <v-snackbar v-model="deleteConfirmation">
    <div class="text-subtitle-1 pb-2">Are you sure you want to delete this recording?</div>
    <template v-slot:actions>
      <v-btn color="primary" variant="flat" @click="deleteRecording()">
        Yes
      </v-btn>
    </template>
  </v-snackbar>
  <v-navigation-drawer v-model="bottomDrawer" location="bottom" temporary>
    <v-container>
      <v-row>
        <v-col>
          <p v-if="isRecording">Recording.... ({{ count }} records)</p>
          <p v-else>Recording Complete! Save ({{ count }}) Records? </p>
          <v-btn color="primary" class="mt-5" v-if="isRecording" @click="stopRecording">Stop Recording</v-btn>
          <v-btn color="primary" class="mt-5 mr-3" v-if="!isRecording" @click="saveRecording">Save</v-btn>
          <v-btn color="primary" variant="tonal" class="mt-5" v-if="!isRecording"
            @click="cancelRecording">Cancel</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-navigation-drawer>
</template>

<style>

.shadow {
  text-shadow: 1px 1px 2px rgb(14, 14, 14);
}
</style>


<script>
import { liveQuery } from "dexie";
import { useObservable } from "@vueuse/rxjs";
import { toRaw } from 'vue';
import { db } from '../db';
import { beginMotionDetection, endMotionDetection } from '../DeviceMotion'

export default {
  name: 'Pet',
  data() {
    return {
      bottomDrawer: false,
      sensorPermission: false,
      pet: null,
      records: [],
      count: 0,
      startTime: 0,
      endTime: process.env.RECORDING_LIMIT_IN_SECONDS || 60,
      isRecording: false,
      recordings: [],
      snackbar: false,
      snackbarMessage: '',
      deleteConfirmation: false,
      deleteId: null,

    }
  },
  methods: {
    async save() {
      // await db.pet.put(this.pet);
      // this.$router.push('/');
    },
    async startRecording() {
      // iOS 13.4+ requires a user gesture to start recording
      if('requestPermission' in DeviceMotionEvent){
        let response = await DeviceMotionEvent.requestPermission()
        console.log(response)
        if(response !== 'granted'){
          return
        }
      };

      // Begin Recording
      this.bottomDrawer = true;
      this.startTime = performance.timeOrigin + performance.now()
      this.records = []
      this.isRecording = true
      console.log(this.startTime)
      beginMotionDetection(this.logger)
    },
    stopRecording() {
      endMotionDetection(this.logger)
      this.isRecording = false
      console.log(this.records)
    },

    logger(data){

      let timeDeltaInSeconds = (( performance.timeOrigin + performance.now() ) - this.startTime) / 1000
      
      if(timeDeltaInSeconds >= this.endTime){
        this.stopRecording()
      }else{
        this.records.push({
          x: data.acceleration.x,
          y: data.acceleration.y,
          z: data.acceleration.z,
          time: timeDeltaInSeconds
        })
  
        this.count = this.records.length
      }
    
    },
    downloadDataAsCSV(recording){
      const headers = [
          '"Time (s)"', 
          '"Acceleration x(m / s ^ 2)"',
          '"Acceleration y(m / s ^ 2)"',
          '"Acceleration z(m / s ^ 2)"',
          '"Absolute acceleration (m/s^2)"'
      ]

      let data = headers.join(',') + '\n'

      recording.records.forEach( (record) => {
        data += `"${record.time}","${record.x}","${record.y}","${record.z}"` 
        data += `,"${Math.sqrt(record.x**2 + record.y**2 + record.z**2)}"\n`
      })


      let blob = new Blob([decodeURIComponent('%ef%bb%bf') , data], { type: 'text/csv;charset=utf-8'});
      let url = window.URL.createObjectURL(blob);
      let a = document.createElement('a');
      a.href = url;
      a.download = `${recording.date}_${this.pet.name}_motion_data.csv`;
      a.click();
    },
    async saveRecording(){
      console.log('saving')
      await db.recordings.put({
        petId: this.pet.id,
        date: Date.now(),
        records: toRaw(this.records)
      })
      this.cancelRecording()
    },
    async deleteRecording(){
      await db.recordings.delete(this.deleteId)
      this.deleteConfirmation = false
      this.snackbarMessage = 'Recording deleted'
      this.snackbar = true
    },
    cancelRecording(){
      this.bottomDrawer = false
      this.isRecording = false
    },
    showAlert(message){
      this.snackbarMessage = message
      this.snackbar = true
    },
    showDeleteConfirmation(id){
      this.deleteId = id
      this.deleteConfirmation = true
    },
  },
  async created() {
    console.log(this.endTime)
    // if(isDeviceMotionSupported() && !isPermissionRequired() ) {
    //   this.sensorPermission = true
    // }
    const petId = Number(this.$route.params.id);
    this.pet = await db.pets.get(petId)
    this.pet.photo = this.pet.photo ? URL.createObjectURL(this.pet.photo) : null
    this.recordings = useObservable(
      liveQuery(async () => {
        return await db.recordings.where('petId').equals(petId).reverse().toArray()
      })
    )
  },
};


</script>