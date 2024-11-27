<template>
  <v-container>
    <v-row justify="center" align="center" style="min-height: 100vh;">
      <v-col cols="12" sm="10" md="8" lg="6" xl="4">
        <v-card class="mx-auto elevation-5">
          <v-toolbar dark color="primary">
            <v-toolbar-title>Login</v-toolbar-title>
          </v-toolbar>

          <v-card-text>
            <v-form @submit.prevent="login" ref="form">
              <v-text-field
                v-model="username"
                label="Username"
                required
                :rules="[v => !!v || 'Username is required']"
                class="my-2"
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Password"
                type="password"
                required
                :rules="[v => !!v || 'Password is required']"
                class="my-2"
              ></v-text-field>

              <v-btn
                color="primary"
                block
                :loading="loading"
                @click="login"
                class="mt-4"
              >
                Login
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Error Snackbar -->
    <v-snackbar
      v-model="showError"
      color="error"
      timeout="3000"
      bottom
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
        
        console.log('Login response:', response.data);
        localStorage.setItem('token', 'true'); // Forcer le token pour le test
        this.$router.push('/dashboard');
      } catch (error) {
        console.error('Login error:', error);
        this.errorMessage = error.response?.data?.error || 'Login failed';
        this.showError = true;
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.v-card {
  margin: 0 auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
