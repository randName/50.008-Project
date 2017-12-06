<template>
<div>
  <v-toolbar app fixed>
    <v-toolbar-side-icon @click.stop="drawer=!drawer"></v-toolbar-side-icon>
    <v-btn v-if="$route.name=='Shop'" icon large @click="searching=true">
      <v-icon>search</v-icon>
    </v-btn>
    <v-btn v-else icon @click="$router.go(-1)">
      <v-icon>arrow_back</v-icon>
    </v-btn>
    <v-spacer></v-spacer>
    <v-toolbar-title>Solid Eureka</v-toolbar-title>
  </v-toolbar>
  <SearchBar :searching="searching" @nosearch="searching=false"/>
  <v-navigation-drawer clipped fixed app v-model="drawer">
    <v-list dense>
      <v-slide-x-transition>
        <v-list-group v-if="user.is_authenticated" :value="userdrop">
          <v-list-tile slot="item">
            <v-list-tile-action>
              <v-icon>account_circle</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{ user.username }}</v-list-tile-title>
            </v-list-tile-content>
            <v-list-tile-action>
              <v-icon>keyboard_arrow_down</v-icon>
            </v-list-tile-action>
          </v-list-tile>
          <v-list-tile v-for="i in useractions" :key="i.title" @click="i.click">
            <v-list-tile-action>
              <v-icon>{{ i.action }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{ i.title }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list-group>
        <v-list-tile v-else avatar :to="{name: 'Login'}">
          <v-list-tile-action>
            <v-icon>account_circle</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Login</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-slide-x-transition>
      <v-divider></v-divider>
      <v-list-tile v-for="i in links" :key="i.title" :to="{name: i.route}">
        <v-list-tile-action>
          <v-icon>{{ i.action }}</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>{{ i.route }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
      <v-list-tile>
        <v-list-tile-action>
          <v-icon style="transform: rotate(45deg)">brightness_2</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-switch label="Dark Mode" v-model="dark"></v-switch>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
  </v-navigation-drawer>
</div>
</template>

<script>
import SearchBar from './SearchBar.vue'

export default {
  computed: {
    user () {
      return this.$user.user
    },
    useractions () {
      let actions = [
        {
          title: 'Profile',
          action: 'home',
          click: () => this.$router.push('/user')
        },
        {
          title: 'Logout',
          action: 'exit_to_app',
          click: () => this.$user.logout().then(() => this.$router.push('/'))
        }
      ]
      if (this.user.is_staff) {
        actions.splice(1, 0, {
          title: 'Manager',
          action: 'dashboard',
          click: () => this.$router.push('/manager')
        })
      }
      return actions;
    }
  },
  watch: {
    dark () {
      this.$emit('dark')
    }
  },
  components: {
    SearchBar
  },
  data () {
    return {
      dark: true,
      drawer: false,
      userdrop: false,
      searching: false,
      links: [
        { route: 'Shop', action: 'store' },
        { route: 'Cart', action: 'shopping_cart' }
      ]
    }
  }
}
</script>
