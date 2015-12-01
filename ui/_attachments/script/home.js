HomeWifi = Marionette.ItemView.extend({
    collection: new RouterConfigApp.Collections.WifiHome(),
    template: window.JST.home_wifi
});

HomeNotification = Marionette.ItemView.extend({
    tagName: 'tr',
    template: JST.home_notification
});

HomeNotifications = Marionette.CompositeView.extend({
    collection: new RouterConfigApp.Collections.Notifications(),
    template: JST.home_notifications,
    childViewContainer: 'tbody',
    childView: Notification
});

HomeDevice = Marionette.ItemView.extend({
    tagName: 'tr',
    template: JST.home_device
});

HomeDevices = Marionette.CompositeView.extend({
    collection: new RouterConfigApp.Collections.ConnectedDevices(),
    template: JST.home_devices,
    childView: HomeDevice,
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
        var notifications = new HomeNotifications();
        this.notifications.show(notifications);
        var deviceCollection = new RouterConfigApp.Collections.ConnectedDevices();
        deviceCollection.fetch({reset: true});
        var devices = new HomeDevices({collection: deviceCollection});
        this.devices.show(devices);
    }
});
