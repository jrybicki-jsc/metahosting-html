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


__backend__ = dict()
a = load_from_file()
if a:
    print 'Loading users database from file %s (loaded: %s)' % (USERS_FILE,
                                                                len(a))
    __backend__ = a
else:
    print 'File %s not found' % USERS_FILE


def _get_user_for_property(property_name, property_value):
    for user_id, user_data in __backend__.iteritems():
        if property_name in user_data \
                and user_data[property_name] == property_value:
            return User(user_id, user_data)
    return None


def get_user_for_id(uid):
    if uid in __backend__:
        return User(values=__backend__[uid], user_id=uid)
    else:
        return None


def get_all_users():
    return [User(user_id, user) for user_id, user in __backend__.iteritems()]


def drop_all_users():
    global __backend__
    __backend__ = {}


def remove_user(uid):
    global __backend__
    if uid in __backend__:
        __backend__.pop(uid)
        return True
    return False


def add_user(uid, name, password, api_key):
    global __backend__
    if uid in __backend__:
        return False

    tmp_dict = {'name': name, 'pass': password, 'api_key': api_key}
    __backend__[uid] = tmp_dict.copy()
    return True


def get_user_for_name(name):
    return _get_user_for_property('name', name)


def validate_password(user_entity, password):
    return user_entity.validate_password(password)


def get_user_for_api_key(api_key):
    return _get_user_for_property('api_key', api_key)


def get_user_for_eppn(api_key):
    tmp_dict = {'name': api_key, 'pass': None, 'api_key': api_key}
    return User(user_id=api_key, values=tmp_dict)
