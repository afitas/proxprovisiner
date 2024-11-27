<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="elevation-12">
          <v-toolbar dark color="primary">
            <v-toolbar-title>Create New Infrastructure</v-toolbar-title>
          </v-toolbar>
          
          <v-card-text>
            <v-form @submit.prevent="createInfrastructure" ref="form">
              <v-text-field
                v-model="form.name"
                label="VM Name"
                required
                :rules="[v => !!v || 'Name is required']"
              ></v-text-field>

              <v-slider
                v-model="form.cpu_cores"
                label="CPU Cores"
                min="1"
                max="8"
                thumb-label
                required
              ></v-slider>

              <v-slider
                v-model="form.memory"
                label="Memory (GB)"
                min="1"
                max="32"
                thumb-label
                required
              ></v-slider>

              <v-slider
                v-model="form.disk_size"
                label="Disk Size (GB)"
                min="10"
                max="500"
                thumb-label
                required
              ></v-slider>
            </v-form>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              :loading="loading"
              @click="createInfrastructure"
            >
              Create Infrastructure
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Success Dialog -->
    <v-dialog v-model="successDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5 green--text">
          Success
        </v-card-title>
        <v-card-text>
          Infrastructure has been created successfully!
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="goToDashboard"
          >
            Go to Dashboard
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Error Dialog -->
    <v-dialog v-model="errorDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5 red--text">
          Error
        </v-card-title>
        <v-card-text>
          {{ errorMessage }}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="error"
            text
            @click="errorDialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'InfraForm',
  data() {
    return {
      form: {
        name: '',
        cpu_cores: 1,
        memory: 2,
        disk_size: 20
      },
      loading: false,
      successDialog: false,
      errorDialog: false,
      errorMessage: ''
    }
  },
  methods: {
    async createInfrastructure() {
      if (!this.$refs.form.validate()) return;

      this.loading = true;
      try {
        await axios.post('http://localhost:5000/api/infrastructure', this.form);
        this.successDialog = true;
        this.$refs.form.reset();
      } catch (error) {
        this.errorMessage = error.response?.data?.error || 'An error occurred while creating the infrastructure';
        this.errorDialog = true;
      } finally {
        this.loading = false;
      }
    },
    goToDashboard() {
      this.successDialog = false;
      this.$router.push('/dashboard');
    }
  }
}
</script>
