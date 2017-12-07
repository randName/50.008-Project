import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.css'
import VueRouter from 'vue-router'

Vue.use(Vuetify)
Vue.use(VueRouter)

// Axios
import axios from 'axios'
Vue.prototype.$http = axios.create({
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken'
})

// User Manager
import {UserManager} from './user'
Vue.prototype.$user = UserManager

// Routes
import App from './App.vue'
import Shop from './routes/Shop.vue'
import Item from './routes/Item.vue'
import Cart from './routes/Cart.vue'
import User from './routes/User.vue'
import Login from './routes/Login.vue'
import Search from './routes/Search.vue'
import Manager from './routes/Manager.vue'

export const routes = [
    { path: '/shop', name: 'Shop', component: Shop },
    { path: '/cart', name: 'Cart', component: Cart },
    { path: '/user', name: 'Profile', component: User },
    { path: '/login', name: 'Login', component: Login },
    { path: '/item/:id', name: 'Item', component: Item },
    { path: '/search', name: 'Search', component: Search },
    { path: '/manager', name: 'Manager', component: Manager },
    { path: '*', redirect: '/shop' }
]
const router = new VueRouter({
    routes,
    scrollBehavior (to, from, savedPosition) {
        return { x: 0, y: 0 }
    }
})

// Filters
Vue.filter('joins', (a, prop='name', sep='; ') => a.map(i => i[prop]).join(sep));

import moment from 'moment'
Vue.filter('moment', (date, format='YYYY/MM/DD hh:mm a') => moment(date).format(format));

new Vue({
    el: '#app',
    router,
    render: h => h(App)
})
