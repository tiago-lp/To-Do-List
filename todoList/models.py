from google.appengine.ext import ndb

class Usuario(ndb.Model):
	keys_tarefas = ndb.IntegerProperty(repeated=True)

	def update(self, data):
		if data.get('operation') == 'add':
			tarefa = Tarefa()
			tarefa.nome = data.get('tarefas')[-1]['nome']
			tarefa.descricao = data.get('tarefas')[-1]['descricao']
			tarefa.prazo = data.get('tarefas')[-1]['prazo']
			key = tarefa.put()
			self.keys_tarefas.append(key.id())

		else:
			tarefa = self.keys_tarefas[(data.get('operation'))]
			self.keys_tarefas.pop(data.get('operation'))
			ndb.Key(Tarefa, tarefa).delete()

	def get_tarefas(self):
		tarefas = []

		if len(self.keys_tarefas) > 0:
			for tarefa in self.keys_tarefas:
				tarefa = Tarefa.get_by_id(tarefa)
				tarefas.append({
					'nome': tarefa.nome, 
					'descricao': tarefa.descricao, 
					'prazo': tarefa.prazo
				})

		return tarefas

class Tarefa(ndb.Model):
	nome = ndb.StringProperty()
	descricao = ndb.StringProperty()
	prazo = ndb.StringProperty()	