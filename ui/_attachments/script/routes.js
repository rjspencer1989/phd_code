App.Routers.Router = Backbone.Router.extend({
    initialize: function () {
        this.view = null;
        this.user_view = null;
        if (App.userCtx.name === null) {
            this.navigate('login', {trigger: true});
        }
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
    },

    wifi : function(){
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
        if (this.view) {
            this.view.exit();
        }
        this.view = new App.Views.ControlPanelView();
        showMenu();
    }
});
