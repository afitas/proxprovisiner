<template>
  <v-container class="pa-4">
    <v-row justify="center">
      <v-col cols="12" xl="10">
        <v-card class="elevation-2">
          <v-toolbar color="primary" dark>
            <v-toolbar-title class="text-h5">Infrastructure Dashboard</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn
              color="white"
              variant="outlined"
              prepend-icon="mdi-plus"
              class="ml-4"
              @click="$router.push('/create')"
            >
              New Infrastructure
            </v-btn>
          </v-toolbar>
          
          <v-card-text class="pa-4">
            <v-data-table
              :headers="headers"
              :items="infrastructures"
              :loading="loading"
              class="elevation-1"
              :items-per-page="10"
              :footer-props="{
                'items-per-page-options': [5, 10, 15, 20],
                'items-per-page-text': 'VMs per page'
              }"
            >
              <template v-slot:item.status="{ item }">
                <v-chip
                  :color="getStatusColor(item.status)"
                  :class="{'white--text': item.status !== 'pending'}"
                  small
                >
                  {{ item.status }}
                </v-chip>
              </template>
              
              <template v-slot:item.created_at="{ item }">
                {{ new Date(item.created_at).toLocaleString() }}
              </template>

              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon
                  variant="text"
                  color="primary"
                  class="mr-2"
                  @click="viewDetails(item)"
                >
                  <v-icon>mdi-eye</v-icon>
                </v-btn>
                <v-btn
                  icon
                  variant="text"
                  :color="item.status === 'running' ? 'error' : 'success'"
                  @click="toggleVMStatus(item)"
                >
                  <v-icon>{{ item.status === 'running' ? 'mdi-stop' : 'mdi-play' }}</v-icon>
                </v-btn>
              </template>

              <template v-slot:no-data>
                <v-alert
                  type="info"
                  class="ma-4"
                >
                  No infrastructures found. Click "New Infrastructure" to create one.
                </v-alert>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Details Dialog -->
    <v-dialog v-model="detailsDialog" max-width="600">
      <v-card v-if="selectedInfra">
        <v-toolbar color="primary" dark>
          <v-toolbar-title>Infrastructure Details</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon @click="detailsDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>

        <v-card-text class="pa-4">
          <v-list>
            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-tag</v-icon>
              </template>
              <v-list-item-title>Name</v-list-item-title>
              <v-list-item-subtitle>{{ selectedInfra.name }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-identifier</v-icon>
              </template>
              <v-list-item-title>VM ID</v-list-item-title>
              <v-list-item-subtitle>{{ selectedInfra.vm_id }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-cpu-64-bit</v-icon>
              </template>
              <v-list-item-title>CPU Cores</v-list-item-title>
              <v-list-item-subtitle>{{ selectedInfra.cpu_cores }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-memory</v-icon>
              </template>
              <v-list-item-title>Memory</v-list-item-title>
              <v-list-item-subtitle>{{ selectedInfra.memory }} GB</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-harddisk</v-icon>
              </template>
              <v-list-item-title>Disk Size</v-list-item-title>
              <v-list-item-subtitle>{{ selectedInfra.disk_size }} GB</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-circle-slice-8</v-icon>
              </template>
              <v-list-item-title>Status</v-list-item-title>
              <v-list-item-subtitle>
                <v-chip
                  :color="getStatusColor(selectedInfra.status)"
                  :class="{'white--text': selectedInfra.status !== 'pending'}"
                  small
                >
                  {{ selectedInfra.status }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            variant="outlined"
            @click="detailsDialog = false"
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
  name: 'Dashboard',
  data() {
    return {
      loading: false,
      infrastructures: [],
      headers: [
        { 
          title: 'Name',
          align: 'start',
          key: 'name',
          sortable: true
        },
        { title: 'VM ID', key: 'vm_id', align: 'center' },
        { title: 'CPU Cores', key: 'cpu_cores', align: 'center' },
        { title: 'Memory (GB)', key: 'memory', align: 'center' },
        { title: 'Disk Size (GB)', key: 'disk_size', align: 'center' },
        { title: 'Status', key: 'status', align: 'center' },
        { title: 'Created At', key: 'created_at', align: 'center' },
        { title: 'Actions', key: 'actions', align: 'center', sortable: false }
      ],
      detailsDialog: false,
      selectedInfra: null
    }
  },
  methods: {
    getStatusColor(status) {
      switch (status.toLowerCase()) {
        case 'running':
          return 'success';
        case 'stopped':
          return 'error';
        case 'pending':
          return 'warning';
        default:
          return 'grey';
      }
    },
    async fetchInfrastructures() {
      this.loading = true;
      try {
        const response = await axios.get('http://localhost:5000/api/infrastructure');
        this.infrastructures = response.data;
      } catch (error) {
        console.error('Failed to fetch infrastructures:', error);
      } finally {
        this.loading = false;
      }
    },
    viewDetails(infra) {
      this.selectedInfra = infra;
      this.detailsDialog = true;
    },
    async toggleVMStatus(infra) {
      try {
        const action = infra.status === 'running' ? 'stop' : 'start';
        await axios.post(`http://localhost:5000/api/infrastructure/${infra.vm_id}/${action}`);
        await this.fetchInfrastructures();
      } catch (error) {
        console.error(`Failed to ${action} VM:`, error);
      }
    }
  },
  created() {
    this.fetchInfrastructures();
  }
}
</script>

<style scoped>
.v-data-table {
  border-radius: 8px;
}

.v-list-item {
  margin-bottom: 8px;
}

.v-list-item__title {
  font-weight: 500;
  color: rgba(0, 0, 0, 0.87);
}

.v-list-item__subtitle {
  margin-top: 4px;
}
</style>
