/// <reference path="../../../typings/jquery/jquery.d.ts"/>
/// <reference path="../../../typings/backbone/backbone.d.ts"/>
window.App = {
    Models: {},
    Collections: {},
    Views: {},
    Routers: {},
    routerInstance: null
};

Backbone.couch_connector.config.db_name = "config";
Backbone.couch_connector.config.ddoc_name = "homework-remote";
Backbone.couch_connector.config.global_changes = false;

window.setActiveLink = function(element){
    "use strict";
    $("#" + element)
    .parent()
        .siblings()
            .removeClass("active")
        .end()
    .addClass("active");
}
