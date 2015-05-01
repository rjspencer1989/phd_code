$(function(){
    'use strict';
    var router = new App.Routers.Router();
    App.routerInstance = router;
    Backbone.history.start();
    App.routerInstance.checkSession();
});
