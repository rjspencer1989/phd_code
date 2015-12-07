HomeWifi = Marionette.ItemView.extend({
    template: window.JST.home_wifi
});

HomeWifiCollection = Marionette.CollectionView.extend({
    childView: HomeWifi
});

HomeNotification = Marionette.ItemView.extend({
    tagName: 'tr',
    template: JST.home_notification
});

HomeNotifications = Marionette.CompositeView.extend({
    template: JST.home_notifications,
    childViewContainer: 'tbody',
    childView: HomeNotification
});

HomeDevice = Marionette.ItemView.extend({
    tagName: 'tr',
    template: JST.home_device
});

HomeDevices = Marionette.CompositeView.extend({
    template: JST.home_devices,
    childView: HomeDevice,
    childViewContainer: 'tbody'
});

HomeEvent = Marionette.ItemView.extend({
    tagName: 'tr',
    template: JST.home_event
});

HomeHistory = Marionette.CompositeView.extend({
    template: JST.home_history,
    childView: HomeEvent,
    childViewContainer: 'tbody'
});

Home = Marionette.LayoutView.extend({
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
