/**
 * Auth Service - Handles authentication & token storage
 */
(function () {
  'use strict';

  angular
    .module('AuthModule')
    .service('AuthService', AuthService);

  AuthService.$inject = ['$http', '$rootScope', 'API_URL'];
  function AuthService($http, $rootScope, API_URL) {

    this.login = function (credentials) {
      return $http.post(API_URL + '/auth/login/', credentials)
        .then(function (response) {
          var data = response.data;
          localStorage.setItem('access_token', data.tokens.access);
          localStorage.setItem('refresh_token', data.tokens.refresh);
          localStorage.setItem('current_user', JSON.stringify(data.user));
          $rootScope.isAuthenticated = true;
          $rootScope.currentUser = data.user;
          return data;
        });
    };

    this.register = function (userData) {
      return $http.post(API_URL + '/auth/register/', userData)
        .then(function (response) {
          var data = response.data;
          localStorage.setItem('access_token', data.tokens.access);
          localStorage.setItem('refresh_token', data.tokens.refresh);
          localStorage.setItem('current_user', JSON.stringify(data.user));
          $rootScope.isAuthenticated = true;
          $rootScope.currentUser = data.user;
          return data;
        });
    };

    this.logout = function () {
      var refreshToken = localStorage.getItem('refresh_token');
      var promise = $http.post(API_URL + '/auth/logout/', { refresh: refreshToken })
        .catch(function () { /* ignore errors */ });

      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('current_user');
      $rootScope.isAuthenticated = false;
      $rootScope.currentUser = null;
      return promise;
    };

    this.getCurrentUser = function () {
      var user = localStorage.getItem('current_user');
      return user ? JSON.parse(user) : null;
    };

    this.isAuthenticated = function () {
      return !!localStorage.getItem('access_token');
    };
  }
})();
