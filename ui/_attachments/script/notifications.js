RouterConfigApp.Models.Notification = Backbone.Model.extend({
    defaults: {
        collection: "notifications",
        name: "",
        service: "",
        user: "",
        status: "pending"
    }
});

RouterConfigApp.Collections.Notifications = Backbone.Collection.extend({
    model: RouterConfigApp.Models.Notification,
    url: "notifications",
    db: {
        changes: true,
        filter: Backbone.couch_connector.config.ddoc_name + "/notifications_ui"
    }
});

var Notification = Marionette.ItemView.extend({
    tagName: "tr",
    template: window.JST.notification_item,

    events: {
        "click .edit-notification-button": "edit",
        "submit .edit-notification-form": "save",
        "click .delete-notification-button": "delete",
        "click .cancel-notification-button": "cancel"
    },
    
    ui: {
        input: ".edit"
    },

    delete: function () {
        "use strict";
        var self = this;
        this.model.set({hidden: true});
        this.model.set({status: "pending"});
        this.model.save(null, {
            success: function () {
                self.remove();
            },
            error: function (model, response) {
                $(".alert").append(response.reason).show();
            }
        });
    },

    edit: function () {
        "use strict";
        this.ui.input.parents("td").addClass("editing");
        this.ui.input.focus();
    },

    cancel: function () {
        "use strict";
        this.ui.input.parents("td").removeClass("editing");
    },

    save: function (e) {
        "use strict";
        e.preventDefault();
        var self = this;
        this.ui.input.parents("td").removeClass("editing");
        var value = this.ui.input.val();
        if (value) {
            this.model.set({user: value});
            this.model.set({status: "pending"});
            this.model.save(null, {
                success: function () {
                    self.render();
                },
                error: function (model, response) {
                    $(".alert").append(response.reason).show();
                }
            });
        }
    }
});

var Notifications = Marionette.CompositeView.extend({
    tagName: "div",
    className: "col-md-12",
    template: window.JST.notification_collection,
    childView: Notification,
    childViewContainer: 'tbody',
    
    events: {
        "change #service": "getPrompt",
        "submit #add-notification-form": "addNotification"
    },

    onRender: function () {
        "use strict";
        window.setActiveLink("registrations-link");
        this.$el.find("#service").trigger("change");
        return this;
    },

    getPrompt: function () {
        "use strict";
        this.$("#user").attr("placeholder", this.$("#service :selected").data("prompt"));
    },

    addNotification: function (e) {
        "use strict";
        e.preventDefault();
        var newModel = new RouterConfigApp.Models.Notification();
        $("#add-notification-form").children("input").each(function (i, el) {
            if ($(el).val() !== "") {
                newModel.set(el.id, $(el).val());
            }
        });
        newModel.set("service", $("#service").val());
        newModel.set("status", "pending");
        this.collection.create(newModel);
        $("#add-notification-form").get(0).reset();
        this.getPrompt();
    },
    
    onDestroy: function(){
        "use strict";
        this.collection.stop_changes();
    }
});

var NotificationLayout = Marionette.LayoutView.extend({
    className: 'col-md-12',
    template: window.JST.notification_layout,
    regions: {
        notification_region: '#notification_region',
        main_user_region: '#main_user_region'
    }
});