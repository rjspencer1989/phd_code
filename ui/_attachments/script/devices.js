App.Models.Device = Backbone.Model.extend({
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
        var txt = "No";
        if(this.model.get('connection_event') === "connect"){
            txt = 'Yes';
        }
        this.$('.is_connected').html(txt);
        return this;
    },

    deny: function(){
        if(this.$el.hasClass('edit-device')){
            var owner = this.$('#device_owner_input').val();
            var device_name = this.$('#device_name_input').val();
            var device_type = this.$('#device_type_select :selected').val();
            var notification_service = this.$('#device_notification_select :selected').val();
            this.model.set({name: owner});
            this.model.set({device_name: device_name});
            this.model.set({device_type: device_type});
            this.model.set({notification_service: notification_service});
        }
        this.model.set({action: 'deny'});
        this.model.set({changed_by: 'user'});
        this.model.save(null, {
            success: function(model, response){
                console.log(response);
            },
            error: function(model, response){
                console.log(response);
                $('.alert').append(response.reason).show();
            }
        });
    },

    permit: function(){
        if(this.$el.hasClass('edit-device')){
            var owner = this.$('#device_owner_input').val();
            var device_name = this.$('#device_name_input').val();
            var device_type = this.$('#device_type_select :selected').val();
            var notification_service = this.$('#device_notification_select :selected').val();
            this.model.set({name: owner});
            this.model.set({device_name: device_name});
            this.model.set({device_type: device_type});
            this.model.set({notification_service: notification_service});
        }
        this.model.set({action: 'permit'});
        this.model.set({changed_by: 'user'});
        this.model.save(null, {
            success: function(model, response){
                console.log(response);
            },
            error: function(model, response){
                console.log(response);
                $('.alert').append(response.reason).show();
            }
        });
    },

    edit: function(){
        this.$el.addClass('editing');
        this.$el.find('#device_notification_select').val(this.model.get('notification_service'));
        this.$el.find('#device_type_select').val(this.model.get('device_type'));
    },

    cancel: function(){
        this.$el.removeClass('editing');
    },

    save: function(){
        var owner = this.$('#edit_owner_input').val();
        var device_name = this.$('#edit_device_name_input').val();
        var device_type = this.$('#device_type_select :selected').val();
        var notification_service = this.$('#device_notification_select :selected').val();
        this.model.set({name: owner});
        this.model.set({device_name: device_name});
        this.model.set({device_type: device_type});
        this.model.set({notification_service: notification_service});
        this.model.set({changed_by: 'user'});
        this.model.save(null, {
            success: function(model, response){
                console.log(response);
            },
            error: function(model, response){
                console.log(response);
                $('.alert').append(response.reason).show();
            }
        });
        this.$el.removeClass('editing');
    }
});

App.Views.ControlPanelView = Backbone.View.extend({
    collection: new App.Collections.Devices(),
    tagName: 'div',
    className: 'col-md-12',
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
        var sel = device.get('state');
        var view = new App.Views.Device({model: device, template: 'device_' + sel});
        this.subviews.push(view);
        this.$('.' + sel).append(view.render().el);
        if(sel === 'pending'){
            view.$el.addClass('edit-device');
        }
    },

    render: function(){
        this.$el.html(this.template());
        $('#main-row').empty().append(this.el);
        setActiveLink('devices-link');
        $('.alert').hide();
        this.collection.each(this.addOne, this);
        return this;
    },

    exit: function(){
        var item = {};
        for (var index in this.subviews) {
            item = this.subviews[index];
            item.remove();
        }
        this.remove();
    }
});
