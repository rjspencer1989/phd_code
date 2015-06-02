App.Routers.Router = Backbone.Router.extend({
    initialize: function () {
        this.view = null;
        this.user_view = null;
    },

    display_user: function(){
        if (this.user_view === null) {
            this.user_view = new App.Views.User();
        }
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
        this.checkSession();
        if (this.view) {
            this.view.exit();
        }
        this.view = new App.Views.Home();
        showMenu();
    },

    login : function(){
        if (this.view) {
            this.view.exit();
        }
        this.view = new App.Views.Login();
        drawLogin();
    },

    wifi : function(){
        this.checkSession();
        if (this.view) {
            this.view.exit();
        }
        this.view = new App.Views.Wifi();
        showMenu();
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
            this.view.exit();
        }
        this.view = new App.Views.ControlPanelView();
        showMenu();
    },

    checkSession: function(){
        console.log('checking session');
        $.couch.session({
            success: function(data){
                console.log(data);
                if(data.userCtx.name !== null){
                    App.userCtx = data.userCtx;
                    App.routerInstance.display_user();
                }else{
                    App.routerInstance.navigate('login', {trigger: true});
                }
            }, error: function(data){
                console.log(data);
                App.routerInstance.navigate('login', {trigger: true});
            }
        });
    }
});
