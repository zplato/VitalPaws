<template>

  <v-img cover :src="photoPreview" aspect-ratio="16/9" max-height="200">
    <div class="d-flex flex-column fill-height justify-center align-center text-white" style="position:relative">
      <h1 class="subheading shadow">
        {{ pet.name }}
      </h1>
      <h4 class="subheading shadow">
        {{ pet.type }}
      </h4>
    </div>
    <!-- <v-btn icon="mdi-camera" color="white" size="x-large" variant="text" style="position:absolute; right:0px; bottom:0px;"></v-btn> -->
  </v-img>

  <v-container>
    <v-row>
      <v-col>
        <v-form @submit.prevent="save">
          <v-card class="mx-auto" title="Add a Pet">
            <v-container>


              <v-text-field color="primary" label="Pet's Name" variant="underlined" v-model="pet.name"
                required></v-text-field>


              <v-radio-group label="Type of Pet" v-model="pet.type" style="position: relative; left: -16px;" class="mt-4">
                <v-radio label="Dog" value="Dog" selected></v-radio>
                <v-radio label="Cat" value="Cat"></v-radio>
              </v-radio-group>

              <!-- <v-select color="primary" variant="underlined" label="Type of Pet" :items="['Cat', 'Dog']"
                v-model="pet.type"></v-select> -->

              <v-text-field color="primary" label="Breed" variant="underlined" v-model="pet.breed"></v-text-field>

              <v-file-input color="primary" label="Photo" variant="underlined" prepend-icon="mdi-camera"
                v-model="fileReference" accept="image/*" capture="environment"
                @update:model-value="photoChanged"></v-file-input>

            </v-container>

            <v-divider></v-divider>

            <v-card-actions>
              <v-spacer></v-spacer>

              <v-btn color="primary" type="submit" variant="elevated">
                Save

              </v-btn>
            </v-card-actions>
          </v-card>

        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>


<script>
import { db } from '../db';

export default {
  name: 'AddPet',
  data() {
    return {
      fileReference: null,
      photoPreview: '/images/default-dog-small.jpg',
      pet: {
        name: '',
        type: '',
        breed: '',
        photo: null,
      },
    };
  },
  methods: {
    async save() {
      await db.pets.put({
        name: this.pet.name || 'Unnamed Pet',
        type: this.pet.type || 'Unspecified Type',
        breed: this.pet.breed || 'Unspecified Breed',
        photo: this.pet.photo || null,
      });
      this.$router.push('/');
    },
    photoChanged(file) {
      let img = Array.isArray(file) ? file[0] : file
      this.pet.photo = img
      this.photoPreview = URL.createObjectURL(img)
    },
  },
  async created() {

    // const petId = this.$route.params.id;
    // this.pet = await db.pet.get(petId);
  },
};


</script>