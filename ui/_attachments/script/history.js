window.App.Models.Event = Backbone.Model.extend({
    defaults: {
        title: "",
        description: "",
        timestamp: new Date().toISOString(),
        collection: "events",
        doc_id: "",
        doc_rev: "",
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
    initialize: function(){
        "use strict";
        this.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    },

    events: {
        "click .undo-button": "request_undo"
    },
    render: function(){
        "use strict";
        var data = {};
        data.title = this.model.get("title");
        data.description = this.model.get("description");
        var date = new Date(this.model.get("timestamp"));
        data.day = date.getDate();
        data.month = this.months[date.getMonth()];
        data.year = date.getFullYear();
        data.hour = date.getHours();
        data.hour = ("0" + data.hour).slice(-2);
        data.minute = date.getMinutes();
        data.minute = ("0" + data.minute).slice(-2);
        data.second = date.getSeconds();
        data.second = ("0" + data.second).slice(-2);
        this.$el.empty().append(this.template(data));
        return this;
    },
    request_undo: function(){
        "use strict";
        this.model.set({perform_undo: true});
        this.model.save();
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
        this.listenTo(this.collection, "add", this.addOne);
        this.collection.fetch({reset: true, descending: true});
        this.subviews = [];
    },

    events: {
        "click .revert-button": "revert_state"
    },

    render: function(){
        "use strict";
        this.$el.html(this.template());
        $("#main-row").empty().append(this.el);
        this.$(".input-group.date").datepicker({
            todayBtn: true,
            todayHighlight: true,
            format: "dd-mm-yyyy",
            endDate: "0d",
            container: ".jump_date",
            orientation: "top"
        }).on('show', function(e){
            console.log($(this).parent().find('.datepicker'));
        });
        window.setActiveLink("history-link");
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

    revert_state: function(){
        "use strict";
        var date_selected = this.$("#history_dp").datepicker("getDate").toISOString();
        var newDoc = new window.App.Models.Rollback();
        newDoc.set({timestamp: date_selected});
        newDoc.save();
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
