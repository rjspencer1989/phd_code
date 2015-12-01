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
   }
});

WiFi = Marionette.CollectionView.extend({
   tagName: 'div',
   className: 'col-md-12',
   childView: WifiModel
});
