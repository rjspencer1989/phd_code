window.App.Models.Wifi = Backbone.Model.extend({
    defaults: {
        collection: "wifi",
        status: "pending",
        ssid: "",
        password: "",
        encryption_type: "wpa",
        mode: "n",
        channel: 1
    }
});

window.App.Collections.Wifi = Backbone.Collection.extend({
    model: window.App.Models.Wifi,
    url: "wifi",
    db: {
        changes: true,
        filter: Backbone.couch_connector.config.ddoc_name + "/wifi_ui"
    }
});

window.App.Collections.WifiHome = Backbone.Collection.extend({
    model: window.App.Models.Wifi,
    url: "wifi"
});

window.App.Views.Wifi = Backbone.View.extend({
    collection: new window.App.Collections.Wifi(),
    tagName: "div",
    className: "col-md-12",
    template: window.JST.wifi,
    initialize: function(){
        "use strict";
        this.listenTo(this.collection, "reset", this.render);
        this.listenTo(this.collection, "change", this.render);
        this.collection.fetch({
            reset: true
        });
    },

    events: {
        "submit": "saveWifi"
    },

    render: function(){
        "use strict";
        this.$el.html(this.template(this.collection.at(0).toJSON()));
        $("#main-row").empty().append(this.el);
        window.setActiveLink("wifi-link");
        $(".alert").hide();
        $('[data-toggle="tooltip"]').tooltip();
        return this;
    },

    saveWifi: function(event){
        "use strict";
        event.preventDefault();
        var changed = false;
        var newSSID = $("#ssid_input").val();
        var newChannel = $("#channel_select :selected").val();
        var newPassword = $("#password_input").val();
        var newMode = $("#mode_select :selected").val();
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
                },
                success: function(model, response){
                    $(".alert.alert-success").show();
                }
            });
        }
        console.log(changed);
        return false;
    },

    exit: function(){
        "use strict";
        this.collection = {};
        this.remove();
    }
});
