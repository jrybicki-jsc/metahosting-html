__author__ = 'jj'


def add_some_ownership(authorizer):
    my_ownership = {
        '1': ['0df959386fee11e4a350f0def1d0c536', '666'],
        '2': ['828d548e6fe411e495bff0def1d0c536']
    }
    for uid, instance_list in my_ownership.iteritems():
        for instance_id in instance_list:
            authorizer.make_owner(user_id=uid, instance_id=instance_id)


def add_some_types(type_store):
    my_list = {
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
    for name, desc in my_list.iteritems():
        type_store.update(name, desc)


def add_some_instances(instance_store):
    my_list = {
        u'0df959386fee11e4a350f0def1d0c536': {
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

    for k, v in my_list.iteritems():
        instance_store.update(k, v)
