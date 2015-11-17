window.App.Models.Device = Backbone.Model.extend({
    url: this.mac_address
});

window.App.Collections.Devices = Backbone.Collection.extend({
    url: "devices",
    db: {
        view: "control",
        changes: true,
        filter: Backbone.couch_connector.config.ddoc_name + "/devices_ui"
    },
    model: window.App.Models.Device
});

window.App.Collections.ConnectedDevices = Backbone.Collection.extend({
    url: "devices",
    db: {
        view: "connected_devices"
    },
    model: window.App.Models.Device
});

window.App.Views.Device = Backbone.View.extend({
    tagName: "tr",
    initialize: function(options){
        "use strict";
        this.template = window.JST[options.template];
    },

    events: {
        "click .deny-button": "deny",
        "click .permit-button": "permit",
        "click .edit-button": "edit",
        "click .cancel-button": "cancel",
        "click .save-button": "save"
    },

    render: function(){
        "use strict";
        this.$el.empty().append(this.template(this.model.toJSON()));
        this.$el.addClass("device");
        var txt = "No";
        var port = this.model.get("port");
        var re = /^wlan0(_1)?$/;
        if(re.test(port)){
            port = 'WiFi';
        }
        if(this.model.get("connection_event") === "connect"){
            txt = "Yes";
        }
        this.$(".is_connected").html(txt);
        this.$(".port").html(port);
        var router_ip = window.location.hostname;
        var end = parseInt(router_ip.substr(router_ip.lastIndexOf('.') + 1));
        var client_ip = '10.2.0.' + (end - 1).toString();
        if(this.model.get('ip_address') === client_ip){
            this.$('.deny-button').attr('disabled', true);
        }
        return this;
    },

    deny: function(){
        "use strict";
        if(this.$el.hasClass("edit-device")){
            var owner = this.$("#device_owner_input").val();
            var device_name = this.$("#device_name_input").val();
            var device_type = this.$("#device_type_select :selected").val();
            var notification_service = this.$("#device_notification_select :selected").val();
            this.model.set({name: owner});
            this.model.set({device_name: device_name});
            this.model.set({device_type: device_type});
            this.model.set({notification_service: notification_service});
        }
        this.model.set({action: "deny"});
        this.model.set({changed_by: "user"});
        this.model.save(null, {
            error: function(model, response){
                $(".alert").append(response.reason).show();
            }
        });
    },

    permit: function(){
        "use strict";
        if(this.$el.hasClass("edit-device")){
            var owner = this.$("#device_owner_input").val();
            var device_name = this.$("#device_name_input").val();
            var device_type = this.$("#device_type_select :selected").val();
            var notification_service = this.$("#device_notification_select :selected").val();
            this.model.set({name: owner});
            this.model.set({device_name: device_name});
            this.model.set({device_type: device_type});
            this.model.set({notification_service: notification_service});
        }
        this.model.set({action: "permit"});
        this.model.set({changed_by: "user"});
        this.model.save(null, {
            error: function(model, response){
                $(".alert").append(response.reason).show();
            }
        });
    },

    edit: function(){
        "use strict";
        this.$el.addClass("editing");
        this.$el.find("#device_notification_select").val(this.model.get("notification_service"));
        this.$el.find("#device_type_select").val(this.model.get("device_type"));
    },

    cancel: function(){
        "use strict";
        this.$el.removeClass("editing");
    },

    save: function(){
        "use strict";
        var owner = this.$("#edit_owner_input").val();
        var device_name = this.$("#edit_device_name_input").val();
        var device_type = this.$("#device_type_select :selected").val();
        var notification_service = this.$("#device_notification_select :selected").val();
        this.model.set({name: owner});
        this.model.set({device_name: device_name});
        this.model.set({device_type: device_type});
        this.model.set({notification_service: notification_service});
        this.model.set({changed_by: "user"});
        this.model.save(null, {
            error: function(model, response){
                $(".alert").append(response.reason).show();
            }
        });
        this.$el.removeClass("editing");
    }
});

window.App.Views.ControlPanelView = Backbone.View.extend({
    collection: new window.App.Collections.Devices(),
    tagName: "div",
    className: "col-md-12",
    template: window.JST.control_panel,
    initialize: function(){
        "use strict";
        this.listenTo(this.collection, "reset", this.render);
        this.listenTo(this.collection, "add", this.addOne);
        this.listenTo(this.collection, "remove", this.render);
        this.listenTo(this.collection, "change", this.render);
        this.collection.fetch({reset: true});
        this.subviews = [];
    },

    addOne: function(device){
        "use strict";
        var sel = device.get("state");
        var view = new window.App.Views.Device({model: device, template: "device_" + sel});
        this.subviews.push(view);
        this.$("." + sel).append(view.render().el);
        if(sel === "pending"){
            view.$el.addClass("edit-device");
        }
    },

    render: function(){
        "use strict";
        this.$el.html(this.template());
        $("#main-row").empty().append(this.el);
        window.setActiveLink("devices-link");
        $(".alert").hide();
        this.collection.each(this.addOne, this);
        return this;
    },

    closeSubViews: function(){
        "use strict";
        var item = {};
        for (var index in this.subviews) {
            item = this.subviews[index];
            item.remove();
        }
    },

    exit: function(){
        "use strict";
        this.closeSubViews();
        this.remove();
    }
});
