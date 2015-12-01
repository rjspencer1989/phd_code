Router = Marionette.AppRouter.extend({
    controller: {
        home: function(){
            "use strict";
            RouterConfigApp.root.main.show(new Home());
        },

        wifi: function(){
            "use strict";
            var collection = new RouterConfigApp.Collections.Wifi();
            collection.fetch({reset: true});
            RouterConfigApp.root.main.show(new WiFi({collection: collection}));
        },
    
        history: function(){
            "use strict";
            RouterConfigApp.root.main.show(new History());
        },
    
        notifications: function(){
            "use strict";
            RouterConfigApp.root.main.show(new Notifications());
        },
    
        controlPanel: function(){
            "use strict";
            RouterConfigApp.root.main.show(new Devices());
        }   
    },

    appRoutes: {
        "home": "home",
        "": "home",
        "wifi": "wifi",
        "history": "history",
        "notifications": "notifications",
        "control": "controlPanel"
    }
});
