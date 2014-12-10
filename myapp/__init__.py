from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.login import LoginManager
from facade import Facade
from autho.autho import RemoteAuthorizer

app = Flask(__name__)
app.secret_key = '03aa1'
app.config.from_envvar('META-HTTP', silent=True)

Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

authorizer = RemoteAuthorizer('http://localhost:6000', 'service2', 'simple')
facade = Facade(authorization=authorizer)

import myapp.views
