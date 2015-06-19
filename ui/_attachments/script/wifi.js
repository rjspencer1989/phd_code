App.Models.Wifi = Backbone.Model.extend({
    defaults : {
        collection : 'wifi',
        status : 'pending',
        ssid : '',
        password : '',
        encryption_type: 'wpa',
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
        var newPassword = $('#password_input').val();
        var mod = this.collection.at(0);
        if(newSSID !== '') mod.set({ssid: newSSID});
        if(newChannel !== 'blank') mod.set({channel: newChannel});
        if(newPassword !== '') mod.set({password: newPassword});
        mod.set({status: 'pending'});
        mod.save(null, {
            success: function(model, response){
                console.log(response);
            },
            error: function(model, response){
                console.log(response);
                $('.alert').append(response.reason).show();
            }
        });
    },

    exit: function(){
        this.remove();
    }
});
