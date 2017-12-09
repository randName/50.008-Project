<template>
<v-container fluid grid-list-lg>
  <v-layout row wrap>
    <v-flex xs12>
      <v-card>
        <v-card-title primary-title>
          <div class="headline">Inventory Management</div>
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-dialog v-model="newitem.dialog" persistent>
            <v-btn slot="activator">New Item</v-btn>
            <v-card>
              <v-card-title>
                <div class="headline">New Item</div>
              </v-card-title>
              <v-card-text>
                <v-text-field v-model="newitem.item.name" label="Name"></v-text-field>
                <v-text-field multi-line
                  v-model="newitem.item.description"
                  label="Description"
                ></v-text-field>
                <v-dialog persistent lazy full-width
                  v-model="newitem.modal" width="290px"
                >
                  <v-text-field readonly
                    slot="activator" v-model="newitem.item.date"
                    label="Date Created" prepend-icon="event"
                  ></v-text-field>
                  <v-date-picker scrollable actions v-model="newitem.item.date">
                    <template slot-scope="{ save, cancel }">
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn flat @click="cancel">Cancel</v-btn>
                        <v-btn flat color="primary" @click="save">OK</v-btn>
                      </v-card-actions>
                    </template>
                  </v-date-picker>
                </v-dialog>
                <v-select dense clearable autocomplete cache-items
                  :search-input.sync="newitem.company.search"
                  :loading="newitem.company.loading"
                  placeholder="Search for company"
                  v-model="newitem.item.company"
                  :items="newitem.company.list"
                  label="Company"
                ></v-select>
                <v-select multiple chips dense clearable
                  autocomplete cache-items
                  :search-input.sync="newitem.creator.search"
                  :loading="newitem.creator.loading"
                  placeholder="Search for creator"
                  v-model="newitem.item.creator"
                  :items="newitem.creator.list"
                  label="Creators"
                ></v-select>
                <v-select multiple chips dense clearable
                  autocomplete cache-items
                  :search-input.sync="newitem.category.search"
                  :loading="newitem.category.loading"
                  placeholder="Search for category"
                  v-model="newitem.item.category"
                  :items="newitem.category.list"
                  label="Categories"
                ></v-select>
                <v-text-field type="number" step="0.01" min="0"
                  v-model="newitem.item.price"
                  label="Price"
                ></v-text-field>
                <v-text-field type="number" min="0"
                  v-model="newitem.item.quantity"
                  label="Current Stock"
                ></v-text-field>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="newitem.dialog=false">Cancel</v-btn>
                <v-btn color="primary" @click="addnew">Add</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="stock.dialog" persistent>
            <v-btn slot="activator">Update stock</v-btn>
            <v-card>
              <v-card-title>
                <div class="headline">Update Stock</div>
              </v-card-title>
              <v-card-text>
                <v-select dense clearable autocomplete cache-items
                  :search-input.sync="stock.search"
                  placeholder="Search for item"
                  :loading="stock.loading"
                  :items="stock.items"
                  v-model="stock.id"
                  label="Item"
                ></v-select>
                <v-text-field type="number" min="0"
                  v-model="stock.item.quantity"
                  label="Stock"
                ></v-text-field>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="stock.dialog=false">Cancel</v-btn>
                <v-btn color="primary" @click="stockupdate">Update</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
  <v-layout row wrap>
    <v-flex xs12>
      <v-card>
        <v-card-title primary-title>
          <div class="headline">Most Popular</div>
        </v-card-title>
        <v-card-text>
          <v-layout row>
            <v-flex xs8>
              <v-select label="Type" :items="entities" v-model="etype"></v-select>
            </v-flex>
            <v-flex xs4>
              <v-text-field type="number" min="0"
                v-model="topnum"
                label="Count"
              ></v-text-field>
            </v-flex>
          </v-layout>
          <v-dialog persistent lazy full-width v-model="modal" width="290px">
            <v-text-field readonly
              slot="activator" v-model="date"
              label="Month" prepend-icon="event"
            ></v-text-field>
            <v-date-picker type="month" v-model="date" scrollable actions>
              <template slot-scope="{ save, cancel }">
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn flat @click="cancel">Cancel</v-btn>
                  <v-btn flat color="primary" @click="save">OK</v-btn>
                </v-card-actions>
              </template>
            </v-date-picker>
          </v-dialog>
          <v-list v-if="popular.length">
            <v-list-tile v-for="i in popular" :key="i[etype].id">
              <v-list-tile-content>
                <v-list-tile-title>
                  {{ i[etype].name }}
                </v-list-tile-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-list-tile-action-text>
                  Sales: {{ i.total }}
                </v-list-tile-action-text>
              </v-list-tile-action>
            </v-list-tile>
          </v-list>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
export default {
  watch: {
    'stock.search' (val) {
      if (val && val.length >= 3) {
        const params = {name: val}
        this.stock.loading = true
        this.$nextTick(() => this.$http.get('/search', {params})
          .then(r => {
            this.stock.items = r.data.data.map(e => ({text: e.name, value: e.id}))
            this.stock.loading = false
        }))
      }
    },
    'stock.id' (val) {
      this.$http.get('/admin/stock/' + val)
      .then(r => this.stock.item = r.data.data)
      .catch(r => this.stock.item = {quantity: null})
    },
    'newitem.company.search' (val) {
      this.searchentity('company', val)
    },
    'newitem.creator.search' (val) {
      this.searchentity('creator', val)
    },
    'newitem.category.search' (val) {
      this.searchentity('category', val)
    },
    topnum (val) {
      this.gettop()
    },
    date (val) {
      this.gettop()
    },
    etype (val) {
      this.gettop()
    }
  },
  methods: {
    stockupdate () {
      this.$http.post('/admin/stock/' + this.stock.id, this.stock.item)
      .then(r => {
        this.stock.dialog = false
        this.stock.id = null
      })
    },
    searchentity (entity, val) {
      if (val && val.length >= 3) {
        const params = {q: val, type: entity}
        this.newitem[entity].loading = true
        this.$nextTick(() => this.$http.get('/entities', {params})
          .then(r => {
            this.newitem[entity].list = r.data.data.map(e=>({text: e.name, value: e.id}))
            this.newitem[entity].loading = false
        }))
      }
    },
    addnew () {
      this.$http.post('/admin/new', this.newitem.item)
      .then(r => {
        this.newitem.dialog = false
        this.newitem.item = {
          name: null,
          price: null,
          creator: [],
          category: [],
          company: null,
          quantity: null,
          description: ''
        }
      })
    },
    gettop () {
      if (this.date === null || this.etype === null) return
      const [year, month] = this.date.split('-')
      const params = {per_page: this.topnum}
      this.$http.get(`/admin/stats/${this.etype}/${year}/${month}`, {params})
      .then(r => this.popular = r.data.data)
    }
  },
  mounted () {
    if (!this.$user.user.is_staff) {
      this.$router.replace('/')
    }
  },
  data () {
    return {
      topnum: 10,
      date: null,
      etype: null,
      modal: false,
      popular: [],
      stock: {
        item: {
          quantity: null
        },
        id: null,
        items: [],
        search: null,
        dialog: false,
        loading: false
      },
      newitem: {
        item: {
          name: null,
          date: null,
          price: null,
          creator: [],
          category: [],
          company: null,
          quantity: null,
          description: ''
        },
        company: {
          list: [],
          search: null,
          loading: false
        },
        creator: {
          list: [],
          search: null,
          loading: false
        },
        category: {
          list: [],
          search: null,
          loading: false
        },
        modal: false,
        dialog: false
      },
      entities: [
        {text: 'Items', value: 'item'},
        {text: 'Creators', value: 'creator'},
        {text: 'Companies', value: 'company'}
      ]
    }
  }
}
</script>
