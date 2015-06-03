App.Views.WifiHome = Backbone.View.extend({
    collection: new App.Collections.Wifi(),
    el: '#home-wifi-config',
    template: window.JST.home_wifi,
    initialize: function () {
        'use strict';
        this.listenTo(this.collection, 'reset', this.render);
        this.listenTo(this.collection, 'change', this.render);
        this.collection.fetch({
            reset: true,
            error: function(data){
                console.log(data);
                App.routerInstance.checkSession();
            }
        });
    },

    render: function () {
        'use strict';
        this.$el.empty().append(this.template(this.collection.at(0).toJSON()));
        return this;
    }
});

App.Views.DeviceHome = Backbone.View.extend({
    tagName: 'tr',
    template: window.JST.home_device,
    render: function(){
        this.$el.empty().append(this.template(this.model.toJSON()));
        return this;
    }
});

App.Views.ConnectedDevicesHome = Backbone.View.extend({
    el: '#home-devices',
    template: window.JST.home_devices,
    collection: new App.Collections.ConnectedDevices(),
    initialize: function () {
        'use strict';
        this.listenTo(this.collection, 'reset', this.render);
        this.listenTo(this.collection, 'change', this.render);
        this.subviews = [];
        this.collection.fetch({
            reset: true,
            error: function(data){
                console.log(data);
            }
        });
    },

    addOne: function(device){
        'use strict';
        var view = new App.Views.DeviceHome({model: device});
        this.subviews.push(view);
        this.$('tbody').append(view.render().el);
    },

    render: function () {
        'use strict';
        this.$el.empty().append(this.template());
        this.collection.each(this.addOne, this);
        return this;
    },

    exit: function(){
        'use strict';
        for (var index in this.subviews) {
            this.subviews[index].remove();
        }
    }
});

App.Views.Home = Backbone.View.extend({
    tagName: 'div',
    className: 'col-md-12',
    template : window.JST.home,
    initialize: function () {
        'use strict';
        this.render();
        this.wifi_view = new App.Views.WifiHome();
        this.devices_view = new App.Views.ConnectedDevicesHome();
    },

    render : function () {
        'use strict';
        this.$el.empty().append(this.template());
        $('#main-row').html(this.el);
        setActiveLink('home-link');
    },

    exit: function(){
        this.wifi_view.remove();
        this.devices_view.exit();
        this.remove();
    }
});
