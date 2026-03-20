/**
 * Register Controller
 */
(function () {
  'use strict';

  angular
    .module('AuthModule')
    .controller('RegisterController', RegisterController);

  RegisterController.$inject = ['$state', 'AuthService'];
  function RegisterController($state, AuthService) {
    var vm = this;

    vm.formData = { username: '', email: '', password: '', password_confirm: '', role: 'pelanggan' };
    vm.loading = false;
    vm.error = null;

    vm.register = function () {
      if (!vm.formData.username || !vm.formData.email || !vm.formData.password) {
        vm.error = 'Semua field wajib diisi.';
        return;
      }
      if (vm.formData.password !== vm.formData.password_confirm) {
        vm.error = 'Password tidak cocok.';
        return;
      }
      vm.loading = true;
      vm.error = null;

      AuthService.register(vm.formData)
        .then(function () {
          $state.go('dashboard');
        })
        .catch(function (err) {
          if (err.data) {
            var messages = [];
            angular.forEach(err.data, function (val, key) {
              messages.push(Array.isArray(val) ? val.join(', ') : val);
            });
            vm.error = messages.join(' | ');
          } else {
            vm.error = 'Registrasi gagal. Coba lagi.';
          }
        })
        .finally(function () {
          vm.loading = false;
        });
    };
  }
})();
