from flask.ext.wtf import Form
from authen import get_user_for_name, validate_password
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = get_user_for_name(self.username.data)
        if user is None:
            self.username.errors.append('Unknown user')
            return False

        if not validate_password(user, self.password.data):
            self.password.errors.append('Unable to validate password')
            return False

        self.user = user
        return True
