RouterConfigApp.Models.MainUser = Backbone.Model.extend({
    defaults: {
        collection: "main_user",
        name: "",
        service: "",
        _id: "main_user",
        status: "pending"
    }
});

RouterConfigApp.Collections.MainUser = Backbone.Collection.extend({
    model: RouterConfigApp.Models.MainUser,
    url: 'main_user'
});

var MainUser = Marionette.ItemView.extend({
    className: "main_user_el",
    template: window.JST.main_user,
    events: {
        "submit #set-main-user": "set_main_user"
    },
    onRender: function(){
        "use strict";
        var selection = this.$el.find("#main-service option[value=\'" + this.model.get("service") + "\']");
        selection.attr('selected', true);
        return this;
    },
    
    ui: {
        name: "#main-name",
        service: "#main-service"
    },
    
    set_main_user: function(e){
        "use strict";
        e.preventDefault();
        var name = this.ui.name.val();
        var service = this.ui.service.val();
        this.model.set("name", name);
        this.model.set("service", service);
        this.model.set("status", "pending");
        this.model.save(null, {
            success: function(model, response){
                $('.alert.alert-success').show();
            }, error: function(model, response){
                $('.alert.alert-danger').show();
            }
        });
    }
});

var MainUserCollection = Marionette.CollectionView.extend({
    childView: MainUser,
    className: 'col-md-12',
    
    onDestroy: function(){
        "use strict";
        this.collection.stop_changes();
    }
});
