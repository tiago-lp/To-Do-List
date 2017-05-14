import webapp2
import json
import datetime
import logging
from google.appengine.api import users
from google.appengine.api import memcache
from models import *
from utils import *

def _assert(condition, status_code, msg):
    if condition:
        return

    logging.info("assertion failed: %s" % msg)
    webapp2.abort(status_code, msg)

class BaseHandler(webapp2.RequestHandler):
    pass

class LoginHandler(BaseHandler):
    def get(self):
        uri = self.request.get('uri', '/')
        self.redirect(users.create_login_url(uri))

class LogoutHandler(BaseHandler):
    def get(self):
        self.redirect(users.create_logout_url('/'))

def login_required(method):
    def check_login(self, *args):
        user = users.get_current_user()
        if user is None:
            self.response.write('{"msg":"requires authentication", "login_url":"http://%s/login"}' % self.request.host)
            self.response.set_status(401)
            return

        method(self, user, *args)

    return check_login

class MainHandler(BaseHandler):
    @login_required
    def get(self, user):
        usuario = Usuario.get_or_insert(user.email(), id=user.email())
        tarefas = usuario.get_tarefas()
        usuario.put()
        user_data = {
            "email": user.email(),
            "usuario": usuario.to_dict(),
            "tarefas": tarefas,
            "logout_url": "http://%s/logout" % self.request.host
        }
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.write(data2json(user_data).encode('utf-8'))

class UsuarioHandler(BaseHandler):
    def put(self, email):
        usuario = Usuario.get_by_id(email)
        _assert(usuario, 400, "usuario not found")
        data = json.loads(self.request.body)
        usuario.update(data)
        usuario.put()

app = webapp2.WSGIApplication([
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/api', MainHandler),
    ('/api/usuario/(.*)', UsuarioHandler),
], debug=True)