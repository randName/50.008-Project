<template>
<div>
  <v-toolbar app fixed clipped-left>
    <v-toolbar-side-icon @click.stop="drawer=!drawer"></v-toolbar-side-icon>
    <v-toolbar-title>Solid Eureka</v-toolbar-title>
    <template v-if="this.$route.name == 'Shop'">
    <v-spacer></v-spacer>
    <v-btn icon>
      <v-icon>search</v-icon>
    </v-btn>
    </template>
  </v-toolbar>
  <v-navigation-drawer clipped fixed app v-model="drawer">
    <v-list dense>
      <template v-if="user.is_authenticated">
      <v-list-group :value="userdrop">
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
        <v-list-tile v-for="i in useractions" :key="i.title" :to="{name: i.route}">
          <v-list-tile-action>
            <v-icon>{{ i.action }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>{{ i.route }}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list-group>
      </template>
      <v-list-tile v-else avatar>
        <v-list-tile-action>
          <v-icon>account_circle</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>Login</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
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
  props: ['user'],
  computed: {
    useractions () {
      let actions = [
        { route: 'Profile', action: 'home' },
        { route: 'Logout', action: 'exit_to_app' }
      ]
      if (this.user.is_staff) {
        actions.splice(1, 0, {route: 'Manager', action: 'dashboard'})
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
