App.Models.Event = Backbone.Model.extend({
    defaults: {
        title: '',
        description: '',
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
    template: window.JST.history_item,
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
    tagName: 'div',
    className: 'col-md-12',
    template: window.JST.history,
    collection: new App.Collections.Events(),
    initialize: function(){
        this.listenTo(this.collection, 'reset', this.render);
        this.collection.fetch({reset: true});
        this.subviews = [];
    },

    events: {
        'click .revert-button': 'revert_state'
    },

    render: function(){
        this.$el.html(this.template());
        $('#main-row').empty().append(this.el);
        setActiveLink('history-link');
        this.collection.each(this.addOne, this);
        $('.carousel').carousel();
        return this;
    },

    addOne: function(event, index){
        var indicator = $(document.createElement('li'));
        indicator.attr('data-target', '#carousel-history');
        indicator.attr('data-slide-to', index);
        $('.carousel-indicators').append(indicator);
        var view = new App.Views.Event({model: event});
        this.subviews.push(view);
        this.$('.carousel-inner').append(view.render().el);
        if(index === this.collection.length -1){
            indicator.addClass('active');
            view.$el.addClass('active');
        }
        if(event.get('undoable') === true){
            view.$el.addClass('undoable');
        }
    },

    revert_state: function(){
        var date_selected = this.$('#history_dp').datepicker('getDate').toISOString();
        console.log(date_selected);
    },

    exit: function(){
        for (var index in this.subviews) {
            this.subviews[index].remove();
        }
        this.remove();
    }
});

function addHistoryEvent(title, description, docId, docRev, undoable){
    var mod = new App.Models.Event();
    mod.set({title: title});
    mod.set({description: description});
    mod.set({timestamp: new Date().toISOString()});
    mod.set({doc_id: docId});
    mod.set({doc_rev: docRev});
    mod.set({undoable: undoable});
    console.log(mod.toJSON());
    new App.Collections.Events().create(mod);
}
