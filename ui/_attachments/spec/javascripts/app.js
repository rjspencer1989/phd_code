describe('application', function(){
    it("should have an application namespace object", function(){
        expect(RouterConfigApp).toBeDefined();
    });

    it("should have a model property", function(){
        expect(RouterConfigApp.Models).toBeDefined();
    });

    it("should have a collection property", function(){
        expect(RouterConfigApp.Collections).toBeDefined();
    });

    it("should have db name set", function(){
        expect(Backbone.couch_connector.config.db_name).toEqual("config");
    });

    it("should have design doc set", function(){
        expect(Backbone.couch_connector.config.ddoc_name).toEqual("homework-remote");
    });

    it("should have global changes turned off", function(){
        expect(Backbone.couch_connector.config.global_changes).toBeFalsy();
    });
});
