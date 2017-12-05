<template>
<v-flex d-flex xs4>
  <v-card flat tile>
    <v-card-text>
      {{ name }}
    </v-card-text>
  </v-card>
</v-flex>
</template>

<script>
export default {
  props: ['id', 'name'],
  data () {
    return {
      item: {}
    }
  }
}
</script>
