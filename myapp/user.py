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


users = {'1': {'name': 'jj', 'pass': 'pass', 'api_key': '661'},
         '2': {'name': 'admin', 'pass': 'admin', 'api_key': '88121'},
         '3': {'name': 'ivan', 'pass': 'ivan', 'api_key': '771'}
        }


def get_user_for_id(uid):
    if uid in users:
        return User(values=users[uid], user_id=uid)
    else:
        return None


def get_user_for_name(name):
    return get_user_for_feature('name', name)


def get_user_for_api_key(api_key):
    return get_user_for_feature('api_key', api_key)


def get_user_for_feature(feature_name, feature_value):
    for user_id, user in users.iteritems():
        if feature_name in user and user[feature_name] == feature_value:
            return User(user_id, user)
    return None