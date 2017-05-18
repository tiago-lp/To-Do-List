"use strict";
function Usuario(data) {
    data = data || {}
    _.extend(this, data)
};

Usuario.prototype.del_tarefa = function(tarefa) {
	_.remove(this.tarefas, function(tarefa) {
		return tarefa['id'] == tarefa['id']
	});
};

Usuario.prototype.add_tarefa = function(tarefa) {
    this.tarefas.push(tarefa);
};