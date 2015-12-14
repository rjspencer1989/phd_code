var HomeWifi = Marionette.ItemView.extend({
    template: window.JST.home_wifi
});

var HomeWifiCollection = Marionette.CollectionView.extend({
    childView: HomeWifi
});

var HomeNotification = Marionette.ItemView.extend({
    tagName: 'tr',
    template: window.JST.home_notification
});

var HomeNotifications = Marionette.CompositeView.extend({
    template: window.JST.home_notifications,
    childViewContainer: 'tbody',
    childView: HomeNotification
});

var HomeDevice = Marionette.ItemView.extend({
    tagName: 'tr',
    template: window.JST.home_device
});

var HomeDevices = Marionette.CompositeView.extend({
    template: window.JST.home_devices,
    childView: HomeDevice,
    childViewContainer: 'tbody'
});

var HomeEvent = Marionette.ItemView.extend({
    tagName: 'tr',
    template: window.JST.home_event
});

var HomeHistory = Marionette.CompositeView.extend({
    template: window.JST.home_history,
    childView: HomeEvent,
    childViewContainer: 'tbody'
});

var Home = Marionette.LayoutView.extend({
    tagName: "div",
    className: "col-md-12",
    template: window.JST.home,
    regions: {
        wifi: '#home-wifi-config',
        devices: '#home-devices',
        notifications: '#home-notifications',
        history: '#home-history'
    },
    
    onRender: function () {
        "use strict";
        window.setActiveLink("home-link");
        var wifiCollection = new RouterConfigApp.Collections.Wifi();
        wifiCollection.fetch({reset: true});
        var wifi = new HomeWifiCollection({collection: wifiCollection});
        this.wifi.show(wifi);
        var notificationCollection = new RouterConfigApp.Collections.Notifications();
        notificationCollection.fetch({reset: true});
        var notifications = new HomeNotifications({collection: notificationCollection});
        this.notifications.show(notifications);
        var deviceCollection = new RouterConfigApp.Collections.ConnectedDevices();
        deviceCollection.fetch({reset: true});
        var devices = new HomeDevices({collection: deviceCollection});
        this.devices.show(devices);
        var historyCollection = new RouterConfigApp.Collections.Events();
        historyCollection.fetch({reset: true, descending: true, limit: 5});
        var events = new HomeHistory({collection: historyCollection});
        this.history.show(events);
    }
});
