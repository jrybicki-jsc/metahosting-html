import uuid


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


def create_instance(instance_type):
    instance = dict()
    instance['id'] = generate_id()
    instance['status'] = 'starting'
    instance['type'] = instance_type
    return instance


def get_instances_of_type(instance_type_name):
    return {iid: desc for iid, desc in get_all_instances().iteritems() if
            desc['type'] == instance_type_name}


def generate_id():
    return uuid.uuid1().hex


def get_instance(instance_id):
    instances = get_all_instances()
    if instance_id in instances:
        return instances[instance_id]
    return None


def get_all_instances():
    return {u'0df959386fee11e4a350f0def1d0c536':
                {
                    u'id': u'0df959386fee11e4a350f0def1d0c536',
                    u'last_info': 1416402900.545865,
                    u'status': u'running',
                    u'ts': 1416402900.542269,
                    u'type': u'mysql'},
            u'666':
                {
                    u'id': u'666',
                    u'last_info': 1416398801.156127,
                    u'status': u'running',
                    u'ts': 1416398801.153139,
                    u'type': u'neo4j'},
            u'828d548e6fe411e495bff0def1d0c536':
                {
                    u'id': u'828d548e6fe411e495bff0def1d0c536',
                    u'last_info': 1416398801.156127,
                    u'status': u'failed',
                    u'ts': 1416398801.153139,
                    u'type': u'mysql'}}


def get_instances_of_type(instance_type_name):
    return {iid: desc for iid, desc in get_all_instances().iteritems() if
            desc['type'] == instance_type_name}


def generate_id():
    return uuid.uuid1().hex
