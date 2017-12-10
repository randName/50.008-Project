<template>
<v-container fluid grid-list-lg>
  <v-layout row wrap>
    <v-flex v-if="item.id" xs12>
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
        </v-card-text>
        <v-card-actions>
          <v-chip color="green" text-color="white">
            ${{ item.price }}
          </v-chip>
          <v-chip color="primary" text-color="white">
            <v-avatar>
              <v-icon>store</v-icon>
            </v-avatar>
            {{ item.quantity }}
          </v-chip>
          <v-spacer></v-spacer>
          <v-dialog v-model="buy.dialog" :disabled="!item.quantity">
            <v-btn color="primary" slot="activator" :disabled="!item.quantity">
              {{ item.quantity ? 'Add to Cart' : 'Out of Stock' }}
            </v-btn>
            <v-card>
              <v-card-title>
                <div class="headline">Add to Cart</div>
              </v-card-title>
              <v-card-text>
                <v-layout row wrap>
                  <v-flex xs9>
                    <v-slider thumb-label
                     ticks step="1" min="1"
                     label="Quantity"
                     :max="item.quantity"
                     v-model="buy.quantity"
                    ></v-slider>
                  </v-flex>
                  <v-flex xs3>
                    <v-text-field v-model="buy.quantity" type="number"></v-text-field>
                  </v-flex>
                </v-layout>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="cart">Add</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-card-actions>
      </v-card>
    </v-flex>
    <v-progress-linear v-else
      :indeterminate="true"
    ></v-progress-linear>
    <v-flex xs12>
      <v-card>
        <v-card-title>
          <div class="headline">Feedback</div>
        </v-card-title>
        <v-card-text>
          <v-expansion-panel v-if="logged_in">
            <v-expansion-panel-content v-if="userFeedback.form">
              <div slot="header">Review this item</div>
              <v-form v-model="valid" ref="form" lazy-validation>
                <v-card>
                  <v-card-text>
                    <v-select required editable
                      :rules="[v=>!!v||'This is required']"
                      :items="scores" label="Score"
                      v-model="userFeedback.score"
                    ></v-select>
                    <v-text-field multi-line
                      label="Your Review (optional)"
                      v-model="userFeedback.review"
                    ></v-text-field>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="submitFB" :disabled="!valid">
                      Submit Feedback
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-form>
            </v-expansion-panel-content>
            <v-expansion-panel-content v-else>
              <div slot="header">
                Your Feedback
                <span class="caption">
                  on {{ userFeedback.made_on | moment("ll") }}
                </span>
              </div>
              <v-card>
                <v-card-text>
                  <v-layout row>
                    <v-flex xs1>
                      <span class="headline">
                        {{ userFeedback.score }}
                      </span>
                    </v-flex>
                    <v-flex xs8>{{ userFeedback.review }}</v-flex>
                    <v-flex xs3>
                      <span class="caption">
                        Usefulness: {{ uf(userFeedback.usefulness) }}
                      </span>
                    </v-flex>
                  </v-layout>
                </v-card-text>
              </v-card>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-btn v-else :to="{name: 'Login'}">
            Login to review this item
          </v-btn>
        </v-card-text>
        <v-list v-if="feedback.length > 0" two-line>
          <v-list-tile avatar v-for="f in feedback" :key="f.user.id">
            <v-list-tile-avatar>
              <span class="headline"> {{ f.score }}</span>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>
                {{ f.user.username }}
                <span class="caption">{{ f.made_on | moment("ll") }}</span>
              </v-list-tile-title>
              <v-list-tile-sub-title>{{ f.review }}</v-list-tile-sub-title>
            </v-list-tile-content>
            <v-list-tile-action>
              <v-list-tile-action-text>
                Usefulness: {{ uf(f.usefulness) }}
              </v-list-tile-action-text>
              <v-menu v-if="logged_in && !rated(f)" bottom offset-y>
                <v-icon slot="activator">thumbs_up_down</v-icon>
                <v-list>
                  <v-list-tile v-for="r in ratings" :key="r.value"
                    @click="rate(f.user.id, r.value)">
                    <v-list-tile-title>{{ r.text }}</v-list-tile-title>
                  </v-list-tile>
                </v-list>
              </v-menu>
            </v-list-tile-action>
          </v-list-tile>
        </v-list>
      </v-card>
    </v-flex>
  </v-layout>
  <v-layout v-if="recommends.length > 0" row wrap>
    <v-flex xs12>
      <v-card>
        <v-card-title primary-title>
          <div class="headline">Recommended Items</div>
        </v-card-title>
        <v-list two-line>
          <v-list-tile avatar v-for="f in recommends" :key="f.id">
            <v-list-tile-content>
              <v-list-tile-title>{{ f.name }}</v-list-tile-title>
              <v-list-tile-sub-title>
                {{ f.users }} bought this item
              </v-list-tile-sub-title>
            </v-list-tile-content>
            <v-list-tile-action>
              <v-list-tile-action-text>
                Sales: {{ f.sales }}
              </v-list-tile-action-text>
              <v-btn icon :to="{name: 'Item', params: {id: f.id}}">
                <v-icon>keyboard_arrow_right</v-icon>
              </v-btn>
            </v-list-tile-action>
          </v-list-tile>
        </v-list>
      </v-card>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
export default {
  computed: {
    logged_in () {
      return this.$user.user.is_authenticated
    }
  },
  methods: {
    get (id) {
      this.$http.get('/item/' + id)
      .then(r => this.item = r.data.data)
      .catch(e => this.$router.go(-1))
      this.$http.get('/recommends/' + id)
      .then(r => this.recommends = r.data.data)
      this.getFB(id)
    },
    getFB (id) {
      if (id === undefined) {
        id = this.item.id
      }
      this.$http.get('/feedback/'+id).then(r => this.loadFB(r.data))
    },
    loadFB (data) {
      const u = data.data.findIndex(f => f.user.id == this.$user.user.id)
      if ( u != -1 ) {
        this.userFeedback = data.data.splice(u, 1)[0]
      }
      this.feedback = data.data
    },
    submitFB () {
      if (this.$refs.form.validate()) {
        this.$http.post(`/feedback/${this.item.id}`, this.userFeedback)
          .then(r => this.loadFB(r.data))
      }
    },
    loadratings () {
      this.userRatings = this.$user.profile.ratings
        .filter(f => f.item.id == this.item.id)
        .map(f => f.user.id)
    },
    rated (f) {
      return (this.userRatings.indexOf(f.user.id) != -1)
    },
    uf (v) {
      return v ? parseInt(v).toFixed(1) : '-'
    },
    rate (u, v) {
      this.userRatings.push(u)
      this.$http.post(`/rate/${this.item.id}/${u}`, {usefulness: v})
        .then(() => this.getFB())
    },
    cart () {
      this.buy.dialog = false;
      this.$cart.post(this.item, this.buy.quantity)
    },
    search (query) {
      this.$router.push({name: 'Search', query})
    }
  },
  mounted () {
    this.get(this.$route.params.id)
    this.$user.getdetails().then(this.loadratings)
  },
  watch: {
    '$route' (to, from) {
      this.get(to.params.id)
    }
  },
  data () {
    return {
      scores: [...Array(11).keys()].map(i => ({text: ''+i, value: i})),
      ratings: [
        { value: 0, text: 'Useless' },
        { value: 1, text: 'Useful' },
        { value: 2, text: 'Very Useful' }
      ],
      userRatings: [],
      userFeedback: {
        form: true,
        score: null,
        review: ''
      },
      valid: true,
      recommends: [],
      feedback: [],
      buy: {
        quantity: 0,
        dialog: false
      },
      item: {
        id: null
      }
    }
  }
}
</script>
