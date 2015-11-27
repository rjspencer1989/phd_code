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
};

window.getDateComponents = function(date){
    "use strict";
    var data = {};
    data.day = date.getDate();
    data.month = this.months[date.getMonth()];
    data.year = date.getFullYear();
    data.hour = date.getHours();
    data.hour = ("0" + data.hour).slice(-2);
    data.minute = date.getMinutes();
    data.minute = ("0" + data.minute).slice(-2);
    data.second = date.getSeconds();
    data.second = ("0" + data.second).slice(-2);
    return data;
};
