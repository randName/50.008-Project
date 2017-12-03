<template>
<v-app dark>
  <NavBar :user="user"/>
  <v-content>
    <v-container fluid>
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
      user: {
        is_authenticated: false
      }
    }
  },
  components: {
    NavBar
  }
}
</script>
