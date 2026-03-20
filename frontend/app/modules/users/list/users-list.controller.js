(function () {
  'use strict';
  angular.module('UsersModule').controller('UsersListController', UsersListController);

  UsersListController.$inject = ['$state', 'UsersService'];
  function UsersListController($state, UsersService) {
    var vm = this;
    vm.users = []; vm.loading = true; vm.error = null; vm.deleteConfirm = null;

    vm.load = function () {
      vm.loading = true;
      UsersService.getAll()
        .then(function (res) { vm.users = res.data.data; vm.total = res.data.total; })
        .catch(function () { vm.error = 'Gagal memuat data user.'; })
        .finally(function () { vm.loading = false; });
    };

    vm.goCreate = function () { $state.go('users.create'); };
    vm.goEdit = function (id) { $state.go('users.edit', { id: id }); };
    vm.confirmDelete = function (u) { vm.deleteConfirm = u; };
    vm.cancelDelete = function () { vm.deleteConfirm = null; };
    vm.doDelete = function () {
      UsersService.delete(vm.deleteConfirm.id)
        .then(function () { vm.deleteConfirm = null; vm.load(); })
        .catch(function (err) {
          vm.error = (err.data && err.data.message) || 'Gagal menghapus user.';
          vm.deleteConfirm = null;
        });
    };

    vm.load();
  }
})();
