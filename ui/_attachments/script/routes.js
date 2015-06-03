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
