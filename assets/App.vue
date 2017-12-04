<template>
<v-app dark>
  <NavBar/>
  <v-content>
    <v-container fluid grid-list-lg>
      <v-slide-x-transition mode="out-in">
        <router-view></router-view>
      </v-slide-x-transition>
    </v-container>
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
