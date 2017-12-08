import Vue from 'vue'

import axios from 'axios'
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

export const CartManager = new Vue({
    computed: {
        size () {
            return Object.keys(this.items).length
        }
    },
    methods: {
        update (response) {
            this.items = response.data.data
        },
        post (item_id, quantity) {
            return axios.post('/order/cart', {item_id, quantity}).then(this.update)
        },
        get () {
            return axios.get('/order/cart').then(this.update)
        }
    },
    data () {
        return {
            items: {}
        }
    }
})
