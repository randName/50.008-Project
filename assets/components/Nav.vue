<template>
<div>
  <v-toolbar app fixed clipped-left>
    <v-toolbar-side-icon @click.stop="drawer=!drawer"></v-toolbar-side-icon>
    <v-toolbar-title>Solid Eureka</v-toolbar-title>
    <template v-if="$route.name == 'Shop'">
    <v-spacer></v-spacer>
    <v-btn icon>
      <v-icon>search</v-icon>
    </v-btn>
    </template>
  </v-toolbar>
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
    </v-list>
  </v-navigation-drawer>
</div>
</template>

<script>
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
  data () {
    return {
      drawer: false,
      userdrop: false,
      links: [
        { route: 'Shop', action: 'store' },
        { route: 'Cart', action: 'shopping_cart' }
      ]
    }
  }
}
</script>
