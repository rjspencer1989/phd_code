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
        view: 'events',
        changes: true,
        filter: Backbone.couch_connector.config.ddoc_name + '/history'
    }
});

App.Views.Event = Backbone.View.extend({
    tagName: 'dd',
    template: window.JST.history_item,
    initialize: function(){
        this.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    },

    events:{
        'click .undo-button': 'request_undo'
    },
    render: function(){
        data = {};
        data.title = this.model.get('title');
        data.description = this.model.get('description');
        date = new Date(this.model.get('timestamp'));
        data.day = date.getDate();
        data.month = this.months[date.getMonth()];
        this.$el.empty().append(this.template(data));
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
        this.listenTo(this.collection, 'add', this.addOne);
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
        return this;
    },

    addOne: function(event, index){
        var cn = 'pos-left clearfix';
        if (index % 2 === 0) {
            cn = 'pos-right clearfix';
        }
        var view = new App.Views.Event({model: event, className: cn});
        this.subviews.push(view);
        this.$('dl').append(view.render().el);
        if(event.get('undoable') === true){
            view.$el.addClass('undoable');
        }
    },

    revert_state: function(){
        var date_selected = this.$('#history_dp').datepicker('getDate').toISOString();
        newDoc = new App.Models.Rollback();
        newDoc.set({timestamp: date_selected});
        newDoc.save();
    },

    exit: function(){
        for (var index in this.subviews) {
            this.subviews[index].remove();
        }
        this.remove();
    }
});

App.Models.Rollback = Backbone.Model.extend({
    url: this.id,
    defaults: {
        collection: 'request_revert',
        status: 'pending'
    }
});
