App.Models.Event = Backbone.Model.extend({
    defaults: {
        title: '',
        description: '',
        user: '',
        timestamp: new Date().toISOString(),
        collection: 'events',
        doc_id: '',
        doc_rev: '',
        undoable: false,
        perform_undo: false
    }
});

App.Collections.Events = Backbone.Collection.extend({
    url: 'events',
    model: App.Models.Event,
    db: {
        view: 'events'
    }
});

App.Views.Event = Backbone.View.extend({
    className: 'item',
    template: _.template($('#history_item_src').html()),
    events:{
        'click .undo-button': 'request_undo'
    },
    render: function(){
        this.$el.empty().append(this.template(this.model.toJSON()));
        return this;
    },
    request_undo: function(){
        this.model.set({perform_undo: true});
        this.model.save();
    }
});

App.Views.Events = Backbone.View.extend({
    el: '#main-content',
    template: _.template($('#history_src').html()),
    collection: new App.Collections.Events(),
    initialize: function(){
        this.collection.on('reset', this.render, this);
        this.collection.fetch({reset: true});
    },

    events: {
        'click .revert-button': 'revert_state'
    }

    render: function(){
        this.$el.empty().append(this.template());
        setActiveLink('history-link');
        this.collection.each(this.addOne, this);
        $('.carousel').carousel();
        return this;
    },

    addOne: function(event, index){
        indicator = $(document.createElement('li'));
        indicator.attr('data-target', '#carousel-history');
        indicator.attr('data-slide-to', index);
        $('.carousel-indicators').append(indicator);
        view = new App.Views.Event({model: event});
        this.$('.carousel-inner').append(view.render().el);
        if(index === 0){
            indicator.addClass('active');
            view.$el.addClass('active');
        }
        if(event.undoable == true){
            view.$el.addClass('undoable');
        }
    },

    revert_state: function(){
        date_selected = this.$('#history_dp').datepicker('getDate').toISOString();
        undo_needed = this.collection.filter(function(m){
            return (m['timestamp'] > date_selected && m['undoable'] == true);
        });
        _.each(undo_needed, function(item){
            console.log(item.toJSON());
        });
    }
});

function addHistoryEvent(title, description, user, docId, docRev, undoable){
    var mod = new App.Models.Event();
    mod.set({title: title});
    mod.set({description: description});
    mod.set({user: user});
    mod.set({timestamp: new Date.toISOString()});
    mod.set({doc_id: docId});
    mod.set({doc_rev: docRev});
    mod.set({undoable: undoable});
    mod.save();
}

function drawHistory(){
    App.routerInstance.checkSession();
    new App.Views.Events();
};
