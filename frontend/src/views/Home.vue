<script setup>

</script>

<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title>My Pets</v-card-title>
          <v-card-text v-if="pets.length === 0">
            No pets found. Add a pet to get started.
          </v-card-text>
          <v-list :items="pets" item-props lines="three">
            <template v-slot:subtitle="{ subtitle }">
              <div v-html="subtitle"></div>
            </template>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
    <v-row align="center" justify="center">
      <v-col cols="auto">
        <v-btn icon="mdi-plus" color="primary" to="/add"></v-btn>
      </v-col>
    </v-row>
  </v-container>
  <!-- <v-navigation-drawer v-model="drawer" location="bottom" temporary>
    <v-list :items="pets"></v-list>
  </v-navigation-drawer> -->
</template>

<script>
import { db } from '../db';

export default {
  data: () => ({
    drawer: false,
    pets: [],
  }),
  async created() {
    let pets = await db.pets.toArray()
    pets.forEach(pet => {
      this.pets.push( {
        title: pet.name || 'Unnamed Pet',
        subtitle: `${pet.type || 'Unspecified Type'} / ${pet.breed || 'Unspecified Breed'}`,
        prependAvatar: pet.photo ? URL.createObjectURL(pet.photo) : null,
        to: `/pet/${pet.id}`,
      
      });
      
    });
  },
}
</script>

<style>
.v-avatar.v-avatar--size-default {
  --v-avatar-height: 60px;
}
</style>