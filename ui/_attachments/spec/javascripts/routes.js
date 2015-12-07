describe('router', function(){
    var router = null;
    beforeEach(function(){
        router = new Router();
    });

    it('should be defined', function(){
      expect(router).toBeDefined();
    });

    it('should have a list of routes', function(){
       expect(router.appRoutes).toBeDefined();
    });

    it("should have a homepage route", function() {
       expect(router.appRoutes['']).toEqual('home');
    });

    it("should have a wifi route", function() {
        expect(router.appRoutes.wifi).toEqual('wifi');
    });

    it("should have a notification route", function() {
        expect(router.appRoutes.notifications).toEqual('notifications');
    });

    it("should have a history route", function() {
        expect(router.appRoutes.history).toEqual('history');
    });

    it("should have a control route", function() {
        expect(router.appRoutes.devices).toEqual('controlPanel');
    });
});
