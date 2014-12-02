#!/usr/bin/env python
from facade import add_type, instances
from myapp import app
from user import add_user
from autho import make_owner


def add_some_users():
    my_list = {'1': {'name': 'jj', 'pass': 'pass', 'api_key': '661'},
               '2': {'name': 'admin', 'pass': 'admin', 'api_key': '88121'},
               '3': {'name': 'ivan', 'pass': 'ivan', 'api_key': '771'}}
    for uid, v in my_list.iteritems():
        add_user(uid=uid, name=v['name'], password=v['pass'], api_key=v['api_key'])


def add_some_ownership():
    my_ownership = {'2': ['0df959386fee11e4a350f0def1d0c536', '666'],
                    '3': ['828d548e6fe411e495bff0def1d0c536']
    }
    for uid, instance_list in my_ownership.iteritems():
        for instance_id in instance_list:
            make_owner(user_id=uid, instance_id=instance_id)


def add_some_types():
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
        add_type(name=name, description=desc)


def add_some_instances():
    my_list = {u'0df959386fee11e4a350f0def1d0c536': {
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
        instances[k] = v


add_some_users()
add_some_ownership()
add_some_types()
add_some_instances()

app.run(debug=True)
