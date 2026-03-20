/**
 * Dashboard Controller - Analytics
 */
(function () {
  'use strict';

  angular
    .module('DashboardModule')
    .controller('DashboardController', DashboardController);

  DashboardController.$inject = ['$http', '$rootScope', 'API_URL'];
  function DashboardController($http, $rootScope, API_URL) {
    var vm = this;

    vm.stats = null;
    vm.loading = true;
    vm.error = null;
    vm.currentUser = $rootScope.currentUser;
    vm.isAdmin = vm.currentUser && vm.currentUser.role === 'admin';

    // Greeting based on time
    var hour = new Date().getHours();
    if (hour < 12) vm.greeting = 'Selamat Pagi';
    else if (hour < 17) vm.greeting = 'Selamat Siang';
    else vm.greeting = 'Selamat Malam';

    function loadStats() {
      $http.get(API_URL + '/auth/dashboard-stats/')
        .then(function (res) {
          vm.stats = res.data;
        })
        .catch(function () {
          vm.error = 'Gagal memuat data statistik.';
        })
        .finally(function () {
          vm.loading = false;
        });
    }

    loadStats();
  }
})();
