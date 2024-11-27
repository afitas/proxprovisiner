<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="text-h4">
            Infrastructure Dashboard
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              @click="$router.push('/create')"
            >
              Create New Infrastructure
            </v-btn>
          </v-card-title>
          
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="infrastructures"
              :loading="loading"
              class="elevation-1"
            >
              <template v-slot:item.status="{ item }">
                <v-chip
                  :color="getStatusColor(item.status)"
                  dark
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
                  small
                  class="mr-2"
                  @click="viewDetails(item)"
                >
                  <v-icon>mdi-eye</v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Details Dialog -->
    <v-dialog v-model="detailsDialog" max-width="600">
      <v-card v-if="selectedInfra">
        <v-card-title class="text-h5">
          Infrastructure Details
        </v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item>
              <v-list-item-title>Name:</v-list-item-title>
              <v-list-item-subtitle>{{ selectedInfra.name }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>VM ID:</v-list-item-title>
              <v-list-item-subtitle>{{ selectedInfra.vm_id }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>CPU Cores:</v-list-item-title>
              <v-list-item-subtitle>{{ selectedInfra.cpu_cores }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Memory:</v-list-item-title>
              <v-list-item-subtitle>{{ selectedInfra.memory }} GB</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Disk Size:</v-list-item-title>
              <v-list-item-subtitle>{{ selectedInfra.disk_size }} GB</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Status:</v-list-item-title>
              <v-list-item-subtitle>
                <v-chip :color="getStatusColor(selectedInfra.status)" dark small>
                  {{ selectedInfra.status }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
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
        { text: 'Name', value: 'name' },
        { text: 'VM ID', value: 'vm_id' },
        { text: 'CPU Cores', value: 'cpu_cores' },
        { text: 'Memory (GB)', value: 'memory' },
        { text: 'Disk Size (GB)', value: 'disk_size' },
        { text: 'Status', value: 'status' },
        { text: 'Created At', value: 'created_at' },
        { text: 'Actions', value: 'actions', sortable: false }
      ],
      detailsDialog: false,
      selectedInfra: null
    }
  },
  methods: {
    getStatusColor(status) {
      switch (status) {
        case 'running':
          return 'green';
        case 'stopped':
          return 'red';
        case 'pending':
          return 'orange';
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
    }
  },
  created() {
    this.fetchInfrastructures();
  }
}
</script>
