<script setup>
import { RouterView, useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
    <v-layout class="rounded rounded-md">
      <v-app-bar :elevation="1" color="primary">
        <template v-slot:append>
          <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        </template>

        <v-app-bar-title @click="router.push({ name: 'home'})" class="cursor-pointer"><v-icon icon="mdi-paw" to="/"></v-icon>&nbsp; Vital Paws</v-app-bar-title>
      </v-app-bar>


    <v-navigation-drawer v-model="drawer" location="right">
      <!-- <v-list-item title="Vital Paws" subtitle="Dope App"></v-list-item>
      <v-divider></v-divider> -->
      <v-list-item link title="My Pets" prepend-icon="mdi-home" to="/"></v-list-item>
      <!-- <v-list-item link title="Add Pet" prepend-icon="mdi-plus"></v-list-item> -->
        <!-- <v-list-item link title="Reports" prepend-icon="mdi-chart-line"></v-list-item> -->
        <v-list-item link title="About App" prepend-icon="mdi-information" to="/about"></v-list-item>
      </v-navigation-drawer>

      <v-main class="">
        <RouterView />
      </v-main>
    </v-layout>

  
</template>

<script>
export default {
  data: () => ({
    drawer: false,
    theme: 'light'
  })
}
</script>

<style>
body {
  background-color: rgb(238, 238, 238)
}

.shadow {
  text-shadow: 1px 1px 2px rgb(75, 75, 75);
}

</style>
