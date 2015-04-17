describe("notification registration data", function () {
    model = null;
    collection = null;
    beforeEach(function () {
        model = new App.Models.Notification();
        collection = new App.Collections.Notifications();
    });
    afterEach(function () {
        model = null;
        collection = null;
    });

    it("should have a model defined", function () {
        expect(App.Models.Notification).toBeDefined();
    });

    it("should have sensible default values", function () {
        expect(model.get('collection')).toEqual('notifications');
        expect(model.get('name')).toEqual('');
        expect(model.get('service')).toEqual('');
        expect(model.get('user')).toEqual('');
    });

    it("should have a collection defined", function () {
        expect(App.Collections.Notifications).toBeDefined();
    });

    it("collection should have a model", function () {
        expect(collection.model).toBe(App.Models.Notification);
    });

    it("collection should have a URL", function () {
        expect(collection.url).toBe('notifications');
    });

    it("collection should have a db property with a view", function () {
        expect(collection.db).toEqual({view: 'notifications'});
    });
});
