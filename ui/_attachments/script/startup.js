$(function(){
    'use strict';
    var router = new App.Routers.Router();
    App.routerInstance = router;
    Backbone.history.start();
    $.couch.session({
        success: function (data) {
            console.log(data);
            App.userCtx = data.userCtx;
        }
    });
});
