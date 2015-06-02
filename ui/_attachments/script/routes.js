App.Routers.Router = Backbone.Router.extend({
    initialize: function () {
        this.view = null;
    },

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
        this.checkSession();
        if (this.view) {
            this.view.remove();
        }
        this.view = new App.Views.ControlPanelView();
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
