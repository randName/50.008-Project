var options = {
  el: '#app',
  delimiters: ['[', ']'],
  data: {
    'drawer': false,
    'usergp': {
      'active': false,
      'list': []
    },
    'routes': [
      {
        'path': '/store',
        'title': 'Store',
        'action': 'store'
      },
      {
        'path': '/cart',
        'title': 'Cart',
        'action': 'shopping_cart'
      }
    ]
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
    }
  }
};
