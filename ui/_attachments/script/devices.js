App.Models.Device = Backbone.Model.extend({
    defaults: {
        action: "",
        collection: "devices",
        device_name: "",
        host_name: "",
        ip_address: "",
        lease_action: "add",
        mac_address: "",
        name: "",
        state: "pending",
        device_type: "",
        notification_service: "",
        timestamp: new Date() / 1000,
        connection_event: "disconnect",
        changed_by: 'system'
    },

    url : this.mac_address
});

App.Collections.Devices = Backbone.Collection.extend({
    url : 'devices',
    db : {
        view: 'control',
        changes: true,
        filter: Backbone.couch_connector.config.ddoc_name + "/devices_ui"
    },
    model : App.Models.Device
});

App.Collections.ConnectedDevices = Backbone.Collection.extend({
    url : 'devices',
    db : {
        view: 'connected_devices'
    },
    model : App.Models.Device
});

App.Views.Device = Backbone.View.extend({
    tagName: 'tr',
    initialize: function(options){
        this.template = window.JST[options.template];
    },

    events: {
        'click .deny-button' : 'deny',
        'click .permit-button' : 'permit',
        'click .edit-button' : 'edit',
        'click .cancel-button' : 'cancel',
        'click .save-button' : 'save'
    },

    render: function(){
        this.$el.empty().append(this.template(this.model.toJSON()));
        this.$el.addClass('device');
        txt = "No";
        if(this.model.get('connection_event') === "connect"){
            txt = 'Yes';
        }
        this.$('.is_connected').html(txt);
        return this;
    },

    deny: function(event){
        if(this.$el.hasClass('edit-device')){
            owner = this.$('#device_owner_input').val();
            device_name = this.$('#device_name_input').val();
            device_type = this.$('#device_type_select :selected').val();
            notification_service = this.$('#device_notification_select :selected').val();
            this.model.set({name: owner});
            this.model.set({device_name: device_name});
            this.model.set({device_type: device_type});
            this.model.set({notification_service: notification_service});
        }
        this.model.set({action: 'deny'});
        this.model.set({changed_by: 'user'});
        this.model.save(null, {
            success: function(model, response, options){
                console.log(response);
                addHistoryEvent('Device Denied', 'The device with MAC Address ' + model.get('mac_address') + ' was denied access to your network', App.userCtx.name, model.id, model.get('_rev'), true);
            },
            error: function(model, response, options){
                console.log(response);
                if(response.status === 401){
                    App.routerInstance.checkSession();
                } else{
                    $('.alert').append(response.reason).show();
                }
            }
        });
    },

    permit: function(event){
        if(this.$el.hasClass('edit-device')){
            owner = this.$('#device_owner_input').val();
            device_name = this.$('#device_name_input').val();
            device_type = this.$('#device_type_select :selected').val();
            notification_service = this.$('#device_notification_select :selected').val();
            this.model.set({name: owner});
            this.model.set({device_name: device_name});
            this.model.set({device_type: device_type});
            this.model.set({notification_service: notification_service});
        }
        this.model.set({action: 'permit'});
        this.model.set({changed_by: 'user'});
        this.model.save(null, {
            success: function(model, response, options){
                console.log(response);
                addHistoryEvent("Device Permitted", model.get('device_name') + " was permitted to use your network. It belongs to " + model.get('name') + ", it is a " + model.get("device_type") + " and network notifications are sent using " + model.get('notification_service'), App.userCtx.name, model.id, model.get('_rev'), true);
            },
            error: function(model, response, options){
                console.log(response);
                if(response.status === 401){
                    App.routerInstance.checkSession();
                } else{
                    $('.alert').append(response.reason).show();
                }
            }
        });
    },

    edit: function(event){
        this.$el.addClass('editing');
        this.$el.find('#device_notification_select').val(this.model.get('notification_service'));
        this.$el.find('#device_type_select').val(this.model.get('device_type'));
    },

    cancel: function(event){
        this.$el.removeClass('editing');
    },

    save: function(event){
        owner = this.$('#edit_owner_input').val();
        device_name = this.$('#edit_device_name_input').val();
        device_type = this.$('#device_type_select :selected').val();
        notification_service = this.$('#device_notification_select :selected').val();
        this.model.set({name: owner});
        this.model.set({device_name: device_name});
        this.model.set({device_type: device_type});
        this.model.set({notification_service: notification_service});
        this.model.save(null, {
            success: function(model, response, options){
                console.log(response);
                addHistoryEvent("Edited Device settings", "The device with MAC address " + model.get('mac_address') + " has been updated", App.userCtx.name, model.id, model.get('rev'), true);
            },
            error: function(model, response, options){
                console.log(response);
                if(response.status === 401){
                    App.routerInstance.checkSession();
                } else{
                    $('.alert').append(response.reason).show();
                }
            }
        });
        this.$el.removeClass('editing');

    }
});

App.Views.ControlPanelView = Backbone.View.extend({
    collection: new App.Collections.Devices(),
    el: '#main-content',
    template: window.JST.control_panel,
    initialize: function(){
        this.listenTo(this.collection, 'reset', this.render);
        this.listenTo(this.collection, 'add', this.addOne);
        this.listenTo(this.collection, 'change', this.render);
        this.listenTo(this.collection, 'remove', this.render);
        this.collection.fetch({reset: true});
        this.subviews = [];
    },

    addOne: function(device){
        sel = device.get('state');
        var view = new App.Views.Device({model: device, template: 'device_' + sel});
        this.subviews.push(view);
        this.$('.' + sel).append(view.render().el);
        if(sel === 'pending'){
            view.$el.addClass('edit-device');
        }
    },

    render: function(){
        this.$el.empty().append(this.template());
        setActiveLink('services-link');
        $('.alert').hide();
        this.collection.each(this.addOne, this);
    },

    exit: function(){
        for (var index in this.subviews) {
            item = this.subviews[index];
            item.exit();
        }
        this.remove();
    }
});
