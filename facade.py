import uuid
from autho import instance_belong_to_user, get_user_instances, make_owner
from time import time

instances = {u'0df959386fee11e4a350f0def1d0c536': {
                    u'id': u'0df959386fee11e4a350f0def1d0c536',
                    u'last_info': 1416402900.545865,
                    u'status': u'running',
                    u'ts': 1416402900.542269,
                    u'type': u'mysql'},
             u'666': {
                    u'id': u'666',
                    u'last_info': 1416398801.156127,
                    u'status': u'running',
                    u'ts': 1416398801.153139,
                    u'type': u'neo4j'},
             u'828d548e6fe411e495bff0def1d0c536': {
                    u'id': u'828d548e6fe411e495bff0def1d0c536',
                    u'last_info': 1416398801.156127,
                    u'status': u'failed',
                    u'ts': 1416398801.153139,
                    u'type': u'mysql'}}


def get_types():
    return {
        u'mysql': {u'description': u'mysql: world leading relational database',
                   u'name': u'mysql',
                   u'ts': 1416402816.064837},
        u'neo4j': {u'description': u'native graph database',
                   u'name': u'neo4j',
                   u'ts': 1416487339.491318},
        u'eXist': {u'description': u'eXist is a XML database',
                   u'name': u'eXist',
                   u'ts': 1416487325.564435}
    }


def create_instance(instance_type, uid):
    instance = dict()
    instance['id'] = generate_id()
    instance['status'] = 'starting'
    instance['type'] = instance_type
    instance['ts'] = time()
    make_owner(uid, instance['id'])
    global instances
    instances[instance['id']] = instance
    return instance


def get_instances_of_type(instance_type_name, uid):
    return {iid: desc for iid, desc in get_all_instances(uid).iteritems() if
            desc['type'] == instance_type_name}


def get_instance(instance_id, uid):
    instance_dict = get_all_instances(uid)
    if instance_id in instance_dict and instance_belong_to_user(instance_id, uid):
        return instance_dict[instance_id]
    return None


def get_all_instances(uid):
    global instances
    user_instances = get_user_instances(uid)
    return {instance_id: instances[instance_id] for instance_id in user_instances}


def generate_id():
    return uuid.uuid1().hex


