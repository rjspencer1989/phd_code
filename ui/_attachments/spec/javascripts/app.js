describe('application', function(){
    it("should have an application namespace object", function(){
        expect(App).toBeDefined();
    });

    it("should have a model property", function(){
        expect(App.Models).toBeDefined();
    });

    it("should have a collection property", function(){
        expect(App.Collections).toBeDefined();
    });

    it("should have a views property", function(){
        expect(App.Views).toBeDefined();
    });

    it("should have a routers property", function(){
        expect(App.Routers).toBeDefined();
    });

    it("should have db name set", function(){
        expect(Backbone.couch_connector.config.db_name).toEqual("homework-remote");
    });

    it("should have design doc set", function(){
        expect(Backbone.couch_connector.config.ddoc_name).toEqual("homework-remote");
    });

    it("should have global changes turned off", function(){
        expect(Backbone.couch_connector.config.global_changes).toBeFalsy();
    });
});
