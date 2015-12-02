RouterConfigApp.Models.Event = Backbone.Model.extend({
    defaults: {
        title: "",
        description: "",
        timestamp: new Date().toISOString(),
        collection: "events",
        undoable: false,
        perform_undo: false
    }
});

RouterConfigApp.Collections.Events = Backbone.Collection.extend({
    url: "events",
    model: RouterConfigApp.Models.Event,
    db: {
        view: "events",
        changes: true,
        filter: Backbone.couch_connector.config.ddoc_name + "/history"
    }
});

Event = Marionette.ItemView.extend({
    tagName: "dd",
    template: window.JST.history_item,
    className: 'clearfix',
    
    initialize: function(options){
        this.isLeft = options.is_left;   
    },

    events: {
        "click .undo-button": "request_undo",
        "click .revert-button": "revert_state"
    },
    
    serializeData: function(){
        "use strict";
        var date = new Date(this.model.get("timestamp"));
        var components = getDateComponents(date);
        components.title = this.model.get("title");
        components.description = this.model.get("description");
        return components;
    },
    
    onRender: function(){
        if (this.isLeft) {
            this.$el.removeClass('pos-right').addClass('pos-left');
        } else {
            this.$el.removeClass('pos-left').addClass('pos-right');
        }
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
        var newDoc = new RouterConfigApp.Models.Rollback();
        newDoc.set({timestamp: this.model.get("timestamp")});
        newDoc.save();
    }
});

Events = Marionette.CompositeView.extend({
    tagName: "div",
    className: "col-md-12",
    template: window.JST.history,
    childView: Event,
    childViewContainer: 'dl',
    
    childViewOptions: function(model, index){
        var isLeft = (index % 2 === 0);
        return {
            is_left: isLeft
        };
    },
    
    events: {
        "submit #revert_datepicker_form": "revertDatepicker"   
    },

    onRender: function(){
        "use strict";
        window.setActiveLink("history-link");
        this.$("#datepicker").datepicker();
        this.$("#datepicker").datepicker("option", "dateFormat", "yy-mm-dd");
        return this;
    },
    
    revertDatepicker: function(event){
        "use strict";
        event.preventDefault();
        var newDoc = new RouterConfigApp.Models.Rollback();
        var ts = this.$("#datepicker").val();
        ts += "T00:00:00Z";
        newDoc.set({timestamp: ts});
        newDoc.save();
    }
});

RouterConfigApp.Models.Rollback = Backbone.Model.extend({
    url: this.id,
    defaults: {
        collection: "request_revert",
        status: "pending"
    }
});
