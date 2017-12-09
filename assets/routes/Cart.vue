<template>
<v-container>
  <v-card>
    <v-card-title primary-title>
      <div class="headline">Your Cart</div>
    </v-card-title>
    <v-data-table hide-actions select-all
      v-model="selected"
      :headers="headers"
      :items="$cart.items"
    >
      <template slot="items" slot-scope="props">
        <td><v-checkbox primary hide-details v-model="props.selected"></v-checkbox></td>
        <td>{{ props.item.name }}</td>
        <td class="text-xs-right">${{ props.item.price }}</td>
        <td class="text-xs-right">{{ props.item.quantity }}</td>
      </template>
      <template slot="no-data">Your cart is empty :c</template>
    </v-data-table>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-chip color="green" text-color="white">
        Total: ${{ total }}
      </v-chip>
      <v-dialog v-if="$user.user.is_authenticated"
        v-model="dialog.open" :disabled="!$cart.size"
      >
        <v-btn color="primary" slot="activator" :disabled="!$cart.size">
          Submit Order
        </v-btn>
        <v-card>
          <v-card-title>
            <div class="headline">
              {{ dialog.done ? 'Order Complete' : 'Confirm Order' }}
            </div>
          </v-card-title>
          <v-card-text v-if="dialog.done">
            Thank you for your order!
          </v-card-text>
          <v-card-text v-else>
            Total: ${{ total }}
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn v-if="dialog.done" :to="{name: 'Shop'}">OK</v-btn>
            <template v-else>
              <v-btn @click.native="dialog.open=false">No</v-btn>
              <v-btn color="primary" @click="submit"
                :disabled="dialog.loading"
                :loading="dialog.loading"
              >Yes</v-btn>
            </template>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-btn v-else :to="{name: 'Login'}">Login</v-btn>
    </v-card-actions>
  </v-card>
</v-container>
</template>

<script>
export default {
  computed: {
    total () {
      const c = this.$cart.items.reduce((i, v) => i + v.quantity*v.price, 0)
      return c ? c.toFixed(2) : '0.00'
    },
  },
  methods: {
    submit () {
      this.dialog.loading = true
      this.$cart.submit().then(() => {
        this.dialog.loading = false
        this.dialog.done = true
      })
      .catch(e => console.log(e.response))
    }
  },
  data () {
    return {
      dialog: {
        loading: false,
        done: false,
        open: false
      },
      selected: [],
      headers: [
        {text: 'Name', value: 'name', align: 'left'},
        {text: 'Price', value: 'price'},
        {text: 'Quantity', value: 'quantity'}
      ]
    }
  }
}
</script>
