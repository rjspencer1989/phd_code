App.Models.Wifi = Backbone.Model.extend({
    defaults : {
        collection : 'wifi',
        status : 'pending',
        ssid : '',
        password : '',
        encryption_type: 'wep',
        password_type: 'txt',
        mode : 'g',
        channel : 1
    }
});

App.Collections.Wifi = Backbone.Collection.extend({
    model : App.Models.Wifi,
    url : 'wifi'
});

App.Views.Wifi = Backbone.View.extend({
    collection: new App.Collections.Wifi(),
    tagName: 'div',
    className: 'col-md-12',
    template : window.JST.wifi,
    initialize : function(){
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

    events : {
        'click #save-wifi-button' : 'saveWifi'
    },

    render: function(){
        this.$el.html(this.template(this.collection.at(0).toJSON()));
        $('#main-row').empty().append(this.el);
        setActiveLink('network-link');
        $('.alert').hide();
        return this;
    },

    saveWifi: function(){
        var newSSID = $('#ssid_input').val();
        var newChannel = $('#channel_select :selected').val();
        var newPasswordType = $('#password_type_select :selected').val();
        var newPassword = $('#password_input').val();
        var mod = this.collection.at(0);
        if(newSSID !== '') mod.set({ssid: newSSID});
        if(newChannel !== 'blank') mod.set({channel: newChannel});
        if(newPasswordType !== 'blank') mod.set({password_type: newPasswordType});
        if(newPassword !== '') mod.set({password: newPassword});
        mod.set({status: 'pending'});
        mod.save(null, {
            success: function(model, response){
                console.log(response);
                //TODO get what settings were changed and put them in the description
                addHistoryEvent("New WiFi Configuration", "WiFi configuration has been updated and devices will need to be reconnected", App.userCtx.name, model.id, model.get('rev'), true);
            },
            error: function(model, response){
                console.log(response);
                if(response.status === 401){
                    App.routerInstance.checkSession();
                } else{
                    $('.alert').append(response.reason).show();
                }
            }
        });
    },

    exit: function(){
        this.remove();
    }
});
