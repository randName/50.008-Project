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
            return axios.get('/user/details').then(this.update)
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
            user: {}
        }
    }
})
