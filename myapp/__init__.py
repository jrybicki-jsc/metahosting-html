from facade import get_facade
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

facade = get_facade()

import myapp.views
