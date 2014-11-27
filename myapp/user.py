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

    def validate_password(self, password):
        return self.get('pass') == password


users = {'1': {'name': 'jj', 'pass': 'pass'},
         '2': {'name': 'admin', 'pass': 'admin'},
         '3': {'name': 'ivan', 'pass': 'ivan'}
}


def get_user_for_id(uid):
    if uid in users:
        return User(values=users[uid], user_id=uid)
    else:
        return None


def get_user_for_name(name):
    for user_id, user in users.iteritems():
        if user['name'] == name:
            return User(user_id, user)
    return None