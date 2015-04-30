'use strict';
App.Models.Notification = Backbone.Model.extend({
    defaults: {
        collection: 'notifications',
        name: '',
        service: '',
        user:''
    }
});

App.Collections.Notifications = Backbone.Collection.extend({
    model: App.Models.Notification,
    url: 'notifications'
});

App.Views.Notification = Backbone.View.extend({
    tagName: 'tr',
    template: _.template($('#notification-items-src').html()),

    events: {
        "click .edit-notification-button" : "edit",
        "click .save-notification-button" : "close",
        "click .delete-notification-button" : "clear",
        "click .cancel-notification-button" : "cancel"
    },

    render: function(){
        this.$el.empty().append(this.template(this.model.toJSON()));
        this.input = this.$('.edit');
        return this;
    },

    clear: function(){
        this.model.set({_deleted: true});
        this.model.save(null, {
            success: function(model, response, options){
                console.log(response);
                addHistoryEvent("Removed Notification Registration", model.get('name') + "  is no longer registered to receive notifications using " + model.get('service') + " identified by " + model.get('user'), App.userCtx.name, model.id, model.get('rev'), true);
            },
            error: function(model, response, options){
                console.log(response);
                if(response.status === 401){
                    App.routerInstance.checkSession();
                } else{
                    $('.alert').append(response.reason).show();
                }
            }
        });
    },

    edit: function(){
        console.log(this.input);
        this.input.parents('td').addClass('editing');
        this.input.focus();
    },

    cancel: function(){
        this.input.parents('td').removeClass('editing');
    },

    close: function(){
        this.input.parents('td').removeClass('editing');
        var value = this.input.val();
        if(value){
            this.model.set({user:value});
            this.model.save(null, {
                success: function(model, response, options){
                    console.log(response);
                    addHistoryEvent("Edited Notification Registration", model.get('name') + " changed notifications for " + model.get('service') + " to identify them as " + model.get('user'), App.userCtx.name, model.id, model.get('rev'), true);
                },
                error: function(model, response, options){
                    console.log(response);
                    if(response.status === 401){
                        App.routerInstance.checkSession();
                    } else{
                        $('.alert').append(response.reason).show();
                    }
                }
            });
        }
    }
});

App.Views.Notifications = Backbone.View.extend({
    collection: new App.Collections.Notifications(),
    el: '#main-content',
    template: JST['templates/notification_collection.html'](),

    initialize: function(){
        this.collection.on('reset', this.render, this);
        this.collection.on('change', this.render, this);
        this.collection.on('remove', this.render, this);
        this.collection.on('add', this.addOne, this);
        this.collection.fetch({reset:true});
    },

    events : {
        'change #service' : 'getPrompt',
        'click #add-notification-button' : 'addNotification'
    },

    render: function(){
        this.$el.empty().append(this.template());
        setActiveLink('services-link');
        this.collection.each(this.addOne, this);
        this.$el.find('#service').trigger('change');
        $('.alert').hide();
        return this;
    },

    getPrompt: function(e){
        this.$('#user').attr('placeholder', this.$('#service :selected').data('prompt'));
    },

    addOne: function(notification){
        var view = new App.Views.Notification({model: notification});
        this.$('#notification-registration-table > tbody').append(view.render().el);
    },

    addNotification: function(e){
        e.preventDefault();
        var newModel = {};
        $('#add-notification-form').children('input').each(function(i,el){
            if($(el).val() !== ""){
                newModel[el.id] = $(el).val();
            }
        });
        newModel.service = $('#service').val();
        this.collection.create(newModel, {
            sucess : function(model, response, options){
                addHistoryEvent("New Notification Registration", model.get('name') + " registered to receive notifications using " + model.get('service') + " identified by " + model.get('user'), App.userCtx.name, model.id, model.get('rev'), true);
            }
        });
    }
});

function drawNotifications(){
    App.routerInstance.checkSession();
    var nsv = new App.Views.Notifications();
}
