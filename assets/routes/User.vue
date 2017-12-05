<template>
<v-container fluid grid-list-lg>
  <v-layout row wrap>
    <v-flex xs12>
      <v-card>
        <v-card-title primary-title>
          <div class="headline">Your Info</div>
        </v-card-title>
        <v-card-text>
          <v-container fluid>
            <v-layout row v-for="i in info" :key="i.label">
              <v-text-field
                :label="i.label"
                :value="i.value"
                :disabled="!i.editable"
              ></v-text-field>
            </v-layout>
          </v-container>
        </v-card-text>
      </v-card>
    </v-flex>
    <v-flex xs12>
      <v-card>
        <v-card-title primary-title>
          <div class="headline">Your Purchases</div>
        </v-card-title>
        <v-card-text>
          <v-list dense>
            <v-list-group no-action v-for="p in profile.orders" :key="p.id" >
              <v-list-tile avatar ripple slot="item">
                <v-list-tile-content>
                  <v-list-tile-title>{{ p.made_on | moment }}</v-list-tile-title>
                  <v-list-tile-sub-title>
                    {{ p.items | joins }}
                  </v-list-tile-sub-title>
                </v-list-tile-content>
                <v-list-tile-action>
                  <v-list-tile-action-text>${{ p.total }}</v-list-tile-action-text>
                  <v-icon>keyboard_arrow_down</v-icon>
                </v-list-tile-action>
              </v-list-tile>
              <v-list-tile v-for="i in p.items" :key="p.id+'-'+i.id">
                <v-list-tile-content>
                  <v-list-tile-title>{{ i.name }}</v-list-tile-title>
                </v-list-tile-content>
                <v-list-tile-action>
                  <v-list-tile-action-text>{{ i.quantity }}</v-list-tile-action-text>
                </v-list-tile-action>
              </v-list-tile>
              <v-divider></v-divider>
            </v-list-group>
          </v-list>
        </v-card-text>
      </v-card>
    </v-flex>
    <v-flex xs12>
      <v-card>
        <v-card-title primary-title>
          <div class="headline">Your Feedback</div>
        </v-card-title>
        <v-card-text>
          <v-list dense>
            <v-list-group no-action v-for="f in profile.feedbacks" :key="f.item.id" >
              <v-list-tile avatar ripple slot="item">
                <v-list-tile-content>
                  <v-list-tile-title>{{ f.item.name }}</v-list-tile-title>
                  <v-list-tile-sub-title>
                    {{ f.made_on | moment }}
                  </v-list-tile-sub-title>
                </v-list-tile-content>
                <v-list-tile-action>
                  <v-list-tile-action-text>
                    Score: {{ f.score }}
                  </v-list-tile-action-text>
                  <v-icon>keyboard_arrow_down</v-icon>
                </v-list-tile-action>
              </v-list-tile>
              <v-list-tile @click="">
                <v-list-tile-content>
                  <v-list-tile-title>{{ f.review }}</v-list-tile-title>
                </v-list-tile-content>
              </v-list-tile>
              <v-divider></v-divider>
            </v-list-group>
          </v-list>
        </v-card-text>
      </v-card>
    </v-flex>
    <v-flex xs12>
      <v-card>
        <v-card-title primary-title>
          <div class="headline">Your Ratings</div>
        </v-card-title>
        <v-card-text>
          <v-list dense>
            <v-list-group no-action v-for="r in profile.ratings" :key="r.item.id" >
              <v-list-tile avatar ripple slot="item">
                <v-list-tile-content>
                  <v-list-tile-title>{{ r.item.name }}</v-list-tile-title>
                  <v-list-tile-sub-title>
                    By {{ r.user.username }} on {{ r.made_on | moment }}
                  </v-list-tile-sub-title>
                </v-list-tile-content>
                <v-list-tile-action>
                  <v-list-tile-action-text>Rating: {{ r.usefulness }}</v-list-tile-action-text>
                  <v-icon>keyboard_arrow_down</v-icon>
                </v-list-tile-action>
              </v-list-tile>
              <v-list-tile @click="">
                <v-list-tile-content>
                  <v-list-tile-title>{{ r.review }}</v-list-tile-title>
                </v-list-tile-content>
                <v-list-tile-action>
                  <v-list-tile-action-text>
                    Score: {{ r.score }}
                  </v-list-tile-action-text>
                </v-list-tile-action>
              </v-list-tile>
              <v-divider></v-divider>
            </v-list-group>
          </v-list>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
export default {
  computed: {
    profile () {
      return this.$user.profile
    }
  },
  mounted () {
    if (!this.$user.user.is_authenticated) {
      this.$router.replace('/')
    }
    this.$user.getdetails()
  },
  data () {
    let user = this.$user.user
    return {
      info: [
        {
          editable: true,
          label: 'First Name',
          value: user.first_name
        },
        {
          editable: true,
          label: 'Last Name',
          value: user.last_name
        },
        {
          editable: true,
          label: 'Email',
          value: user.email
        },
        {
          editable: false,
          label: 'Joined',
          value: user.date_joined
        }
      ]
    }
  }
}
</script>
