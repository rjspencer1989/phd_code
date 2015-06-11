App.Routers.Router = Backbone.Router.extend({
    initialize: function () {
        this.view = null;
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
    },

    wifi : function(){
        if (this.view) {
            this.view.exit();
        }
        this.view = new App.Views.Wifi();
    },

    history : function(){
        if (this.view) {
            this.view.exit();
        }
        this.view = new App.Views.Events();
    },

    notifications : function(){
        if (this.view) {
            this.view.exit();
        }
        this.view = new App.Views.Notifications();
    },

    controlPanel : function(){
        if (this.view) {
            this.view.exit();
        }
        this.view = new App.Views.ControlPanelView();
    }
});
