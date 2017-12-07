import Vue from 'vue'
import axios from 'axios'

export const Paginator = new Vue({
    computed: {
        pages () {
            return this.total ? Math.ceil(this.total/this.per_page) : 2
        },
        idx () {
            return (this.page - 1) * this.per_page
        },
        view () {
            if ( this.url === null ) return []
            if ( ! this.loaded.includes(this.page) ) {
                if ( this.idx > 0 && this.items[this.idx-1] == undefined ) {
                    const start = Math.max(...this.loaded) * this.per_page
                    const arr = new Array(this.idx-start).fill({});
                    this.items.push(...arr)
                }
                const params = Object.assign({}, this.params, {
                    sort: this.sort.join(','),
                    page: this.page,
                    per_page: this.per_page
                })
                const delc = this.page < Math.max(...this.loaded) ? this.per_page : 0
                this.$http.get(this.url, {params}).then(r => this.load(r.data, delc))
            }
            return this.items.slice(this.idx, this.idx + this.per_page)
        }
    },
    methods: {
        set (url, params, sort) {
            this.url = url
            if (params) {
                this.params = params
                if (sort) {
                    this.sort = sort
                }
            }
            this.page = 1
            this.total = 0
            this.items = []
            this.loaded = []
        },
        load (data, delc) {
            this.total = data.meta.total
            this.items.splice(this.idx, delc, ...data.data)
            this.loaded.push(this.page)
        }
    },
    data () {
        return {
            url: null,
            page: 1,
            total: 0,
            sort: [],
            items: [],
            loaded: [],
            params: {},
            visible: 6,
            per_page: 20
        }
    }
})
