import uuid
import autho
from time import time

instances = dict()
_types = dict()


def get_types():
    return _types.copy()


def add_type(name, description):
    global _types
    _types[name] = description


def remove_type(name):
    global _types
    if name not in _types:
        return False
    _types.pop(name)
    return True


def create_instance(instance_type, uid):
    if instance_type not in get_types():
        #exception?
        return None

    instance = dict()
    instance['id'] = _generate_id()
    instance['status'] = 'starting'
    instance['type'] = instance_type
    instance['ts'] = time()
    autho.make_owner(uid, instance['id'])
    global instances
    instances[instance['id']] = instance
    return instance


def get_instances_of_type(instance_type_name, uid):
    return {iid: desc for iid, desc in get_all_instances(uid).iteritems() if
            desc['type'] == instance_type_name}


def get_instance(instance_id, uid):
    instance_dict = get_all_instances(uid)
    if instance_id in instance_dict and autho.is_user_instance(instance_id, uid):
        return instance_dict[instance_id]
    return None


def get_all_instances(uid):
    global instances
    user_instances = autho.get_user_instances(uid)
    return {instance_id: instances[instance_id] for instance_id in user_instances}


def _generate_id():
    return uuid.uuid1().hex


