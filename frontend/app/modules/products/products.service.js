/**
 * Products Service
 */
(function () {
  'use strict';

  angular
    .module('ProductsModule')
    .service('ProductsService', ProductsService);

  ProductsService.$inject = ['$http', 'API_URL'];
  function ProductsService($http, API_URL) {
    var base = API_URL + '/products/';

    this.getAll = function (search) {
      var params = search ? { params: { search: search } } : {};
      return $http.get(base, params);
    };

    this.getById = function (id) {
      return $http.get(base + id + '/');
    };

    this.create = function (data) {
      return $http.post(base, data);
    };

    this.update = function (id, data) {
      return $http.put(base + id + '/', data);
    };

    this.delete = function (id) {
      return $http.delete(base + id + '/');
    };
  }
})();
