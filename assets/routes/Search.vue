<template>
<v-container>
  <h1>Search Results</h1>
</v-container>
</template>

<script>
export default {
  mounted () {
    console.log(this.$route.query)
  },
  data () {
    return {}
  }
}
</script>
