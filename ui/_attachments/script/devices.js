RouterConfigApp.Models.Device = Backbone.Model.extend({
    url: this.mac_address
});

RouterConfigApp.Collections.Devices = Backbone.Collection.extend({
    url: "devices",
    db: {
        view: "control",
        changes: true,
        filter: Backbone.couch_connector.config.ddoc_name + "/devices_ui"
    },
    model: RouterConfigApp.Models.Device
});

RouterConfigApp.Collections.ConnectedDevices = Backbone.Collection.extend({
    url: "devices",
    db: {
        view: "connected_devices"
    },
    model: RouterConfigApp.Models.Device
});

RouterConfigApp.Collections.MacLookup = Backbone.Collection.extend({
    url: "devices",
    model: RouterConfigApp.Models.Device,
    db: {
        view: "mac_from_ip"
    }
});

Device = Marionette.ItemView.extend({
    className: "col-lg-3 col-md-4 col-sm-6 device",

    getTemplate: function(){
        return JST[this.model.get('state')];
    },

    ui: {
        device_name : '#edit_device_name_input',
        owner: '#device_owner_input',
        port: '.port',
        isConnected: '.is_connected',
        denyButton: '.deny-button',
        permitButton: '.permit-button',
        editButton: '.edit-button',
        cancelButton: '.cancel-button',
        saveButton: '.save-button',
        errorAlert: '.alert-danger strong'
    },

    events: {
        "click @ui.denyButton": "deny",
        "click @ui.permitButton": "permit",
        "click @ui.editButton": "edit",
        "click @ui.cancelButton": "cancel",
        "click @ui.saveButton": "save"
    },

    modelEvents: {
        "change": function(){
            this.render();
        }
    },

    onRender: function(){
        "use strict";
        var txt = "No";
        var port = this.model.get("port");
        var re = /^wlan0(_1)?$/;
        if(re.test(port)){
            port = 'WiFi';
        }
        if(this.model.get("connection_event") === "connect"){
            txt = "Yes";
        }
        this.ui.isConnected.html(txt);
        this.ui.port.html(port);
        var router_ip = window.location.hostname;
        var end = parseInt(router_ip.substr(router_ip.lastIndexOf('.') + 1), 10);
        var client_ip = '10.2.0.' + (end - 1).toString();
        if(this.model.get('ip_address') === client_ip){
            this.ui.denyButton.attr('disabled', true);
        }

        if(this.model.get('state') === 'pending'){
            this.$el.addClass('editing');
        } else{
            this.$el.removeClass('editing');
        }
    },

    deny: function(){
        "use strict";
        if(this.$el.hasClass("editing")){
            var owner = this.ui.owner.val();
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
                this.ui.errorAlert.append(response.reason);
                this.ui.errorAlert.show();
            }
        });
    },

    permit: function(){
        "use strict";
        if(this.$el.hasClass("editing")){
            var owner = this.ui.owner.val();
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
                this.ui.errorAlert.append(response.reason);
                this.ui.errorAlert.show();
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
        var owner = this.ui.owner.val();
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
                this.ui.errorAlert.append(response.reason);
                this.ui.errorAlert.show();
            }
        });
    }
});

Devices = Marionette.CompositeView.extend({
    collection: new RouterConfigApp.Collections.Devices(),
    tagName: "div",
    className: "col-md-12",
    template: window.JST.control_panel,
    childView: Device,
    childViewContainer: '.device_container',

    onRender: function(){
        "use strict";
        window.setActiveLink("devices-link");
    }
});
