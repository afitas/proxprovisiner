<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-card class="mx-auto">
          <v-card-title class="text-h5 font-weight-bold">
            Créer une nouvelle infrastructure
          </v-card-title>

          <v-card-text>
            <v-form ref="form">
              <v-text-field
                v-model="form.name"
                label="Nom de l'infrastructure"
                required
                :rules="[v => !!v || 'Le nom est requis']"
                class="mb-4"
              ></v-text-field>

              <v-row>
                <!-- CPU -->
                <v-col cols="12" sm="4">
                  <v-card class="resource-card">
                    <div class="text-h6 mb-2">CPU</div>
                    <v-slider
                      v-model="form.cpu_cores"
                      :min="1"
                      :max="8"
                      :step="1"
                      thumb-label
                      class="mb-1"
                    ></v-slider>
                    <v-text-field
                      v-model="form.cpu_cores"
                      type="number"
                      :min="1"
                      :max="8"
                      :rules="[v => v >= 1 && v <= 8 || 'La valeur doit être entre 1 et 8']"
                      density="compact"
                      variant="outlined"
                      hide-details
                    ></v-text-field>
                  </v-card>
                </v-col>

                <!-- RAM -->
                <v-col cols="12" sm="4">
                  <v-card class="resource-card">
                    <div class="text-h6 mb-2">RAM (GB)</div>
                    <v-slider
                      v-model="form.memory"
                      :min="1"
                      :max="32"
                      :step="1"
                      thumb-label
                      class="mb-1"
                    ></v-slider>
                    <v-text-field
                      v-model="form.memory"
                      type="number"
                      :min="1"
                      :max="32"
                      :rules="[v => v >= 1 && v <= 32 || 'La valeur doit être entre 1 et 32']"
                      density="compact"
                      variant="outlined"
                      hide-details
                    ></v-text-field>
                  </v-card>
                </v-col>

                <!-- Storage -->
                <v-col cols="12" sm="4">
                  <v-card class="resource-card">
                    <div class="text-h6 mb-2">Stockage (GB)</div>
                    <v-slider
                      v-model="form.disk_size"
                      :min="10"
                      :max="500"
                      :step="10"
                      thumb-label
                      class="mb-1"
                    ></v-slider>
                    <v-text-field
                      v-model="form.disk_size"
                      type="number"
                      :min="10"
                      :max="500"
                      :rules="[v => v >= 10 && v <= 500 || 'La valeur doit être entre 10 et 500']"
                      density="compact"
                      variant="outlined"
                      hide-details
                    ></v-text-field>
                  </v-card>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              @click="submitForm"
              :loading="loading"
            >
              Créer
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'InfraForm',
  data() {
    return {
      loading: false,
      form: {
        name: '',
        cpu_cores: 1,
        memory: 1,
        disk_size: 10
      }
    }
  },
  methods: {
    async submitForm() {
      if (!this.$refs.form.validate()) return;

      this.loading = true;
      try {
        await axios.post('http://localhost:5000/api/infrastructure', this.form);
        this.$router.push('/dashboard');
      } catch (error) {
        console.error('Error:', error);
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.resource-card {
  height: 100%;
  padding: 16px;
  display: flex;
  flex-direction: column;
}

.resource-card .text-h6 {
  margin-bottom: 16px;
  color: var(--v-primary-base);
}

.v-slider {
  margin-bottom: 8px;
}

.v-text-field {
  margin-top: 4px;
}
</style>
