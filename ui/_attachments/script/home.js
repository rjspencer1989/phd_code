App.Views.WifiHome = Backbone.View.extend({
    collection: new App.Collections.Wifi(),
    el: '#home-wifi-config',
    template: _.template($('#home-wifi-src').html()),
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
    template: _.template($('#home_device_src').html()),
    render: function(){
        this.$el.empty().append(this.template(this.model.toJSON()));
        return this;
    }
});

App.Views.ConnectedDevicesHome = Backbone.View.extend({
    el: '#home-devices',
    template: window.JST['templates/home.html'],
    collection: new App.Collections.ConnectedDevices(),
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

    addOne: function(device){
        var view = new App.Views.DeviceHome({model: device});
        this.$('tbody').append(view.render().el);
    },

    render: function () {
        'use strict';
        this.$el.empty().append(this.template());
        this.collection.each(this.addOne, this);
        return this;
    }
});

App.Views.Home = Backbone.View.extend({
    el: '#main-content',
    template : _.template($('#home-src').html()),
    initialize: function () {
        'use strict';
        this.render();
        new App.Views.WifiHome();
        new App.Views.ConnectedDevicesHome();
    },

    render : function () {
        'use strict';
        this.$el.empty().append(this.template());
        setActiveLink('home-link');
    }
});

function drawHome(){
    App.routerInstance.checkSession();
    new App.Views.Home();
}
