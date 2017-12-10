import qs from 'qs'
import Vue from 'vue'

import axios from 'axios'
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

export const UserManager = new Vue({
    methods: {
        update (response) {
            this.user = response.data.data
        },
        get () {
            if (this.user.id !== undefined) {
                return Promise.resolve(this.user)
            }
            return axios.get('/user/details').then(this.update)
        },
        getdetails () {
            if (!this.user.is_authenticated) {
                return Promise.resolve(null)
            }
            let details = ['orders', 'ratings', 'feedbacks']
            return axios.all(details.map(
                d => axios.get('/user/' + d)
                     .then(r => this.profile[d] = r.data.data)
            ))
        },
        login (form, register) {
            if ( register ) {
                form = {
                    username: form.username,
                    password1: form.password,
                    password2: form.password2,
                }
            } else {
                form = {
                    username: form.username,
                    password: form.password,
                }
            }
            return axios.post('/user/login', qs.stringify(form)).then(this.update)
        },
        logout () {
            return axios.get('/logout/').then(this.get)
        }
    },
    data () {
        return {
            profile: {
                orders: [],
                ratings: [],
                feedbacks: []
            },
            user: {}
        }
    }
})
