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
            if ( ! this.loaded.includes(this.page) ) {
                if ( this.idx > 0 && this.items[this.idx-1] == undefined ) {
                    const start = Math.max(...this.loaded) * this.per_page
                    const arr = new Array(this.idx-start).fill(this.fill);
                    this.items.push(...arr)
                }
                const params = {
                    sort: this.sort,
                    page: this.page,
                    per_page: this.per_page
                }
                const delc = this.page < Math.max(...this.loaded) ? this.per_page : 0
                this.$http.get(this.url, {params}).then(r => this.load(r.data.data, delc))
            }
            return this.items.slice(this.idx, this.idx + this.per_page)
        }
    },
    methods: {
        load (data, delc) {
            this.items.splice(this.idx, delc, ...data)
            this.loaded.push(this.page)
        }
    },
    data () {
        return {
            url: '',
            page: 1,
            total: 0,
            sort: [],
            items: [],
            loaded: [],
            fill: null,
            per_page: 20
        }
    }
})
