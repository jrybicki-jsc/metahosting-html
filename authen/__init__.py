from authen.user import User
import json
import os

USERS_FILE = 'myapp/data/users.json'


def load_from_file(file_name=USERS_FILE):
    if os.path.isfile(file_name):
        with open(file_name) as f:
            users = json.load(f)
    else:
        return None
    return users

_backend = dict()
a = load_from_file()
if a:
    print 'Loading users database from file %s (loaded: %s)' % (USERS_FILE,
                                                                len(a))
    _backend = a
else:
    print 'File %s not found' % USERS_FILE


def _get_user_for_feature(feature_name, feature_value):
    for user_id, user in _backend.iteritems():
        if feature_name in user and user[feature_name] == feature_value:
            return User(user_id, user)
    return None


def get_user_for_id(uid):
    if uid in _backend:
        return User(values=_backend[uid], user_id=uid)
    else:
        return None


def get_all_users():
    return [User(user_id, user) for user_id, user in _backend.iteritems()]


def drop_all_users():
    global _backend
    _backend = {}


def remove_user(uid):
    global _backend
    if uid in _backend:
        _backend.pop(uid)
        return True
    return False


def add_user(uid, name, password, api_key):
    global _backend
    if uid in _backend:
        return False

    tmp_dict = {'name': name, 'pass': password, 'api_key': api_key}
    _backend[uid] = tmp_dict.copy()
    return True


def get_user_for_name(name):
    return _get_user_for_feature('name', name)


def get_user_for_api_key(api_key):
    return _get_user_for_feature('api_key', api_key)
