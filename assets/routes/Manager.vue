<template>
<v-container>
  <h1>Manager</h1>
</v-container>
</template>

<script>
export default {
  mounted () {
    if (!this.$user.user.is_staff) {
      this.$router.replace('/')
    }
  },
  data () {
    return {}
  }
}
</script>
