<template>
<v-flex v-if="item" d-flex xs12 sm6>
  <v-card flat tile :to="details">
    <v-card-title>
      {{ item.name }}
    </v-card-title>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-chip>
        <v-avatar>
          <v-icon>history</v-icon>
        </v-avatar>
        {{ item.date_created | moment("MMM Do YY") }}
      </v-chip>
      <v-chip>
        <v-avatar>
          <v-icon>star</v-icon>
        </v-avatar>
        {{ score }}
      </v-chip>
    </v-card-actions>
  </v-card>
</v-flex>
</template>

<script>
export default {
  props: ['item'],
  computed: {
    score () {
      if ( this.item.score ) {
        return parseFloat(this.item.score).toFixed(1)
      } else {
        return '-'
      }
    },
    details () {
      return { name: 'Item', params: {id: this.item.id} }
    }
  },
  data () {
    return {
    }
  }
}
</script>
