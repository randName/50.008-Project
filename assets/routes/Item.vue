<template>
<v-container fluid grid-list-lg>
  <v-layout v-if="item.id" row wrap>
    <v-flex xs12>
      <v-card>
        <v-card-title primary-title>
          <div class="headline">{{ item.name }}</div>
        </v-card-title>
        <v-card-text>
          <p>{{ item.description }}</p>
          <div class="text-xs-left">
            <v-chip>
              <v-avatar>
                <v-icon>history</v-icon>
              </v-avatar>
              {{ item.date_created | moment("MMM Do YY") }}
            </v-chip>
            <v-chip @click="search({company: item.company.id})">
              <v-avatar>
                <v-icon>business</v-icon>
              </v-avatar>
              {{ item.company.name }}
            </v-chip>
          </div>
          <div class="text-xs-left">
            <v-chip v-for="c in item.creators" :key="c.id"
              @click="search({creator: c.id})">
              <v-avatar>
                <v-icon>face</v-icon>
              </v-avatar>
              {{ c.name }}
            </v-chip>
          </div>
          <div class="text-xs-left">
            <v-chip v-for="c in item.categorys" :key="c.id"
              @click="search({category: c.id})">
              <v-avatar>
                <v-icon>label</v-icon>
              </v-avatar>
              {{ c.name }}
            </v-chip>
          </div>
          <div class="text-xs-left">
            <v-chip color="green" text-color="white">
              <v-avatar class="green darken-3">$</v-avatar>
              {{ item.price }}
            </v-chip>
            <v-chip color="primary" text-color="white">
              {{ item.quantity }} in stock
            </v-chip>
          </div>
        </v-card-text>
      </v-card>
    </v-flex>
    <v-dialog v-model="dialog">
      <v-btn fab fixed bottom right color="primary" slot="activator">
        <v-icon>shopping_basket</v-icon>
      </v-btn>
      <v-card>
        <v-card-title>
          <div class="headline">Add to cart</div>
        </v-card-title>
        <v-card-text>
          Quantity Chooser
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-layout>
  <v-progress-linear v-else :indeterminate="true"></v-progress-linear>
</v-container>
</template>

<script>
export default {
  computed: {
  },
  methods: {
    get (id) {
      this.$http.get('/item/' + id)
      .then(r => this.item = r.data.data)
      .catch(e => this.$router.go(-1))
    },
    search (query) {
      this.$router.push({name: 'Search', query})
    }
  },
  mounted () {
    this.get(this.$route.params.id)
  },
  watch: {
    '$route' (to, from) {
      this.get(to.params.id)
    }
  },
  data () {
    return {
      dialog: false,
      item: {
        id: null
      }
    }
  }
}
</script>
