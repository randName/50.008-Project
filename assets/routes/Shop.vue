<template>
<v-container fluid grid-list-sm>
  <v-layout row wrap>
    <v-flex xs12>
      <v-card>
        <v-card-title primary-title>
          <div>
            <div class="headline">Welcome to Solid Eureka!</div>
            <span class="grey--text">The generic item store</span>
          </div>
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn :to="{name: 'Search'}">Search the store</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
export default {
  data () {
    return {
    }
  },
  components: {
  }
}
</script>
