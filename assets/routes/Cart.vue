<template>
<v-container>
  <v-card>
    <v-card-title primary-title>
      <div class="headline">Your Cart</div>
    </v-card-title>
    <v-data-table hide-actions select-all
      v-model="selected"
      :headers="headers"
      :items="items"
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
      <v-btn :disabled="$cart.size == 0" @click="submit">Submit Order</v-btn>
    </v-card-actions>
  </v-card>
</v-container>
</template>

<script>
export default {
  computed: {
    total () {
      const c = this.items.reduce((i, v) => i + v.quantity*v.price, 0)
      return c ? c.toFixed(2) : '0.00'
    },
    items () {
      return Object.values(this.$cart.items)
    }
  },
  methods: {
    submit () {
      this.$cart.submit()
    }
  },
  data () {
    return {
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
