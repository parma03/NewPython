/**
 * Login Controller
 */
(function () {
  'use strict';

  angular
    .module('AuthModule')
    .controller('LoginController', LoginController);

  LoginController.$inject = ['$state', 'AuthService'];
  function LoginController($state, AuthService) {
    var vm = this;

    vm.credentials = { username: '', password: '' };
    vm.loading = false;
    vm.error = null;

    vm.login = function () {
      if (!vm.credentials.username || !vm.credentials.password) {
        vm.error = 'Username dan password wajib diisi.';
        return;
      }
      vm.loading = true;
      vm.error = null;

      AuthService.login(vm.credentials)
        .then(function () {
          $state.go('dashboard');
        })
        .catch(function (err) {
          vm.error = (err.data && err.data.message) || 'Login gagal. Periksa kembali kredensial Anda.';
        })
        .finally(function () {
          vm.loading = false;
        });
    };
  }
})();
