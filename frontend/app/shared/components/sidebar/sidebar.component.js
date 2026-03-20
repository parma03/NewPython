/**
 * Sidebar Component Controller
 */
(function () {
  'use strict';

  angular
    .module('AppModule')
    .controller('SidebarController', SidebarController);

  SidebarController.$inject = ['$rootScope', '$state', 'AuthService'];
  function SidebarController($rootScope, $state, AuthService) {
    var vm = this;

    vm.currentUser = $rootScope.currentUser;
    vm.isAdmin = vm.currentUser && vm.currentUser.role === 'admin';

    vm.isActive = function (stateName) {
      return $state.includes(stateName);
    };

    vm.logout = function () {
      AuthService.logout().finally(function () {
        $rootScope.isAuthenticated = false;
        $rootScope.currentUser = null;
        $state.go('login');
      });
    };
  }
})();
