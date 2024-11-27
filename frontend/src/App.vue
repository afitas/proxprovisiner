<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title class="text-h6 font-weight-bold">
        Proxmox Provisioner
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <div class="d-flex align-center">
        <v-btn
          v-if="isLoggedIn"
          color="white"
          variant="outlined"
          density="comfortable"
          prepend-icon="mdi-logout"
          @click="logout"
        >
          Déconnexion
        </v-btn>
      </div>
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>

    <!-- Global Snackbar -->
    <v-snackbar
      v-model="showSnackbar"
      :color="snackbarColor"
      :timeout="3000"
      bottom
    >
      {{ snackbarText }}
      <template v-slot:action="{ attrs }">
        <v-btn
          text
          v-bind="attrs"
          @click="showSnackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      showSnackbar: false,
      snackbarText: '',
      snackbarColor: 'success'
    }
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('token');
    }
  },
  methods: {
    async logout() {
      try {
        localStorage.removeItem('token');
        await this.$router.push('/login');
        this.showSnackbar = true;
        this.snackbarText = 'Déconnexion réussie';
        this.snackbarColor = 'success';
      } catch (error) {
        console.error('Erreur lors de la déconnexion:', error);
      }
    }
  }
}
</script>

<style>
.v-application {
  background-color: #f5f5f5 !important;
}

.v-main {
  min-height: 100vh;
}

.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px;
}

.centered-card {
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Style pour le bouton de déconnexion */
.v-app-bar .v-btn {
  height: 36px !important;
  min-width: 100px;
  margin-right: 16px;
  border: 2px solid white;
}

.v-app-bar .v-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
</style>
