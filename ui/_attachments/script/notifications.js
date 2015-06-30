window.App.Models.Notification = Backbone.Model.extend({
    defaults: {
        collection: "notifications",
        name: "",
        service: "",
        user: "",
        status: "pending"
    }
});

window.App.Models.MainUser = Backbone.Model.extend({
    defaults: {
        collection: "main_user",
        name: "",
        service: ""
    },
    url: "main_user"
});

window.App.Collections.Notifications = Backbone.Collection.extend({
    model: window.App.Models.Notification,
    url: "notifications",
    db: {
        changes: true,
        filter: Backbone.couch_connector.config.ddoc_name + "/notifications_ui"
    }
});

window.App.Views.Notification = Backbone.View.extend({
    tagName: "tr",
    template: window.JST.notification_item,

    initialize: function(){
        "use strict";
        this.listenTo(this.model, "change", this.change_handler);
    },

    events: {
        "click .edit-notification-button": "edit",
        "click .save-notification-button": "save",
        "click .delete-notification-button": "delete",
        "click .cancel-notification-button": "cancel"
    },

    render: function () {
        "use strict";
        this.$el.empty().append(this.template(this.model.toJSON()));
        this.input = this.$(".edit");
        return this;
    },

    change_handler: function(){
        "use strict";
        this.render();
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
        this.input.parents("td").addClass("editing");
        this.input.focus();
    },

    cancel: function () {
        "use strict";
        this.input.parents("td").removeClass("editing");
    },

    save: function () {
        "use strict";
        var self = this;
        this.input.parents("td").removeClass("editing");
        var value = this.input.val();
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

window.App.Views.MainUser = Backbone.View.extend({
    className: "main_user_el",
    template: window.JST.main_user,
    render: function(){
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    }
});

window.App.Views.Notifications = Backbone.View.extend({
    collection: new window.App.Collections.Notifications(),
    tagName: "div",
    className: "col-md-12",
    template: window.JST.notification_collection,
    initialize: function () {
        "use strict";
        this.listenTo(this.collection, "reset", this.render);
        this.listenTo(this.collection, "add", this.addOne);
        this.collection.fetch({reset: true});
        this.subviews = [];
        this.main_user_model = new window.App.Models.MainUser();
        this.main_user_model.fetch();
    },

    events: {
        "change #service": "getPrompt",
        "click #add-notification-button": "addNotification"
    },

    render: function () {
        "use strict";
        this.$el.html(this.template());
        $("#main-row").empty().append(this.el);
        window.setActiveLink("registrations-link");
        this.collection.each(this.addOne, this);
        this.$el.find("#service").trigger("change");
        $(".alert").hide();
        main_user_view = new window.App.Views.MainUser({model: this.main_user_model});
        this.subviews.push(main_user_view);
        $("#main-user-div").html(main_user_view.render().el);
        return this;
    },

    getPrompt: function () {
        "use strict";
        this.$("#user").attr("placeholder", this.$("#service :selected").data("prompt"));
    },

    addOne: function (notification) {
        "use strict";
        var view = new window.App.Views.Notification({model: notification});
        this.subviews.push(view);
        this.$("#notification-registration-table > tbody").append(view.render().el);
    },

    addNotification: function (e) {
        "use strict";
        e.preventDefault();
        var newModel = new window.App.Models.Notification();
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

    exit: function(){
        "use strict";
        var item = null;
        for (var index in this.subviews) {
            item = this.subviews[index];
            item.remove();
        }
        this.remove();
    }
});
