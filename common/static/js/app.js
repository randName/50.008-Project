var app = new Vue({
  el: '#app',
  delimiters: ['[', ']'],
  data: {
    'drawer': false,
    'forms': {},
    'page': '',
    'ajax': ''
  },
  methods: {
    loadJSON: function(url, success, error){
      console.log(url);
      this.ajax = 'loading...';
      axios.get(url).then(function(response){
        app.ajax = 'done';
        console.log(response);
        if (success) success(response);
      }).catch(function(e){
        app.ajax = 'error';
        console.log(e);
        if (error) error(e);
      });
    },
    href: function(url){
      window.location = url;
    }
  }
});
