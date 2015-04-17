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

    it("model should have a set of defaults", function () {
        expect(model.get('action')).toEqual('');
        expect(model.get('collection')).toEqual('devices');
        expect(model.get('device_name')).toEqual('');
        expect(model.get('host_name')).toEqual('');
        expect(model.get('ip_address')).toEqual('');
        expect(model.get('lease_action')).toEqual('add');
        expect(model.get('mac_address')).toEqual('');
        expect(model.get('name')).toEqual('');
        expect(model.get('state')).toEqual('pending');
        expect(model.get('device_type')).toEqual('');
        expect(model.get('notification_service')).toEqual('');
        expect(model.get('timestamp')).toBeDefined();
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
        expect(collection.db).toEqual({view:'control'});
    });
});
