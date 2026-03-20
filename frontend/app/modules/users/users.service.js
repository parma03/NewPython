(function () {
  'use strict';
  angular.module('UsersModule').service('UsersService', UsersService);

  UsersService.$inject = ['$http', 'API_URL'];
  function UsersService($http, API_URL) {
    var base = API_URL + '/users/';
    this.getAll = function () { return $http.get(base); };
    this.getById = function (id) { return $http.get(base + id + '/'); };
    this.create = function (data) { return $http.post(base, data); };
    this.update = function (id, data) { return $http.put(base + id + '/', data); };
    this.delete = function (id) { return $http.delete(base + id + '/'); };
  }
})();
