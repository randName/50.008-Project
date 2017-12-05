<template>
<v-container fluid grid-list-sm>
  <v-layout row wrap>
    <ShopItem v-for="i in p.view" :key="i.id" :id="i.id" :name="i.name"/>
  </v-layout>
  <div class="text-xs-center">
    <v-pagination :length="p.pages" v-model="p.page"></v-pagination>
  </div>
</v-container>
</template>

<script>
import ShopItem from '../components/ShopItem.vue'

import {Paginator} from '../pager'
Paginator.url = '/items'
Paginator.fill = {id: null, name: null}

export default {
  data () {
    return {
      p: Paginator
    }
  },
  components: {
    ShopItem
  }
}
</script>
