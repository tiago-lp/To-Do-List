"use strict";
var vm;
(function() {
  var app = angular.module('app', ['ngMaterial', 'ui.router']);
  
  app.config(function($mdIconProvider, $urlRouterProvider, $stateProvider) {
    $mdIconProvider.fontSet('md', 'material-icons');
    // configurações de states
    $urlRouterProvider.otherwise('/');
    $stateProvider
    .state('app', {
        'abstract': true,
        'views': {
            'header': {
                templateUrl: 'header.html'
            }
        }
    })
    .state('app.home', {
        'url': '/',
        'views': {
            'contents@': {
                templateUrl: 'home.html',
                controller: 'TarefasCtrl as vm'
            },
        }
    })
    .state('app.about', {
        'url': '/about',
        'views': {
            'contents@': {
                templateUrl: 'about.html'
            },
        }
    })
    .state('app.cadtarefas', {
        'url': '/ct',
        'views': {
            'contents@': {
                templateUrl: 'cadtarefas.html',
                controller: 'TarefasCtrl as vm'
            },
        }
    })
  });

  app.controller('AppCtrl', function AppCtrl(UserService) {
        vm = this;
        vm.save_user = UserService.save;
        Object.defineProperties(vm, {
            user: {
                get: function () { return UserService.user; },
                set: function (data) { UserService.user = data; }
            },
            eh_perfil: {
                get: function () { return vm.user instanceof Usuario; }
            }
        })
    });
})();