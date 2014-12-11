from time import time
import unittest
from autho.local import LocalAuthorizer
from myapp import app, facade, type_store, instance_store, authorizer
from user import add_user, drop_all_users
from mock import Mock


class ViewsTest(unittest.TestCase):
    def setUp(self):
        self.tearDown()

        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.types = ['mysql', 'eXist', 'mongo']

        for i in self.types:
            facade.add_type(i, {'desc': 'description'})

        self.li = facade.get_types()

        self.user_list = dict()
        self.user_list['1'] = {'name': 'jj',
                               'password': 'bar',
                               'api_key': 'fo'}
        self.user_list['2'] = {'name': 'bruce',
                               'password': 'Spring',
                               'api_key': '10020100210212'}
        self.user_list['3'] = {'name': 'Eva',
                               'password': 'myS3cr3t!',
                               'api_key': 'afda001112'}

        drop_all_users()
        for uid, user in self.user_list.iteritems():
            add_user(uid, user['name'], user['password'], user['api_key'])

        self.non_existing_user = {'name': 'Odin',
                                  'password': 'Fooo',
                                  'api_key': 'foaaaa'}
        self.instances = []

        for i in range(0, 3):
            inst = facade.create_instance(instance_type=self.types[0],
                                          uid='2')
            self.instances.append(inst)

        for i in range(0, 2):
            inst = facade.create_instance(instance_type=self.types[1],
                                          uid='2')
            self.instances.append(inst)

        self.instance_owner = self.user_list['2'].copy()
        self.instance_owner['id'] = '2'

        self.app = app.test_client()

    def tearDown(self):
        drop_all_users()
        authorizer.drop_all()
        inst = instance_store.get_all()
        for instance_id, value in inst.iteritems():
            instance_store.remove(instance_id)

        inst = type_store.get_all()
        for type_name, value in inst.iteritems():
            type_store.remove(type_name)

    def test_login(self):
        for uid, user in self.user_list.iteritems():
            rv = self.login(user)
            self.assertEquals(rv.status_code, 200)
            self.assertTrue('Logged in successfully' in rv.data)
            rv = self.logout()
            self.assertEquals(rv.status_code, 200)
            self.assertTrue('Logged out' in rv.data)

        for uid, user in self.user_list.iteritems():
            rv = self.login({'name': user['name'], 'password': 'wrong'})
            self.assertTrue('Unable to validate password' in rv.data)

        rv = self.login(self.non_existing_user)
        self.assertTrue('Unable to validate password' in rv.data)

        rv = self.login({'name': self.instance_owner['name'], 'password': ''})
        self.assertTrue('This field is required' in rv.data)
        rv = self.login({'name': '', 'password': 'password'})
        self.assertTrue('This field is required' in rv.data)

    def test_get_types(self):
        # no login required
        facade.get_types = Mock(return_value=self.li)
        rv = self.app.get('/types/')
        for t in self.types:
            self.assertTrue(t in rv.data)

    def test_get_instances(self):
        # not available until logged in
        rv = self.app.get('/instances/')
        self.assertEquals(rv.status_code, 302)

        self.login(self.user_list['1'])

        ret = {instance['id']: instance for instance in self.instances}
        facade.get_all_instances = Mock(return_value={})
        rv = self.app.get('/instances/')
        self.assertEquals(rv.status_code, 200)
        self.assertTrue('No instances' in rv.data)
        self.logout()
        rv = self.app.get('/instances/')
        self.assertEquals(rv.status_code, 302)

        self.login(self.instance_owner)
        facade.get_all_instances = Mock(return_value=ret)
        rv = self.app.get('/instances/')
        self.assertEquals(rv.status_code, 200)
        for iid in self.instances:
            self.assertTrue(iid['id'] in rv.data)
        self.logout()

    def test_single_instance(self):
        # not available until logged in (even if not existing)
        rv = self.app.get('/instances/311')
        self.assertEquals(rv.status_code, 302)

        rv = self.app.get('/instances/' + self.instances[0]['id'])
        self.assertEquals(rv.status_code, 302)

        self.login(self.user_list['1'])

        # not existing
        rv = self.app.get('/instances/311')
        self.assertEquals(rv.status_code, 404)

        # existing but not his
        rv = self.app.get('/instances/' + self.instances[0]['id'])
        self.assertEquals(rv.status_code, 404)
        self.logout()

        self.login(self.instance_owner)
        # able to access all its instance

        for i in self.instances:
            facade.get_instance = Mock(return_value=i)
            rv = self.app.get('/instances/' + i['id'])
            self.assertEquals(rv.status_code, 200)
            facade.get_instance.assert_called_with(
                instance_id=i['id'],
                uid=self.instance_owner['id'])

        # not existing instance for logged in user
        facade.get_instance = Mock(return_value=None)
        rv = self.app.get('/instances/311')
        self.assertEquals(rv.status_code, 404)
        self.logout()

    def test_single_type(self):
        # not available until logged in (even if not existing)
        rv = self.app.get('/types/wordpress')
        self.assertEquals(rv.status_code, 302)

        for t in self.types:
            rv = self.app.get('/types/' + t)
            self.assertEquals(rv.status_code, 302)

        self.login(self.user_list['1'])

        # logged user should access all types

        for t in self.types:
            rv = self.app.get('/types/' + t)
            self.assertEquals(rv.status_code, 200)
            # but must not view instances unless he has some
            print '%r' % facade.get_instances_of_type(t, '1')
            self.assertFalse('Instances of this type' in rv.data)

        self.logout()

        self.login(self.instance_owner)
        # logged user should access all types
        ret = {instance['id']: instance for instance in self.instances}
        facade.get_instances_of_type = Mock(return_value=ret)
        for t in self.types[:-1]:
            rv = self.app.get('/types/' + t)
            self.assertEquals(rv.status_code, 200)
            # type view includes instances
            self.assertTrue('Instances of this type' in rv.data)

        # not existing, not available even for logged-in
        rv = self.app.get('/types/wordpress')
        self.assertEquals(rv.status_code, 404)

        self.logout()

    def test_help(self):
        rv = self.app.get('/help/')
        self.assertEquals(200, rv.status_code)

    def test_create_instance(self):
        # not available for not authenticated
        rv = self.app.post('/')
        self.assertEquals(302, rv.status_code)
        self.login(self.instance_owner)
        # bad request:
        rv = self.app.post('/')
        self.assertEquals(400, rv.status_code)

        # non-existing type should fail:
        rv = self.app.post('/',
                           data={'instance_type': 'mss'},
                           follow_redirects=True)

        self.assertTrue('Unable to create instance' in rv.data, rv.data)
        rv = self.app.post('/',
                           data={'instance_type': self.types[0]},
                           follow_redirects=True)
        self.assertTrue('created' in rv.data)
        self.logout()

    def test_index(self):
        rv = self.app.get('/')
        # expect log-in redirection
        self.assertEquals(302, rv.status_code)

        self.login(self.instance_owner)
        rv = self.app.get('/')
        # expect log-in redirection
        self.assertEquals(200, rv.status_code)
        res = self.logout()

    def login(self, user):
        return self.app.post('/login',
                             data={'username': user['name'],
                                   'password': user['password']},
                             follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
