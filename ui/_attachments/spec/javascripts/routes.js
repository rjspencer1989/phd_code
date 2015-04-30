describe('router', function(){
    var router = null;
    beforeEach(function(){
        router = new App.Routers.Router();
    });

    it('should be defined', function(){
      expect(router).toBeDefined();
    });

    it('should have a list of routes', function(){
       expect(router.routes).toBeDefined();
    });

    it("should have a homepage route", function() {
       expect(router.routes['']).toEqual('home');
    });

    it("should have a login route", function() {
       expect(router.routes.login).toEqual('login');
    });

    it("should have a wifi route", function() {
        expect(router.routes.wifi).toEqual('wifi');
    });

    it("should have a notification route", function() {
        expect(router.routes.notifications).toEqual('notifications');
    });

    it("should have a history route", function() {
        expect(router.routes.history).toEqual('history');
    });

    it("should have a control route", function() {
        expect(router.routes.control).toEqual('controlPanel');
    });
});
