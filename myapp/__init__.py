from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.login import LoginManager

app = Flask(__name__)
app.secret_key = '03aa1'
app.config.from_envvar('META-HTTP', silent=True)

Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

import myapp.views
