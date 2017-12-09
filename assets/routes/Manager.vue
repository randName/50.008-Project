<template>
<v-container fluid grid-list-lg>
  <v-layout row wrap>
    <v-flex xs12>
      <v-card>
        <v-card-title primary-title>
          <div class="headline">Most Popular</div>
        </v-card-title>
        <v-card-text>
          <v-select label="Type" :items="entities" v-model="etype"></v-select>
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
            <v-list-tile v-for="i in popular">
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
    date (val) {
      this.gettop()
    },
    etype (val) {
      this.gettop()
    }
  },
  methods: {
    gettop () {
      if (this.date === null || this.etype === null) return
      const [year, month] = this.date.split('-')
      this.$http.get(`/admin/stats/${this.etype}/${year}/${month}`)
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
      date: null,
      etype: null,
      modal: false,
      popular: [],
      entities: [
        {text: 'Items', value: 'item'},
        {text: 'Creators', value: 'creator'},
        {text: 'Companies', value: 'company'}
      ]
    }
  }
}
</script>
