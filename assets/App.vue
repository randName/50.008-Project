<template>
<v-app :dark="dark">
  <NavBar @dark="dark=!dark"/>
  <v-content>
    <v-fade-transition mode="out-in">
      <router-view></router-view>
    </v-fade-transition>
  </v-content>
</v-app>
</template>

<script>
import NavBar from './components/Nav.vue'

export default {
  data () {
    return {
      dark: true
    }
  },
  methods: {
  },
  created () {
    this.$user.get()
    this.$cart.get()
  },
  components: {
    NavBar
  }
}
</script>
