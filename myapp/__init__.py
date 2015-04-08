from facade import get_facade
import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.login import LoginManager
from logging import StreamHandler, DEBUG
import sys


class ReverseProxied(object):
    """
    Follow instructions at http://flask.pocoo.org/snippets/35/
    to handle our reverse proxy.
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        server = environ.get('HTTP_X_FORWARDED_SERVER', '')
        if server:
            environ['HTTP_HOST'] = server
        return self.app(environ, start_response)


app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

app.secret_key = '03aa1'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'Europe/Berlin'
app.config.from_envvar('META-HTTP', silent=True)

# set up console logger:
handler = StreamHandler(stream=sys.stdout)
handler.setLevel(DEBUG)
app.logger.addHandler(handler)

Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

if 'HTTP_DEBUG' in os.environ:
    from facade.facade import Facade
    from helpers.LocalAutho import LocalAuthorizer
    from helpers.DictStore import Store

    instance_store = Store()
    type_store = Store()
    authorizer = LocalAuthorizer()

    from helpers import add_some_types, add_some_instances, add_some_ownership
    add_some_types(type_store=type_store)
    add_some_instances(instance_store=instance_store)
    add_some_ownership(authorizer=authorizer)

    def send_method(routing_key, subject, message):
        print 'Incoming message: %s %s %s' % (routing_key, subject, message)
        if routing_key == 'info':
            return
        if subject == 'delete_instance':
            instance_store.remove(message['id'])
        else:
            instance_store.update(message['id'], message)

    facade = Facade(authorization=authorizer,
                    type_store=type_store,
                    instance_store=instance_store,
                    send_method=send_method)

else:
    facade = get_facade()

import myapp.views
