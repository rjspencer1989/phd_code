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
        "click .save-notification-button" : "save",
        "click .delete-notification-button" : "delete",
        "click .cancel-notification-button" : "cancel"
    },

    render: function () {
        'use strict';
        this.$el.empty().append(this.template(this.model.toJSON()));
        this.input = this.$('.edit');
        return this;
    },

    delete: function () {
        'use strict';
        var self = this;
        this.model.set({hidden: true});
        this.model.set({status: 'pending'});
        this.model.save(null, {
            success: function (model, response, options) {
                console.log(response);
                self.remove();
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

    save: function () {
        'use strict';
        this.input.parents('td').removeClass('editing');
        var value = this.input.val();
        if (value) {
            this.model.set({user: value});
            this.model.set({status: 'pending'});
            this.model.save(null, {
                success: function (model, response, options) {
                    console.log(response);
                },
                error: function (model, response, options) {
                    console.log(response);
                    $('.alert').append(response.reason).show();
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
        this.listenTo(this.collection, 'change', this.change_handler);
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
    
    change_handler: function(){
        'use strict';
        console.log('change');
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
            sucess : function (model) {
                console.log(model.toJSON());
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
