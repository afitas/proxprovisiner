<template>
  <v-app>
    <v-app-bar app color="primary" dark v-if="isLoggedIn">
      <v-toolbar-title>Proxmox Infrastructure Manager</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="logout">
        Logout
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('user')
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('user')
      this.$router.push('/login')
    }
  }
}
</script>
