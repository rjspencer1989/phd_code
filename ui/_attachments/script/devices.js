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

var Device = Marionette.ItemView.extend({
    className: "col-lg-3 col-md-4 col-sm-6 device",
    getTemplate: function(){
        if(this.edit_mode){
            return window.JST.edit;
        } else if(this.model.get('state') === 'pending'){
            return window.JST.pending;
        } else {
            return window.JST.device;
        }
    },
    
    templateHelpers: {
        states: {
            permit: {
                button_text: 'Deny',
                button_class: 'deny-button',
                bootstrap_class: 'btn-danger'
            },
        
            deny: {
                button_text: 'Permit',
                button_class: 'permit-button',
                bootstrap_class: 'btn-success'
            }
        }
    },

    ui: {
        device_name : '#device_name_input',
        owner: '#edit_owner_input',
        notification_service: '#device_notification_select',
        device_type: '#device_type_select',
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
        if(this.model.get('ip_address') === RouterConfigApp.clientIP){
            this.ui.denyButton.attr('disabled', true);
        }
    },

    deny: function(){
        "use strict";
        if(this.model.get('state') === 'pending'){
            var owner = this.ui.owner.val();
            var device_name = this.ui.device_name.val();
            var device_type = this.ui.device_type.val();
            var notification_service = this.ui.notification_service.val();
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
        if(this.model.get('state') === 'pending'){
            var owner = this.ui.owner.val();
            var device_name = this.ui.device_name.val();
            var device_type = this.ui.device_type.val();
            var notification_service = this.ui.notification_service.val();
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
        this.edit_mode = true;
        this.render();
    },

    cancel: function(){
        "use strict";
        this.edit_mode = false;
        this.render();
    },

    save: function(){
        "use strict";
        var owner = this.ui.owner.val();
        var device_name = this.ui.device_name.val();
        var device_type = this.ui.device_type.val();
        var notification_service = this.ui.notification_service.val();
        this.model.set({name: owner});
        this.model.set({device_name: device_name});
        this.model.set({device_type: device_type});
        this.model.set({notification_service: notification_service});
        this.model.set({changed_by: "user"});
        this.edit_mode = false;
        var error_alert = this.ui.errorAlert;
        this.model.save(null, {
            error: function(model, response){
                error_alert.append(response.reason);
                error_alert.show();
            }
        });
    }
});

var Devices = Marionette.CompositeView.extend({
    tagName: "div",
    className: "col-md-12",
    template: window.JST.control_panel,
    childView: Device,
    childViewContainer: '.device_container',
    
    collectionEvents: {
        'add': function(){
            this.render();
        }
    },

    onRender: function(){
        "use strict";
        window.setActiveLink("devices-link");
    }
});
