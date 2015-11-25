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

window.App.Views.TableRow = Backbone.View.extend({
    tagName: "tr",
    initialize: function(options){
        "use strict";
        this.template = window.JST[options.template];
    },
    
    render: function(){
        "use strict";
        this.$el.empty().append(this.template(this.model.toJSON()));
        return this;
    }
});

window.App.Views.CollectionHome = Backbone.View.extend({
    initialize: function(options){
        "use strict";
        this.el = options.el;
        this.collection = new App.Collections[options.collection]();
        this.template = window.JST[options.template];
        this.subTemplate = options.sub_template;
        this.listenTo(this.collection, "reset", this.render);
        this.listenTo(this.collection, "change", this.render);
        this.subviews = [];
        this.collection.fetch({
            reset: true
        });
    },
    
    addOne: function(item){
        "use strict";
        var view = new window.App.Views.TableRow({model: item, template: this.subTemplate});
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
        var options = {
            collection: "Notifications", 
            template: "home_notifications", 
            sub_template: "home_notification", 
            el: "#home-notifications"
        };
        this.notifications_view = new window.App.Views.CollectionHome(options);
        options = {
            collection: "ConnectedDevices",
            template: "home_devices",
            sub_template: "home_device",
            el: "#home-devices"
        };
        this.devices_view = new window.App.Views.CollectionHome(options);
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
