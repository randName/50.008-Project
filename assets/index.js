import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.css'
import VueRouter from 'vue-router'

import axios from 'axios'
Vue.prototype.$http = axios.create({
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken'
})

import {UserManager} from './user'
Vue.prototype.$user = UserManager

import App from './App.vue'
import Shop from './routes/Shop.vue'
import Cart from './routes/Cart.vue'
import User from './routes/User.vue'
import Login from './routes/Login.vue'
import Manager from './routes/Manager.vue'

export const routes = [
    { path: '/shop', name: 'Shop', component: Shop },
    { path: '/cart', name: 'Cart', component: Cart },
    { path: '/user', name: 'Profile', component: User },
    { path: '/login', name: 'Login', component: Login },
    { path: '/manager', name: 'Manager', component: Manager },
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
