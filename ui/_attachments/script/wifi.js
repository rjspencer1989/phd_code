RouterConfigApp.Models.Wifi = Backbone.Model.extend({
    defaults: {
        collection: "wifi",
        status: "pending",
        ssid: "",
        password: "",
        encryption_type: "wpa",
        mode: "n",
        channel: 1,
        bss_active: false
    }
});

RouterConfigApp.Collections.Wifi = Backbone.Collection.extend({
    model: RouterConfigApp.Models.Wifi,
    url: "wifi",
    db: {
        changes: true,
        filter: Backbone.couch_connector.config.ddoc_name + "/wifi_ui"
    }
});

WifiModel = Marionette.ItemView.extend({
   template: JST.wifi,
   
   events: {
        "submit #save-wifi-form": "saveWifi"
    },
    
    onShow: function(){
        window.setActiveLink("wifi-link");
        $('[data-toggle="tooltip"]').tooltip();
    },
    
    ui: {
        ssid: '#ssid_input',
        channel: '#channel_select',
        pasword: '#password_input',
        mode: '#mode_select'
    },
    
    saveWifi: function(event){
        "use strict";
        event.preventDefault();
        var changed = false;
        var newSSID = this.ui.ssid.val();
        var newChannel = this.ui.channel.val();
        var newPassword = this.ui.pasword.val();
        var newMode = this.ui.mode.val();

        if(newSSID !== ""){
            changed = true;
            this.model.set({ssid: newSSID});
        }
        if(newChannel !== "blank"){
            changed = true;
            this.model.set({channel: newChannel});
        }
        if(newMode !== "blank"){
            changed = true;
            this.model.set({mode: newMode});
        }
        if(newPassword !== ""){
            changed = true;
            this.model.set({password: newPassword});
        }
        this.model.set({status: "pending"});

        if (newSSID === "" && newPassword === "") {
            this.model.set({with_bss: false});
        }
        if(changed === true){
            this.model.save(null, {
                error: function(model, response){
                    $(".alert.alert-danger").append(response.reason).show();
                    model.fetch({reset: true});
                },
                success: function(model, response){
                    $(".alert.alert-success").show();
                    model.fetch({reset: true});
                }
            });
        }
    }
});

WiFi = Marionette.CollectionView.extend({
   tagName: 'div',
   className: 'col-md-12',
   childView: WifiModel
});
