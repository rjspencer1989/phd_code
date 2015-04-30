App.Routers.Router = Backbone.Router.extend({
    routes : {
        '' : 'home',
        'login' : 'login',
        'wifi' : 'wifi',
        'history': 'history',
        'notifications' : 'notifications',
        'control' : 'controlPanel'
    },

    home : function(){
        drawHome();
    },

    login : function(){
        drawLogin();
    },

    wifi : function(){
        drawWifi();
    },

    history : function(){
        drawHistory();
    },

    notifications : function(){
        drawNotifications();
    },

    controlPanel : function(){
        drawControlPanel();
    },

    checkSession: function(){
        console.log('checking session');
        $.couch.session({
            success: function(data){
                console.log(data);
                if(data.userCtx.name !== null){
                    App.userCtx = data.userCtx;
                    showMenu();
                    new App.Views.User();
                }else{
                    App.routerInstance.navigate('login', true);
                }
            }, error: function(data){
                console.log(data);
                App.routerInstance.navigate('login', true);
            }
        });
    }
});
