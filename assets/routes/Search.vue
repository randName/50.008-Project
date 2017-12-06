<template>
<v-container fluid grid-list-sm>
  <v-select multiple dense chips clearable ref="select"
    autocomplete cache-items :search-input.sync="ensearch"
    :loading="loading" v-model="select" :items="items"
    label="Entities" placeholder="Search Entities..."
  >
    <template slot="selection" slot-scope="data">
      <v-chip :selected="data.selected" @input="data.parent.selectItem(data.item)">
        <v-avatar>
          <v-icon>{{ data.item.avatar }}</v-icon>
        </v-avatar>
        {{ data.item.text }}
      </v-chip>
    </template>
    <template slot="item" slot-scope="data">
      <v-list-tile-avatar>
        <v-icon>{{ data.item.avatar }}</v-icon>
      </v-list-tile-avatar>
      <v-list-tile-content>
        <v-list-tile-title>{{ data.item.text }}</v-list-tile-title>
      </v-list-tile-content>
    </template>
  </v-select>
  <v-text-field clearable
    v-model="namesearch"
    label="Search Names"
    @keyup.enter="dosearch"
  ></v-text-field>
  <v-layout row wrap>
    <SearchItem v-for="i in results" :key="i.id" :id="i.id" :name="i.name"/>
  </v-layout>
</v-container>
</template>

<script>
import SearchItem from '../components/SearchItem.vue'

export default {
  watch: {
    ensearch (val) {
      if (val && val.length >= 3) {
        const params = {q: val}
        this.loading = true;
        this.$nextTick(() => this.$http.get('/entities', {params})
          .then(r => {
            this.items = r.data.data.map(this.selectshow)
            this.loading = false
          }))
      }
    },
    select (val) {
      const q = {
        company: [],
        creator: [],
        category: []
      }
      val.forEach(i => {
        let [k, v] = i.split('-')
        q[k].push(v)
      })
      Object.keys(q).forEach(k => { q[k] = q[k].length ? q[k].join(',') : null })
      this.se = q
      this.dosearch()
    }
  },
  methods: {
    selectshow (e) {
      const ico = {
        creator: 'face',
        category: 'label',
        company: 'business'
      }
      return {
        text: e.name,
        avatar: ico[e.type],
        value: e.type+'-'+e.id
      }
    },
    dosearch () {
      let params = this.se
      params.name = this.namesearch
      if (Object.keys(params).every(i => !params[i])) return
      this.$nextTick(() => this.$http.get('/search', {params})
        .then(r => this.results = r.data.data))
    },
    make (t, e) {
      e.type = t
      const i = this.selectshow(e)
      this.items.push(i)
      this.$refs.select.selectItem(i)
    }
  },
  mounted () {
    if (this.$route.query.q) {
      this.namesearch = this.$route.query.q
    }
    ['company', 'creator', 'category'].forEach(k => {
      if (this.$route.query[k]) {
        const params = {type: k, id: this.$route.query[k]}
        this.$http.get('/entities', {params})
          .then(r => this.make(k, r.data.data))
      }
    })
  },
  components: {
    SearchItem
  },
  data () {
    return {
      se: {},
      items: [],
      select: [],
      results: [],
      ensearch: null,
      loading: false,
      namesearch: null
    }
  }
}
</script>
