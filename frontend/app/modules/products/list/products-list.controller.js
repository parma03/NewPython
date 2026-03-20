/**
 * Products List Controller
 */
(function () {
  'use strict';

  angular
    .module('ProductsModule')
    .controller('ProductsListController', ProductsListController);

  ProductsListController.$inject = ['$state', 'ProductsService'];
  function ProductsListController($state, ProductsService) {
    var vm = this;
    vm.products = [];
    vm.loading = true;
    vm.error = null;
    vm.searchQuery = '';
    vm.deleteConfirm = null;

    vm.load = function () {
      vm.loading = true;
      ProductsService.getAll(vm.searchQuery)
        .then(function (res) { vm.products = res.data.data; vm.total = res.data.total; })
        .catch(function () { vm.error = 'Gagal memuat data barang.'; })
        .finally(function () { vm.loading = false; });
    };

    vm.search = function () { vm.load(); };

    vm.goCreate = function () { $state.go('products.create'); };
    vm.goEdit = function (id) { $state.go('products.edit', { id: id }); };

    vm.confirmDelete = function (product) { vm.deleteConfirm = product; };
    vm.cancelDelete = function () { vm.deleteConfirm = null; };

    vm.doDelete = function () {
      if (!vm.deleteConfirm) return;
      ProductsService.delete(vm.deleteConfirm.id)
        .then(function () { vm.deleteConfirm = null; vm.load(); })
        .catch(function () { vm.error = 'Gagal menghapus produk.'; vm.deleteConfirm = null; });
    };

    vm.load();
  }
})();
