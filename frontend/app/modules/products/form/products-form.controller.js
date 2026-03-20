/**
 * Products Form Controller - Create & Edit
 */
(function () {
  'use strict';

  angular
    .module('ProductsModule')
    .controller('ProductsFormController', ProductsFormController);

  ProductsFormController.$inject = ['$state', '$stateParams', 'ProductsService'];
  function ProductsFormController($state, $stateParams, ProductsService) {
    var vm = this;

    vm.isEdit = !!$stateParams.id;
    vm.loading = false;
    vm.error = null;
    vm.formData = { name: '', description: '', price: '', stock: 0, is_active: true };

    if (vm.isEdit) {
      vm.loading = true;
      ProductsService.getById($stateParams.id)
        .then(function (res) { vm.formData = res.data; })
        .catch(function () { vm.error = 'Gagal memuat data barang.'; })
        .finally(function () { vm.loading = false; });
    }

    vm.save = function () {
      vm.loading = true;
      vm.error = null;

      var promise = vm.isEdit
        ? ProductsService.update($stateParams.id, vm.formData)
        : ProductsService.create(vm.formData);

      promise
        .then(function () { $state.go('products'); })
        .catch(function (err) {
          if (err.data) {
            var msgs = [];
            angular.forEach(err.data, function (v, k) {
              msgs.push(k + ': ' + (Array.isArray(v) ? v.join(', ') : v));
            });
            vm.error = msgs.join(' | ');
          } else {
            vm.error = 'Terjadi kesalahan. Coba lagi.';
          }
        })
        .finally(function () { vm.loading = false; });
    };

    vm.cancel = function () { $state.go('products'); };
  }
})();
