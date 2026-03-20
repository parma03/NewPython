/**
 * HTTP Interceptor - Auto-attach JWT Bearer token
 * Fix: skip auth endpoints untuk mencegah logout loop saat login gagal
 */
(function () {
  "use strict";

  angular
    .module("AppModule")
    .factory("AuthInterceptor", AuthInterceptor)
    .config(function ($httpProvider) {
      $httpProvider.interceptors.push("AuthInterceptor");
    });

  AuthInterceptor.$inject = ["$q", "$injector"];
  function AuthInterceptor($q, $injector) {
    var AUTH_URLS = [
      "/auth/login/",
      "/auth/register/",
      "/auth/token/refresh/",
      "/auth/logout/",
    ];

    function isAuthUrl(url) {
      return AUTH_URLS.some(function (path) {
        return url && url.indexOf(path) !== -1;
      });
    }

    return {
      request: function (config) {
        var token = localStorage.getItem("access_token");
        if (token && !isAuthUrl(config.url)) {
          config.headers.Authorization = "Bearer " + token;
        }
        return config;
      },
      responseError: function (rejection) {
        if (rejection.status === 401 && !isAuthUrl(rejection.config.url)) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          localStorage.removeItem("current_user");

          var $rootScope = $injector.get("$rootScope");
          $rootScope.isAuthenticated = false;
          $rootScope.currentUser = null;

          var $state = $injector.get("$state");
          $state.go("login");
        }
        return $q.reject(rejection);
      },
    };
  }
})();
