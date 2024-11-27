<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" >
        <v-card class="elevation-12">
          <v-toolbar dark color="primary">
            <v-toolbar-title>Login to Proxmox Manager</v-toolbar-title>
          </v-toolbar>
          
          <v-card-text>
            <v-form @submit.prevent="login" ref="form">
              <v-text-field
                v-model="username"
                label="Username"
                prepend-icon="mdi-account"
                type="text"
                :rules="[v => !!v || 'Username is required']"
                required
                class="mt-4"
              ></v-text-field>
              
              <v-text-field
                v-model="password"
                label="Password"
                prepend-icon="mdi-lock"
                type="password"
                :rules="[v => !!v || 'Password is required']"
                required
                class="mt-4"
              ></v-text-field>
            </v-form>
          </v-card-text>
          
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn 
              color="primary" 
              @click="login" 
              :loading="loading"
              size="large"
            >
              Login
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Error Snackbar -->
    <v-snackbar
      v-model="showError"
      color="error"
      timeout="3000"
    >
      {{ errorMessage }}
      <template v-slot:action="{ attrs }">
        <v-btn
          text
          v-bind="attrs"
          @click="showError = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      showError: false,
      errorMessage: ''
    }
  },
  methods: {
    async login() {
      if (!this.$refs.form.validate()) return;

      this.loading = true;
      try {
        const response = await axios.post('http://localhost:5000/api/login', {
          username: this.username,
          password: this.password
        });
        
        // Store user info
        localStorage.setItem('user', JSON.stringify(response.data.user));
        
        // Redirect to dashboard
        this.$router.push('/dashboard');
      } catch (error) {
        this.errorMessage = error.response?.data?.error || 'Login failed';
        this.showError = true;
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
