window.App.Routers.Router = Backbone.Router.extend({
    initialize: function () {
        "use strict";
        this.view = null;
    },

    routes: {
        "": "home",
        "wifi": "wifi",
        "history": "history",
        "notifications": "notifications",
        "control": "controlPanel"
    },

    home: function(){
        "use strict";
        if (this.view) {
            this.view.exit();
        }
        this.view = new window.App.Views.Home();
    },

    wifi: function(){
        "use strict";
        if (this.view) {
            this.view.exit();
        }
        this.view = new window.App.Views.Wifi();
    },

    history: function(){
        "use strict";
        if (this.view) {
            this.view.exit();
        }
        this.view = new window.App.Views.Events();
    },

    notifications: function(){
        "use strict";
        if (this.view) {
            this.view.exit();
        }
        this.view = new window.App.Views.Notifications();
    },

    controlPanel: function(){
        "use strict";
        if (this.view) {
            this.view.exit();
        }
        this.view = new window.App.Views.ControlPanelView();
    }
});
