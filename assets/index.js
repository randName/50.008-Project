import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.css'
import VueRouter from 'vue-router'

import axios from 'axios'
Vue.prototype.$http = axios.create({
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken'
})

import App from './App.vue'
import Shop from './components/Shop.vue'
import Cart from './components/Cart.vue'

export const routes = [
  { path: '/shop', name: 'Shop', component: Shop },
  { path: '/cart', name: 'Cart', component: Cart },
  { path: '*', redirect: '/shop' }
]
const router = new VueRouter({routes})

Vue.use(Vuetify)
Vue.use(VueRouter)

new Vue({
    el: '#app',
    router,
    render: h => h(App)
})
