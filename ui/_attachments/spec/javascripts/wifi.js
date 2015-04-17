describe("wifi data", function () {
    model = null;
    collection = null;
    beforeEach(function () {
        model = new App.Models.Wifi();
        collection = new App.Collections.Wifi();
    });

    afterEach(function () {
        model = null;
        collection = null;
    });

    it("should have a model property", function () {
        expect(App.Models.Wifi).toBeDefined();
    });

    it("model should contain a set of defaults", function () {
        expect(model.defaults).toBeDefined();
    });

    it("defaults should have a collection property set to wifi", function () {
        expect(model.get('collection')).toEqual('wifi');
    });

    it("defaults should have a list of properties", function () {
        expect(model.get('status')).toEqual('pending');
        expect(model.get('ssid')).toEqual('');
        expect(model.get('password')).toEqual('');
        expect(model.get('encryption_type')).toEqual('wpa');
        expect(model.get('password_type')).toEqual('txt');
        expect(model.get('mode')).toEqual('n');
        expect(model.defaults.channel).toEqual(1);
    });

    it("should have a collection", function () {
        expect(App.Collections.Wifi).toBeDefined();
    });

    it("collection should have a model property", function () {
        expect(collection.model).toBeDefined();
    });

    it("collection should have a url property", function () {
        expect(collection.url).toBeDefined();
    });

    it("collection should have a db property with a view", function () {
        expect(collection.db.view).toBeDefined();
    });
});
