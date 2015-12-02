Router = Marionette.AppRouter.extend({
    controller: {
        home: function(){
            "use strict";
            RouterConfigApp.root.main.show(new Home());
        },

        wifi: function(){
            "use strict";
            console.log('rofl');
            var collection = new RouterConfigApp.Collections.Wifi();
            collection.fetch({reset: true});
            RouterConfigApp.root.main.show(new WiFi({collection: collection}));
        },
    
        history: function(){
            "use strict";
            var collection = new RouterConfigApp.Collections.Events();
            collection.fetch({reset: true, descending: true});
            RouterConfigApp.root.main.show(new Events({collection: collection}));
        },
    
        notifications: function(){
            "use strict";
            console.log('foobar');
            var collection = new RouterConfigApp.Collections.Notifications();
            collection.fetch({reset: true});
            RouterConfigApp.root.main.show(new Notifications({collection: collection}));
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
