var App = {
    Models : {},
    Collections : {},
    Views : {},
    Routers : {},
    userCtx: null,
    routerInstance : null
};

Backbone.couch_connector.config.db_name = "config";
Backbone.couch_connector.config.ddoc_name = "homework-remote";
Backbone.couch_connector.config.global_changes = false;

function setActiveLink(element){
    'use strict';
    $('#' + element)
    .parent()
        .siblings()
            .removeClass('active')
        .end()
    .addClass('active');
}
