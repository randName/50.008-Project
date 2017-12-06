<template>
<v-toolbar app fixed flat ref="toolbar" :manual-scroll="!searching">
  <v-btn icon large @click="nosearch">
    <v-icon>arrow_back</v-icon>
  </v-btn>
  <v-text-field clearable single-line solo light
    id="search" key="search" ref="search" v-model="search"
    placeholder="Search" prepend-icon="search" @keyup.enter="dosearch"
  ></v-text-field>
  <v-menu offset-y v-model="showsearch" activator="#search">
    <v-list light dense>
      <v-list-tile v-for="i in suggestions" :key="i.type+i.id" @click="dosearch(i)">
        <v-list-tile-avatar>
          <v-icon color="black">{{ icons[i.type] }}</v-icon>
        </v-list-tile-avatar>
        <v-list-tile-content>
          <v-list-tile-title>{{ i.name }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
  </v-menu>
</v-toolbar>
</template>

<script>
export default {
  props: ['searching'],
  computed: {
    showsearch: {
      get () {
        return this.searching && this.suggestions.length > 0
      },
      set (v) {
        if (!v) {
          this.nosearch()
        }
      }
    },
  },
  watch: {
    searching (val) {
      this.$refs.toolbar.isScrolling = !val
      if (val) {
        this.$nextTick(() => this.$refs.search.focus())
      } else {
        this.search = null
        this.suggestions = []
      }
    },
    search (val) {
      if (val && val.length >= 3) {
        const params = {q: val}
        this.$nextTick(() => this.$http.get('/entities', {params})
          .then(r => this.suggestions = r.data.data))
      } else {
        this.$nextTick(() => this.suggestions = [])
      }
    },
  },
  methods: {
    nosearch () {
      this.$emit('nosearch')
    },
    dosearch (entity) {
      let query = {}
      if (entity.name) {
        query[entity.type] = entity.id
      } else if (this.search) {
        query = {q: this.search}
      }
      if (Object.keys(query).length) {
        this.nosearch()
        this.$router.push({name: 'Search', query})
      }
    }
  },
  data () {
    return {
      icons: {
        creator: 'face',
        category: 'label',
        company: 'business'
      },
      search: null,
      suggestions: [],
    }
  }
}
</script>
