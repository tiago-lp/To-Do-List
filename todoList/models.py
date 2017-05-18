from google.appengine.ext import ndb
from google.appengine.api import mail
import datetime

class Usuario(ndb.Model):
	keys_tarefas = ndb.IntegerProperty(repeated=True)

	def update(self, data):
		if data.get('operation') == 'add':
			self.add_tarefa(data)

		else:
			self.del_tarefa(data)

		self.put()
		tarefas_update = {
			"tarefas": self.get_tarefas()
		}
		return tarefas_update

	def add_tarefa(self, data):
		tarefa = Tarefa()
		tarefa.nome = data.get('tarefas')[-1]['nome']
		tarefa.descricao = data.get('tarefas')[-1]['descricao']
		tarefa.prazo = data.get('tarefas')[-1]['prazo']
		key = tarefa.put()
		self.keys_tarefas.append(key.id())

	def del_tarefa(self, data):
		tarefaID = data.get('operation')
		self.keys_tarefas.remove(tarefaID)
		ndb.Key(Tarefa, tarefaID).delete()

	def get_tarefas(self):
		tarefas = []

		if len(self.keys_tarefas) > 0:
			for tarefaID in self.keys_tarefas:
				tarefa = Tarefa.get_by_id(tarefaID)
				tarefas.append({
					'nome': tarefa.nome, 
					'descricao': tarefa.descricao, 
					'prazo': tarefa.prazo,
					'id' : tarefaID
				})

		return tarefas

	def get_data(self):
		data = {
			"email": self.key.id(),
			"usuario": self.to_dict(),
			"tarefas": self.get_tarefas()
		}

		return data

	def send_email(self):
		expirando = []
		for tarefaID in self.keys_tarefas:
			tarefa = Tarefa.get_by_id(tarefaID)
			if tarefa.expirando:
				expirando.append('Sem nome' if len(tarefa.nome) == 0 else tarefa.nome)

		if len(expirando) > 0:
			num_tarefas = str(len(expirando))
			tarefas = ', '.join(expirando)
			message = 'A(s) seguinte(s) tarefa(s) esta(ao) expirando: %s' % tarefas
			mail.send_mail(
				sender='tiago.pereira@ccc.ufcg.edu.br',
				to=self.key.id(),
				subject='Voce tem ' + num_tarefas + ' tarefa(s) proxima(s) de expirar',
				body=message
				)

class Tarefa(ndb.Model):
	nome = ndb.StringProperty()
	descricao = ndb.StringProperty()
	prazo = ndb.StringProperty()
	expirando = ndb.BooleanProperty()

	def verify_deadline(self):
		current_time = datetime.datetime.now().date()
		if self.prazo:
			data = self.prazo.split('T')[0].split('-')
			deadline = datetime.datetime(int(data[0]), int(data[1]), int(data[2]))
			time_left = deadline.date() - current_time
			self.expirando = time_left <= datetime.timedelta(2) and time_left >= datetime.timedelta(0)
		else:
			self.expirando = False

		self.put()