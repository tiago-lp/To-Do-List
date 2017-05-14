var vm;

(function() {
	var app = angular.module('app');
	
	app.controller('TarefasCtrl', function TarefasCtrl(UserService, $mdDialog) {
		vm = this;
		vm.save_user = UserService.save;
        vm.tarefa = {
        	nome: '',
        	descricao: '',
        	prazo: ''
        };
        Object.defineProperties(vm, {
            user: {
                get: function () { return UserService.user; },
                set: function (data) { UserService.user = data; }
            }
        })

        vm.del_tarefa = function(index, ev) {
          vm.showConfirm(ev, 'A tarefa ' + vm.user.tarefas[index].nome + ' será finalizada', index);
          vm.save_user(index);
        };

        vm.add_tarefa = function(ev) {
          vm.user.add_tarefa(vm.tarefa);
          vm.showAlert(ev,'A tarefa ' + vm.tarefa.nome + ' foi salva com sucesso');
          vm.save_user('add');
          vm.clear();
        };

        vm.clear = function clear() {
          vm.tarefa = {
          	nome: '',
        	descricao: '',
        	prazo: ''
          };
        };

        vm.showAlert = function showAlert(ev, message) {
          $mdDialog.show(
          $mdDialog.alert()
            .parent(angular.element(document.querySelector('#popupContainer')))
            .clickOutsideToClose(true)
            .title('Sucesso')
            .textContent(message)
            .ariaLabel('Alert Dialog Demo')
            .ok('Entendi')
            .targetEvent(ev)
          );
        };

        vm.showConfirm = function showConfirm(ev, message, index) {
          var confirm = $mdDialog.confirm()
              .title('Deseja finalizar tarefa?')
              .textContent(message)
              .ariaLabel('Lucky day')
              .targetEvent(ev)
              .ok('Sim')
              .cancel('Cancelar');

          $mdDialog.show(confirm).then(function() {
            vm.showAlert(ev, 'Tarefa finalizada com sucesso');
            vm.user.del_tarefa(index);
          });
        };
	});
})();