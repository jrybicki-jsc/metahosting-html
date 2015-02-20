
class User(dict):
    def __init__(self, user_id, values):
        super(User, self).__init__()
        self.update({'user_id': user_id})
        self.update(values)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.get('user_id')

    def get_name(self):
        return self.get('name')

    def get_api_key(self):
        return self.get('api_key')

    def validate_password(self, password):
        return self.get('pass') == password
