App.Models.Wifi = Backbone.Model.extend({
    defaults : {
        collection : 'wifi',
        status : 'pending',
        ssid : '',
        password : '',
        encryption_type: 'wep',
        password_type: 'txt',
        mode : 'n',
        channel : 1
    }
});

App.Collections.Wifi = Backbone.Collection.extend({
    model : App.Models.Wifi,
    url : 'wifi'
});

App.Views.Wifi = Backbone.View.extend({
    collection: new App.Collections.Wifi(),
    el : '#main-content',
    template : window.JST['templates/wifi.html'],
    initialize : function(options){
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
        this.$el.empty().append(this.template(this.collection.at(0).toJSON()));
        setActiveLink('network-link');
        $('.alert').hide();
        return this;
    },

    saveWifi: function(){
        newSSID = $('#ssid_input').val();
        newMode = $('#mode_select :selected').val();
        newChannel = $('#channel_select :selected').val();
        newEncryption = $('#encryption_type_select :selected').val();
        newPasswordType = $('#password_type_select :selected').val();
        newPassword = $('#password_input').val();
        mod = this.collection.at(0);
        if(newSSID !== '') mod.set({ssid: newSSID});
        if(newMode !== 'blank') mod.set({mode: newMode});
        if(newChannel !== 'blank') mod.set({channel: newChannel});
        if(newPasswordType !== 'blank') mod.set({password_type: newPasswordType});
        if(newPassword !== '') mod.set({password: newPassword});
        mod.set({status: 'pending'});
        mod.save(null, {
            success: function(model, response, options){
                console.log(response);
                //TODO get what settings were changed and put them in the description
                addHistoryEvent("New WiFi Configuration", "WiFi configuration has been updated and devices will need to be reconnected", App.userCtx.name, model.id, model.get('rev'), true);
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
    }
});

function drawWifi() {
    App.routerInstance.checkSession();
    window.wifiView = new App.Views.Wifi();
}
