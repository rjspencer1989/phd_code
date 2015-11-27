window.App.Models.Event = Backbone.Model.extend({
    defaults: {
        title: "",
        description: "",
        timestamp: new Date().toISOString(),
        collection: "events",
        undoable: false,
        perform_undo: false
    }
});

window.App.Collections.Events = Backbone.Collection.extend({
    url: "events",
    model: window.App.Models.Event,
    db: {
        view: "events",
        changes: true,
        filter: Backbone.couch_connector.config.ddoc_name + "/history"
    }
});

window.App.Views.Event = Backbone.View.extend({
    tagName: "dd",
    template: window.JST.history_item,

    events: {
        "click .undo-button": "request_undo",
        "click .revert-button": "revert_state"
    },
    render: function(){
        "use strict";
        var date = new Date(this.model.get("timestamp"));
        var data = getDateComponents();
        data.title = this.model.get("title");
        data.description = this.model.get("description");
        this.$el.empty().append(this.template(data));
        return this;
    },
    request_undo: function(){
        "use strict";
        var should_undo = true;
        var docs = this.model.get('docs');
        if(docs.length === 1){
            if (docs[0].doc_collection === 'devices' && this.model.get('prompt') === true){
                if(!window.confirm("This is a new device. Undoing this change will make your router forget about the device. Do you wish to continue?")){
                    should_undo = false;
                }
            }
        }

        if(should_undo){
            this.model.set({perform_undo: true});
            this.model.save();
        }
    },
    revert_state: function(){
        "use strict";
        var newDoc = new window.App.Models.Rollback();
        newDoc.set({timestamp: this.model.get("timestamp")});
        newDoc.save();
    }
});

window.App.Views.Events = Backbone.View.extend({
    tagName: "div",
    className: "col-md-12",
    template: window.JST.history,
    collection: new window.App.Collections.Events(),
    initialize: function(){
        "use strict";
        this.listenTo(this.collection, "reset", this.render);
        this.listenTo(this.collection, "add", this.add_event);
        this.collection.fetch({reset: true, descending: true});
        this.subviews = [];
    },

    add_event: function(){
        "use strict";
        console.log(this);
        this.collection.fetch({reset: true, descending: true});
    },

    render: function(){
        "use strict";
        this.$el.html(this.template());
        $("#main-row").empty().append(this.el);
        window.setActiveLink("history-link");
        this.$(".date-picker").datepicker();
        this.collection.each(this.addOne, this);
        return this;
    },

    addOne: function(event, index){
        "use strict";
        var cn = "pos-left clearfix";
        if (index % 2 === 0) {
            cn = "pos-right clearfix";
        }
        var view = new window.App.Views.Event({model: event, className: cn});
        this.subviews.push(view);
        this.$("dl").append(view.render().el);
        if(event.get("undoable") === true){
            view.$el.addClass("undoable");
        }
    },

    exit: function(){
        "use strict";
        for (var index in this.subviews) {
            this.subviews[index].remove();
        }
        this.remove();
    }
});

window.App.Models.Rollback = Backbone.Model.extend({
    url: this.id,
    defaults: {
        collection: "request_revert",
        status: "pending"
    }
});
