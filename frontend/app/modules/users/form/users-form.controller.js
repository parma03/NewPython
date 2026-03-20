(function () {
  'use strict';
  angular.module('UsersModule').controller('UsersFormController', UsersFormController);

  UsersFormController.$inject = ['$state', '$stateParams', 'UsersService'];
  function UsersFormController($state, $stateParams, UsersService) {
    var vm = this;
    vm.isEdit = !!$stateParams.id;
    vm.loading = false; vm.error = null;
    vm.formData = { username: '', email: '', password: '', role: 'pelanggan', is_active: true };

    if (vm.isEdit) {
      vm.loading = true;
      UsersService.getById($stateParams.id)
        .then(function (res) { vm.formData = res.data; vm.formData.password = ''; })
        .catch(function () { vm.error = 'Gagal memuat data user.'; })
        .finally(function () { vm.loading = false; });
    }

    vm.save = function () {
      vm.loading = true; vm.error = null;
      var data = angular.copy(vm.formData);
      if (vm.isEdit && !data.password) delete data.password;

      var promise = vm.isEdit
        ? UsersService.update($stateParams.id, data)
        : UsersService.create(data);

      promise
        .then(function () { $state.go('users'); })
        .catch(function (err) {
          var msgs = [];
          if (err.data) angular.forEach(err.data, function(v, k) { msgs.push(k + ': ' + (Array.isArray(v) ? v.join(', ') : v)); });
          vm.error = msgs.length ? msgs.join(' | ') : 'Terjadi kesalahan.';
        })
        .finally(function () { vm.loading = false; });
    };

    vm.cancel = function () { $state.go('users'); };
  }
})();
