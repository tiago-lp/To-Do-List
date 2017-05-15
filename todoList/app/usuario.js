"use strict";
function Usuario(data) {
    data = data || {}
    _.extend(this, data)
};

Usuario.prototype.del_tarefa = function(index) {
    this.tarefas.splice(index, 1);
};

Usuario.prototype.add_tarefa = function(tarefa) {
    this.tarefas.push(tarefa);
};