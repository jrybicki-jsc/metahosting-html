from facade import get_facade
import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.login import LoginManager
from logging import StreamHandler, DEBUG
import sys

app = Flask(__name__)
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

if 'HTTP_DEBUG' in os.environ:
    from facade.facade import Facade
    from helpers.LocalAutho import LocalAuthorizer
    from stores.dict_store import Store

    instance_store = Store()
    type_store = Store()
    authorizer = LocalAuthorizer()

    from helpers import add_some_types
    add_some_types(type_store=type_store)

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
                    send_method=send_method
                    )

else:
    facade = get_facade()

import myapp.views
