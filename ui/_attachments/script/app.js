RouterConfigApp = new Marionette.Application();

RouterConfigApp.on('start', function(){
    RouterConfigApp.router = new Router();
    RouterConfigApp.root = new RootView();
    RouterConfigApp.root.render();
    var linkCollection = new RouterConfigApp.Collections.Links(RouterConfigApp.links);
    var LinkView = new Links({collection: linkCollection});
    RouterConfigApp.root.nav.show(LinkView); 
    Backbone.history.start(); 
});

RootView = Marionette.LayoutView.extend({
    el: 'body',
    template: JST.main,
    regions: {
        'nav': '#header',
        'main': '#main-row'
    }
});

RouterConfigApp.links = [
    {
        title: "Home",
        link: "index.html/#/home",
        icon: "glyphicon-home",
        tag_id: "home-link"
    }, {
        title: "Wi-Fi",
        link: "index.html/#/wifi",
        icon: "glyphicon-signal",
        tag_id: "wifi-link"
    }, {
        title: "Notifications",
        link: "index.html/#/notifications",
        icon: "glyphicon-inbox",
        tag_id: "registrations-link"
    }, {
        title: "Devices",
        icon: "glyphicon-phone",
        link: "index.html/#/devices",
        tag_id: "devices_link"
    }, {
        title: "History",
        icon: "glyphicon-time",
        link: "index.html/#/history",
        tag_id: "history_link"
    }
];

RouterConfigApp.Models = {};
RouterConfigApp.Collections = {};

RouterConfigApp.Models.Link = Backbone.Model.extend({});
RouterConfigApp.Collections.Links = Backbone.Collection.extend({
    model: RouterConfigApp.Models.Link
});

Link = Marionette.ItemView.extend({
    template: JST.link,
    tagName: 'li'
});

Links = Marionette.CompositeView.extend({
    childView: Link,
    childViewContainer: '#navbar-collapse > ul',
    template: JST.nav
});

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

window.getDateComponents = function(d){
    "use strict";
    var date = new Date(d);
    var data = {};
    var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    data.day = date.getDate();
    data.month = months[date.getMonth()];
    data.year = date.getFullYear();
    data.hour = date.getHours();
    data.hour = ("0" + data.hour).slice(-2);
    data.minute = date.getMinutes();
    data.minute = ("0" + data.minute).slice(-2);
    data.second = date.getSeconds();
    data.second = ("0" + data.second).slice(-2);
    return data;
};

window.formatDate = function(date){
    var d = new Date(date);
    var components = getDateComponents(d);
    return components.day + "/" + components.month + "/" +
        components.year + " " + components.hour + ":" +
        components.minute + ":" + components.second;
};