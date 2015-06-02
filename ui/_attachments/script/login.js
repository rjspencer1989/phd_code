App.Views.Login = Backbone.View.extend({
    tagName: "div",
    className: "col-md-12",
    template: window.JST.login,
    initialize: function(){
        App.userCtx = null;
        hideMenu();
        this.render();
    },

    events: {
        'submit #form-signin': 'login'
    },

    render: function(){
        this.$el.html(this.template());
        $('#main-row').html(this.el);
        return this;
    },

    login: function(e){
        e.preventDefault();
        console.log('login function');
        var user = $('#inputName').val();
        var password = $('#inputPassword').val();
        $.couch.login({
            name: user,
            password: password,
            success: function(data){
                App.routerInstance.navigate('/', {trigger: true});
            },
            error: function(data){
                alert('You could not be logged in');
            }
        });
    },

    exit: function(){
        this.remove();
    }
});

App.Views.User = Backbone.View.extend({
    el: '#user-id',
    template: window.JST.user_id,
    initialize: function(){
        this.render();
    },
    events:{
        'click #logout-link' : 'logout'
    },
    render: function(){
        this.$el.empty().append(this.template({name: App.userCtx.name}));
        return this;
    },

    logout: function(){
        this.remove();
        $.couch.logout({
            success: function(data){
                App.userCtx = null;
                console.log('logging out');
                App.routerInstance.navigate('login', {trigger: true});
            }
        });
    }
});
