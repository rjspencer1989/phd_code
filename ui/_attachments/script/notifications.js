App.Models.Notification = Backbone.Model.extend({
    defaults: {
        collection: 'notifications',
        name: '',
        service: '',
        user: '',
        status: 'pending'
    }
});

App.Collections.Notifications = Backbone.Collection.extend({
    model: App.Models.Notification,
    url: 'notifications'
});

App.Views.Notification = Backbone.View.extend({
    tagName: 'tr',
    template: window.JST.notification_item,

    events: {
        "click .edit-notification-button" : "edit",
        "click .save-notification-button" : "close",
        "click .delete-notification-button" : "clear",
        "click .cancel-notification-button" : "cancel"
    },

    render: function () {
        'use strict';
        this.$el.empty().append(this.template(this.model.toJSON()));
        this.input = this.$('.edit');
        return this;
    },

    clear: function () {
        'use strict';
        this.model.set({hidden: true});
        this.model.set({status: 'pending'});
        this.model.save(null, {
            success: function (model, response, options) {
                console.log(response);
                addHistoryEvent("Removed Notification Registration", model.get('name') + "  is no longer registered to receive notifications using " + model.get('service') + " identified by " + model.get('user'), App.userCtx.name, model.id, model.get('_rev'), true);
            },
            error: function (model, response, options) {
                console.log(response);
                $('.alert').append(response.reason).show();
            }
        });
    },

    edit: function () {
        'use strict';
        console.log(this.input);
        this.input.parents('td').addClass('editing');
        this.input.focus();
    },

    cancel: function () {
        'use strict';
        this.input.parents('td').removeClass('editing');
    },

    close: function () {
        'use strict';
        this.input.parents('td').removeClass('editing');
        var value = this.input.val();
        if (value) {
            this.model.set({user: value});
            this.model.set({status: 'pending'});
            this.model.save(null, {
                success: function (model, response, options) {
                    console.log(response);
                    addHistoryEvent("Edited Notification Registration", model.get('name') + " changed notifications for " + model.get('service') + " to identify them as " + model.get('user'), App.userCtx.name, model.id, model.get('_rev'), true);
                },
                error: function (model, response, options) {
                    console.log(response);
                    if (response.status === 401) {
                        App.routerInstance.checkSession();
                    } else {
                        $('.alert').append(response.reason).show();
                    }
                }
            });
        }
    }
});

App.Views.Notifications = Backbone.View.extend({
    collection: new App.Collections.Notifications(),
    tagName: 'div',
    className: 'col-md-12',
    template: window.JST.notification_collection,
    initialize: function () {
        'use strict';
        this.listenTo(this.collection, 'reset', this.render);
        this.listenTo(this.collection, 'change', this.render);
        this.listenTo(this.collection, 'remove', this.render);
        this.listenTo(this.collection, 'add', this.addOne);
        this.collection.fetch({reset: true});
        this.subviews = [];
    },

    events : {
        'change #service' : 'getPrompt',
        'click #add-notification-button' : 'addNotification'
    },

    render: function () {
        'use strict';
        this.$el.html(this.template());
        $('#main-row').empty().append(this.el);
        setActiveLink('services-link');
        this.collection.each(this.addOne, this);
        this.$el.find('#service').trigger('change');
        $('.alert').hide();
        return this;
    },

    getPrompt: function () {
        'use strict';
        this.$('#user').attr('placeholder', this.$('#service :selected').data('prompt'));
    },

    addOne: function (notification) {
        'use strict';
        var view = new App.Views.Notification({model: notification});
        this.subviews.push(view);
        this.$('#notification-registration-table > tbody').append(view.render().el);
    },

    addNotification: function (e) {
        'use strict';
        e.preventDefault();
        var newModel = new App.Models.Notification();
        $('#add-notification-form').children('input').each(function (i, el) {
            if ($(el).val() !== "") {
                newModel.set(el.id, $(el).val());
            }
        });
        newModel.set("service", $('#service').val());
        newModel.set("status", "pending");
        this.collection.create(newModel, {
            sucess : function (model, response, options) {
                addHistoryEvent("New Notification Registration", model.get('name') + " registered to receive notifications using " + model.get('service') + " identified by " + model.get('user'), App.userCtx.name, model.id, model.get('_rev'), true);
            }
        });
    },

    exit: function(){
        for (var index in this.subviews) {
            item = this.subviews[index];
            item.remove();
        }
        this.remove();
    }
});
