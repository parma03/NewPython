/**
 * AppModule - Root AngularJS Application
 * Routing dengan ui-router, role-based guard
 */
(function () {
  'use strict';

  angular
    .module('AppModule', [
      'ui.router',
      'AuthModule',
      'DashboardModule',
      'ProductsModule',
      'UsersModule',
    ])
    .constant('API_URL', 'http://localhost:8000/api/v1')
    .config(RouterConfig)
    .run(AppRun);

  /* ─── ROUTER CONFIG ─────────────────────────────────────────────────────── */
  RouterConfig.$inject = ['$stateProvider', '$urlRouterProvider', '$locationProvider'];
  function RouterConfig($stateProvider, $urlRouterProvider, $locationProvider) {

    // Default redirect ke login
    $urlRouterProvider.otherwise('/login');

    $stateProvider
      // ── Auth ──────────────────────────────────────────────────────────────
      .state('login', {
        url: '/login',
        templateUrl: 'app/modules/auth/login/login.html',
        controller: 'LoginController',
        controllerAs: 'vm',
        data: { requireAuth: false }
      })
      .state('register', {
        url: '/register',
        templateUrl: 'app/modules/auth/register/register.html',
        controller: 'RegisterController',
        controllerAs: 'vm',
        data: { requireAuth: false }
      })

      // ── Dashboard ─────────────────────────────────────────────────────────
      .state('dashboard', {
        url: '/dashboard',
        templateUrl: 'app/modules/dashboard/dashboard.html',
        controller: 'DashboardController',
        controllerAs: 'vm',
        data: { requireAuth: true, roles: ['admin', 'pelanggan'] }
      })

      // ── Products (Admin Only) ─────────────────────────────────────────────
      .state('products', {
        url: '/products',
        templateUrl: 'app/modules/products/list/products-list.html',
        controller: 'ProductsListController',
        controllerAs: 'vm',
        data: { requireAuth: true, roles: ['admin'] }
      })
      .state('products.create', {
        url: '/products/create',
        templateUrl: 'app/modules/products/form/products-form.html',
        controller: 'ProductsFormController',
        controllerAs: 'vm',
        data: { requireAuth: true, roles: ['admin'] }
      })
      .state('products.edit', {
        url: '/products/edit/:id',
        templateUrl: 'app/modules/products/form/products-form.html',
        controller: 'ProductsFormController',
        controllerAs: 'vm',
        data: { requireAuth: true, roles: ['admin'] }
      })

      // ── Users (Admin Only) ────────────────────────────────────────────────
      .state('users', {
        url: '/users',
        templateUrl: 'app/modules/users/list/users-list.html',
        controller: 'UsersListController',
        controllerAs: 'vm',
        data: { requireAuth: true, roles: ['admin'] }
      })
      .state('users.create', {
        url: '/users/create',
        templateUrl: 'app/modules/users/form/users-form.html',
        controller: 'UsersFormController',
        controllerAs: 'vm',
        data: { requireAuth: true, roles: ['admin'] }
      })
      .state('users.edit', {
        url: '/users/edit/:id',
        templateUrl: 'app/modules/users/form/users-form.html',
        controller: 'UsersFormController',
        controllerAs: 'vm',
        data: { requireAuth: true, roles: ['admin'] }
      });
  }

  /* ─── APP RUN (Route Guard) ─────────────────────────────────────────────── */
  AppRun.$inject = ['$rootScope', '$state', 'AuthService'];
  function AppRun($rootScope, $state, AuthService) {

    // Init state dari localStorage
    var user = AuthService.getCurrentUser();
    if (user) {
      $rootScope.isAuthenticated = true;
      $rootScope.currentUser = user;
    } else {
      $rootScope.isAuthenticated = false;
      $rootScope.currentUser = null;
    }

    $rootScope.$on('$stateChangeStart', function (event, toState) {
      var requireAuth = toState.data && toState.data.requireAuth;
      var allowedRoles = toState.data && toState.data.roles;

      // Jika sudah login dan mau ke login/register → redirect ke dashboard
      if (!requireAuth && $rootScope.isAuthenticated) {
        event.preventDefault();
        $state.go('dashboard');
        return;
      }

      // Jika belum login dan route butuh auth → ke login
      if (requireAuth && !$rootScope.isAuthenticated) {
        event.preventDefault();
        $state.go('login');
        return;
      }

      // Cek role permission
      if (requireAuth && allowedRoles && $rootScope.currentUser) {
        var userRole = $rootScope.currentUser.role;
        if (allowedRoles.indexOf(userRole) === -1) {
          event.preventDefault();
          $state.go('dashboard');
          return;
        }
      }
    });

    // Set page title pada setiap navigasi
    $rootScope.$on('$stateChangeSuccess', function (event, toState) {
      var titles = {
        'dashboard': 'Dashboard',
        'products': 'Kelola Barang',
        'products.create': 'Tambah Barang',
        'products.edit': 'Edit Barang',
        'users': 'Kelola User',
        'users.create': 'Tambah User',
        'users.edit': 'Edit User',
      };
      $rootScope.pageTitle = titles[toState.name] || 'AppSystem';
    });
  }

})();
