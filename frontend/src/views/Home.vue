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
          <v-list>

            <v-list-item v-for="pet in pets" :key="pet.id" :subtitle="pet.subtitle"
              :title="pet.title" :to="pet.to" class="mb-3">
              <template v-slot:prepend>
                <v-avatar color="grey-lighten-1">
                  <v-img :src="pet.prependAvatar"></v-img>
                </v-avatar>
              </template>

              <template v-slot:append>
                <v-btn color="grey-lighten-1" icon="mdi-delete" variant="text" @click.prevent="deletePet(pet.id)"></v-btn>
              </template>
            </v-list-item>
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
</template>

<script>
import { db } from '../db';

export default {
  data: () => ({
    drawer: false,
    pets: [],
  }),
  methods: {
    async deletePet(id, e) {
      if(confirm('Are you sure you want to delete this pet?')) {
        await db.pets.delete(id);
        this.pets = this.pets.filter(p => p.id !== id);
      }
      return false
    },
    async getPets() {
      this.pets = [];
      let pets = await db.pets.toArray();
      pets.forEach(pet => {
        this.pets.push({
          id: pet.id,
          title: pet.name || 'Unnamed Pet',
          subtitle: `${pet.type || 'Unspecified Type'} / ${pet.breed || 'Unspecified Breed'}`,
          prependAvatar: pet.photo ? URL.createObjectURL(pet.photo) : null,
          to: `/pet/${pet.id}`,
        });
      });
    },
  },
  async created() {
    await this.getPets();
  },
}
</script>

<style>
.v-avatar.v-avatar--size-default {
  --v-avatar-height: 60px;
}
</style>