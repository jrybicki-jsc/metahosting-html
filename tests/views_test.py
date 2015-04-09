import unittest
from myapp import app, myapp
from authen import add_user, drop_all_users
from facade.facade import Facade, generate_id
from time import time
from mock import Mock


class ViewsTest(unittest.TestCase):
    def setUp(self):

        self.tearDown()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

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

        for uid, user in self.user_list.iteritems():
            add_user(uid, user['name'], user['password'], user['api_key'])

        self.non_existing_user = {'name': 'Odin',
                                  'password': 'Fooo',
                                  'api_key': 'foaaaa'}
        self.instance_owner = self.user_list['2'].copy()
        self.instance_owner['id'] = '2'

        self.type_names = ['mysql', 'eXist', 'mongo']
        self.types = {}
        for name in self.type_names:
            instance_type = dict()
            instance_type['name'] = name
            instance_type['description'] = \
                'service_a for doing less cool stuff'
            self.types[name] = instance_type

        self.instances = dict()
        for i in range(1, 3):
            inst = self.prepare_instance('starting', self.type_names[0])
            self.instances[inst['id']] = inst.copy()

        self.facade = Mock()
        myapp.views.facade = self.facade
        self.facade.get_all_instances = Mock(return_value={})
        self.facade.get_types = Mock(return_value=self.types)
        self.facade.get_active_types = Mock(return_value=self.types)
        # .get_all_instances
        self.app = app.test_client()

    def prepare_instance(self, status, instance_type):
        instance = dict()
        instance['id'] = generate_id()
        instance['status'] = status
        instance['type'] = instance_type
        instance['ts'] = time()
        return instance

    def tearDown(self):
        drop_all_users()

    def test_login(self):
        for uid, user in self.user_list.iteritems():
            rv = self.login(user)
            self.assertEquals(rv.status_code, 200)
            self.assertTrue('Logged in successfully' in rv.data)
            rv = self.logout()
            self.assertEquals(rv.status_code, 200)
            self.assertTrue('Please log in to access this page' in rv.data)

        for uid, user in self.user_list.iteritems():
            rv = self.login({'name': user['name'], 'password': 'wrong'})
            self.assertTrue('Unable to validate password' in rv.data)

        rv = self.login(self.non_existing_user)
        self.assertTrue('Unknown user' in rv.data)

        rv = self.login({'name': self.instance_owner['name'], 'password': ''})
        self.assertTrue('This field is required' in rv.data)
        rv = self.login({'name': '', 'password': 'password'})
        self.assertTrue('This field is required' in rv.data)

    def test_get_types(self):
        # no login required

        rv = self.app.get('/types/')
        for t in self.types:
            self.assertTrue(t in rv.data)

    def test_get_instances(self):
        # not available until logged in
        rv = self.app.get('/instances/')
        self.assertEquals(rv.status_code, 302)

        self.login(self.user_list['1'])

        self.facade.get_all_instances = Mock(return_value={})
        rv = self.app.get('/instances/')
        self.assertEquals(rv.status_code, 200)
        self.assertTrue('No instances' in rv.data)
        # assert:called_with
        self.logout()
        rv = self.app.get('/instances/')
        self.assertEquals(rv.status_code, 302)

        self.login(self.instance_owner)
        self.facade.get_all_instances = Mock(return_value=self.instances)
        rv = self.app.get('/instances/')
        self.assertEquals(rv.status_code, 200)
        for iid, desc in self.instances.iteritems():
            print 'Checking %s-->%s' % (iid, desc)
            self.assertTrue(iid in rv.data)
        self.logout()

    def test_single_instance(self):
        # all that autho-stuff is a little bit mumbo-jumbo from old version
        # not available until logged in (even if not existing)
        rv = self.app.get('/instances/311')
        self.assertEquals(rv.status_code, 302)

        for iid, desc in self.instances.iteritems():
            rv = self.app.get('/instances/' + iid)
            self.assertEquals(rv.status_code, 302)

        self.login(self.user_list['1'])

        # not existing
        self.facade.get_instance = Mock(return_value=None)
        rv = self.app.get('/instances/311')
        self.assertEquals(rv.status_code, 404)

        # existing but not his
        self.facade.get_instance = Mock(return_value=None)
        rv = self.app.get('/instances/' + self.instances.keys()[0])
        self.assertEquals(rv.status_code, 404)
        self.logout()

        self.login(self.instance_owner)
        # able to access all its instance

        for iid, desc in self.instances.iteritems():
            self.facade.get_instance = Mock(return_value=desc)
            rv = self.app.get('/instances/' + iid)
            self.assertEquals(rv.status_code, 200)

        # not existing instance for logged in user
        self.facade.get_instance = Mock(return_value=None)
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
        self.facade.get_instances_of_type = Mock(return_value=[])
        for t in self.types:
            rv = self.app.get('/types/' + t)
            self.assertEquals(rv.status_code, 200)
            # but must not view instances unless he has some
            self.assertFalse('Instances of this type' in rv.data)

        self.logout()

        self.login(self.instance_owner)
        # logged user should access all types
        self.facade.get_instances_of_type = Mock(return_value=self.instances)

        for t in self.types:
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
        self.facade.create_instance = Mock(return_value=None)
        rv = self.app.post('/',
                           data={'instance_type': 'mss'},
                           follow_redirects=True)

        self.assertTrue('Unable to create instance' in rv.data, rv.data)
        instance = self.instances.get(self.instances.keys()[0])
        self.facade.create_instance = Mock(return_value=instance)
        rv = self.app.post('/',
                           data={'instance_type': self.type_names[0]},
                           follow_redirects=True)
        self.assertTrue('created' in rv.data)
        self.logout()

    def test_delete_instance(self):
        rv = self.app.post('/instances/11/delete')
        self.assertEquals(302, rv.status_code)

        self.login(self.instance_owner)
        self.facade.delete_instance = Mock(return_value=False)
        rv = self.app.post('/instances/11/delete')
        self.assertEqual(404, rv.status_code)
        self.facade.delete_instance.\
            assert_called_with('11', uid=self.instance_owner['id'])

        self.facade.delete_instance = Mock(return_value=True)
        rv = self.app.post('/instances/11/delete', follow_redirects=True)
        self.assertEqual(200, rv.status_code)
        self.facade.delete_instance.\
            assert_called_with('11', uid=self.instance_owner['id'])
        self.assertTrue('Instance 11 removed' in rv.data)
        self.logout()

    def test_profile(self):
        rv = self.app.get('/profile')
        self.assertEqual(302, rv.status_code)

        self.login(self.instance_owner)
        rv = self.app.get('/profile')
        self.assertEqual(200, rv.status_code)
        self.assertTrue(self.instance_owner['name'] in rv.data)
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

    def test_health(self):
        rv = self.app.get('/healthcheck/')
        self.assertEqual(rv.status_code, 200)

    def login(self, user):
        return self.app.post('/login',
                             data={'username': user['name'],
                                   'password': user['password']},
                             follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
