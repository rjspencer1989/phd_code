describe("control panel", function () {
    var collection = null;
    var model = null;
    beforeEach(function () {
        collection = new App.Collections.Devices();
        model = new App.Models.Device();
    });
    it("should have a device model", function () {
        expect(App.Models.Device).toBeDefined();
    });

    it("collection should be defined", function () {
        expect(App.Collections.Devices).toBeDefined();
    });

    it("collection should have a model", function () {
        expect(collection.model).toEqual(App.Models.Device);
    });

    it("collection should have a url", function () {
        expect(collection.url).toEqual('devices');
    });

    it("collection should have a db and view", function () {
        expect(collection.db).toEqual({view:'control', changes: true, filter: 'homework-remote/devices_ui'});
    });

    it("model should save", function () {
        val = collection.create(model);
        console.log(val.toJSON());
        expect(val).not.toBeNull();
    });
});
