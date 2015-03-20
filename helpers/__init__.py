
def add_some_ownership(authorizer):
    my_ownership = {
        '1': ['0df959386fee11e4a350f0def1d0c536',
              '666',
              '9b4ad79cb83411e4adbfd63e388e3f27',
              '828d548e6fe411e495bff0def1d0c536'],
        '2': ['828d548e6fe411e495bff0def1d0c536']
    }
    for uid, instance_list in my_ownership.iteritems():
        for instance_id in instance_list:
            authorizer.make_owner(user_id=uid, instance_id=instance_id)


def add_some_types(type_store):
    my_list = {
        u'mysql': {u'description': u'mysql: world leading relational database',
                   u'name': u'mysql',
                   u'ts': 1416402816.064837,
                   u'available': True},
        u'virtual1': {u'available': True,
                      u'description': u'virtual worker for testing purposes',
                      u'name': u'virtual1',
                      u'ts': 1424338658.027424, },
        u'neo4j': {u'description': u'native graph database',
                   u'name': u'neo4j',
                   u'ts': 1416487339.491318,
                   u'available': True},
        u'eXist': {u'description': u'eXist is a XML database',
                   u'name': u'eXist',
                   u'ts': 1416487325.564435,
                   u'environment': {u'EXIST_MEMORY': u'1024',
                                    u'EXIST_ADMIN_PASSWORD': u''},
                   u'available': True},
        u'NoNeXist': {u'name': u'eXist',
                      u'ts': 1416487325.564435}

    }
    for name, desc in my_list.iteritems():
        type_store.update(name, desc)


def add_some_instances(instance_store):
    my_list = {
        u'0df959386fee11e4a350f0def1d0c536': {
            u'connection': {
                u'3306/tcp': [{u'HostIp': u'0.0.0.0', u'HostPort': u'49151'}]
            },
            u'environment': [u'MYSQL_ROOT_PASSWORD=KvmWaEq4sdMSUGio'],
            u'id': u'0df959386fee11e4a350f0def1d0c536',
            u'last_info': 1416402900.545865,
            u'status': u'running',
            u'ts': 1416402900.542269,
            u'type': u'mysql'},
        u'666': {
            u'connection': {
                u'7473/tcp': [{u'HostIp': u'0.0.0.0', u'HostPort': u'49153'}],
                u'7474/tcp': [{u'HostIp': u'0.0.0.0', u'HostPort': u'49154'}]
            },
            u'urls': [u'http://0.0.0.0:49154/', 'https://0.0.0.0:49153/'],
            u'id': u'666',
            u'last_info': 1416398801.156127,
            u'status': u'running',
            u'ts': 1416398801.153139,
            u'type': u'neo4j'},
        u'828d548e6fe411e495bff0def1d0c536': {
            u'connection': {
                u'3306/tcp': [{u'HostIp': u'0.0.0.0', u'HostPort': u'49156'}]
            },
            u'environment': [u'MYSQL_ROOT_PASSWORD=KvmWaEq4sdMSUGio'],
            u'id': u'828d548e6fe411e495bff0def1d0c536',
            u'last_info': 1416398801.156127,
            u'status': u'failed',
            u'ts': 1416398801.153139,
            u'type': u'mysql'},
        u'9b4ad79cb83411e4adbfd63e388e3f27': {
            u'connection': {
                u'8080/tcp': [{u'HostIp': u'0.0.0.0', u'HostPort': u'49155'}]
            },
            u'environment': [
                u'EXIST_MEMORY=1024',
                u'EXIST_ADMIN_PASSWORD=KvmWaEq4sdMSUGio'],
            u'urls': [u'http://0.0.0.0:49155/exist/'],
            u'created': 1424349681.114382,
            u'id': u'9b4ad79cb83411e4adbfd63e388e3f27',
            u'last_info': 1424349870.699567,
            u'status': u'starting',
            u'ts': 1424349870.696452,
            u'type': u'exist'},
    }

    for k, v in my_list.iteritems():
        instance_store.update(k, v)
