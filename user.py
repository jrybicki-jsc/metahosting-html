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

users = {}


def get_user_for_id(uid):
    if uid in users:
        return User(values=users[uid], user_id=uid)
    else:
        return None


def get_all_users():
    return [User(user_id, user) for user_id, user in users.iteritems()]


def drop_all_users():
    global users
    users = {}


def remove_user(uid):
    global users
    if uid in users:
        users.pop(uid)
        return True
    return False


def add_user(uid, name, password, api_key):
    global users
    if uid in users:
        return False

    tmp_dict = {'name': name, 'pass': password, 'api_key': api_key}
    users[uid] = tmp_dict.copy()
    return True


def get_user_for_name(name):
    return _get_user_for_feature('name', name)


def get_user_for_api_key(api_key):
    return _get_user_for_feature('api_key', api_key)


def _get_user_for_feature(feature_name, feature_value):
    for user_id, user in users.iteritems():
        if feature_name in user and user[feature_name] == feature_value:
            return User(user_id, user)
    return None
