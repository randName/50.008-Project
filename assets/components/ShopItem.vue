<template>
<v-flex d-flex xs4>
  <v-card flat tile :to="details">
    <v-card-text>
      {{ name }}
    </v-card-text>
  </v-card>
</v-flex>
</template>

<script>
export default {
  props: ['id', 'name'],
  computed: {
    details () {
      return { name: 'Item', params: {id: this.id} }
    }
  },
  data () {
    return {
      item: {}
    }
  }
}
</script>
