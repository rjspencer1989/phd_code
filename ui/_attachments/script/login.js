App.Views.Login = Backbone.View.extend({
    el : '#main-content',
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
        this.$el.empty().append(this.template());
    },

    login: function(e){
        e.preventDefault();
        var user = $('#inputName').val();
        var password = $('#inputPassword').val();
        $.couch.login({
            name: user,
            password: password,
            success: function(data){
                App.routerInstance.navigate('/', true);
            },
            error: function(data){
                alert('You could not be logged in');
            }
        });
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
        the_view = this;
        $.couch.logout({
            success: function(data){
                App.userCtx = null;
                console.log('logging out');
                the_view.remove();
                App.routerInstance.navigate('login', true);
            }
        });
    }
});

function drawLogin(){
    $.couch.session({
        success: function(data){
            if(data.userCtx.name !== null){
                App.routerInstance.navigate('/', true);
            } else{
                App.routerInstance.navigate('login', true);
            }
        }, error: function(data){
            App.routerInstance.navigate('login', true);
        }
    });
}
