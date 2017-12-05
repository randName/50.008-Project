<template>
<v-app dark>
  <NavBar/>
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
    }
  },
  methods: {
  },
  created () {
    this.$user.get()
  },
  components: {
    NavBar
  }
}
</script>
