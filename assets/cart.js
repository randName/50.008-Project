import Vue from 'vue'

import axios from 'axios'
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

export const CartManager = new Vue({
    computed: {
        size: {
            set (v) {},
            get () {
                return this.items.length
            }
        }
    },
    methods: {
        submit () {
            return axios.post('/order/submit', {order: this.items}).then(this.ordered)
        },
        ordered (response) {
            this.order = response.data.data
            this.items = []
        },
        update (response) {
            this.items = response.data.data
        },
        post (item, quantity) {
            const params = {
                quantity,
                id: item.id,
                name: item.name,
                price: item.price
            }
            return axios.post('/order/cart', params).then(this.update)
        },
        get () {
            this.order = {}
            return axios.get('/order/cart').then(this.update)
        }
    },
    data () {
        return {
            order: {},
            items: []
        }
    }
})
