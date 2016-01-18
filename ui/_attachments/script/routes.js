var Router = Marionette.AppRouter.extend({
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
            var collection = new RouterConfigApp.Collections.Events();
            collection.fetch({reset: true, descending: true});
            RouterConfigApp.root.main.show(new Events({collection: collection}));
        },
    
        notifications: function(){
            "use strict";
            var notificationCollection = new RouterConfigApp.Collections.Notifications();
            notificationCollection.fetch({reset: true});
            var userCollection = new RouterConfigApp.Collections.MainUser();
            userCollection.fetch({reset: true});
            var notificationLayout = new NotificationLayout();
            RouterConfigApp.root.main.show(notificationLayout);
            notificationLayout.notification_region.show(new Notifications({collection: notificationCollection}));
            notificationLayout.main_user_region.show(new MainUserCollection({collection: userCollection}));
        },
    
        controlPanel: function(){
            "use strict";
            console.log("application control panel view");
            var collection = new RouterConfigApp.Collections.Devices();
            collection.fetch({reset: true});
            RouterConfigApp.root.main.show(new Devices({collection: collection}));
        }   
    },

    appRoutes: {
        "home": "home",
        "": "home",
        "wifi": "wifi",
        "history": "history",
        "notifications": "notifications",
        "devices": "controlPanel"
    }
});
