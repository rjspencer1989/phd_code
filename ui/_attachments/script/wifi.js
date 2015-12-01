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
        channel: '#channel_select : selected',
        pasword: '#password_input',
        mode: '#mode_select: selected'
    },
    
    saveWifi: function(event){
        "use strict";
        event.preventDefault();
        var changed = false;
        var newSSID = ui.ssid.val();
        var newChannel = ui.channel.val();
        var newPassword = ui.pasword.val();
        var newMode = ui.mode.val();
        var mod = this.collection.at(0);
        if(newSSID !== ""){
            changed = true;
            mod.set({ssid: newSSID});
        }
        if(newChannel !== "blank"){
            changed = true;
            mod.set({channel: newChannel});
        }
        if(newMode !== "blank"){
            changed = true;
            mod.set({mode: newMode});
        }
        if(newPassword !== ""){
            changed = true;
            mod.set({password: newPassword});
        }
        mod.set({status: "pending"});

        if (newSSID === "" && newPassword === "") {
            mod.set({with_bss: false});
        }
        if(changed === true){
            mod.save(null, {
                error: function(model, response){
                    $(".alert.alert-danger").append(response.reason).show();
                    this.collection.fetch({reset: true});
                },
                success: function(model, response){
                    $(".alert.alert-success").show();
                }
            });
        }
        console.log(changed);
        return false;
    }
});

WiFi = Marionette.CollectionView.extend({
   tagName: 'div',
   className: 'col-md-12',
   childView: WifiModel
});
