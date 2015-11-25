window.App.Views.WifiHome = Backbone.View.extend({
    collection: new window.App.Collections.WifiHome(),
    el: "#home-wifi-config",
    template: window.JST.home_wifi,
    initialize: function () {
        "use strict";
        this.listenTo(this.collection, "reset", this.render);
        this.listenTo(this.collection, "change", this.render);
        this.collection.fetch({
            reset: true
        });
    },

    render: function () {
        "use strict";
        this.$el.empty().append(this.template(this.collection.at(0).toJSON()));
        return this;
    }
});

window.App.Views.NotificationHome = Backbone.View.extend({
    tagName: "tr",
    template: window.JST.home_notification,
    render: function(){
        "use strict";
        this.$el.empty().append(this.template(this.model.toJSON()));
        return this;
    }
});

window.App.Views.NotificationsHome = Backbone.View.extend({
    el: "#home-notifications",
    template: window.JST.home_notifications,
    collection: new App.Collections.Notifications(),
    initialize: function(){
        "use strict";
        this.listenTo(this.collection, "reset", this.render);
        this.listenTo(this.collection, "change", this.render);
        this.subviews = [];
        this.collection.fetch({
            reset: true
        });
    },
    
    addOne: function(notification){
        "use strict";
        var view = new window.App.Views.NotificationHome({model: notification});
        this.subviews.push(view);
        this.$("tbody").append(view.render().el);
    },

    render: function () {
        "use strict";
        this.$el.empty().append(this.template());
        this.collection.each(this.addOne, this);
        return this;
    },

    exit: function(){
        "use strict";
        for (var index in this.subviews) {
            this.subviews[index].remove();
        }
        this.remove();
    }
});

window.App.Views.DeviceHome = Backbone.View.extend({
    tagName: "tr",
    template: window.JST.home_device,
    render: function(){
        "use strict";
        this.$el.empty().append(this.template(this.model.toJSON()));
        return this;
    }
});

window.App.Views.ConnectedDevicesHome = Backbone.View.extend({
    el: "#home-devices",
    template: window.JST.home_devices,
    collection: new window.App.Collections.ConnectedDevices(),
    initialize: function () {
        "use strict";
        this.listenTo(this.collection, "reset", this.render);
        this.listenTo(this.collection, "change", this.render);
        this.subviews = [];
        this.collection.fetch({
            reset: true
        });
    },

    addOne: function(device){
        "use strict";
        var view = new window.App.Views.DeviceHome({model: device});
        this.subviews.push(view);
        this.$("tbody").append(view.render().el);
    },

    render: function () {
        "use strict";
        this.$el.empty().append(this.template());
        this.collection.each(this.addOne, this);
        return this;
    },

    exit: function(){
        "use strict";
        for (var index in this.subviews) {
            this.subviews[index].remove();
        }
        this.remove();
    }
});

window.App.Views.Home = Backbone.View.extend({
    tagName: "div",
    className: "col-md-12",
    template: window.JST.home,
    initialize: function () {
        "use strict";
        this.render();
        this.wifi_view = new window.App.Views.WifiHome();
        this.devices_view = new window.App.Views.ConnectedDevicesHome();
        this.notifications_view = new window.App.Views.NotificationsHome();
    },

    render: function () {
        "use strict";
        this.$el.empty().append(this.template());
        $("#main-row").html(this.el);
        window.setActiveLink("home-link");
    },

    exit: function(){
        "use strict";
        this.wifi_view.remove();
        this.devices_view.exit();
        this.notifications_view.exit();
        this.remove();
    }
});
