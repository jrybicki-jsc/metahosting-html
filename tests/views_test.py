import unittest
from autho import drop_ownerships
import facade
from myapp import app
from facade import add_type, create_instance, remove_type, delete_instance
from user import add_user, get_all_users, drop_all_users


class ViewsTest(unittest.TestCase):
    def setUp(self):
        drop_all_users()
        drop_ownerships()
        facade.instances = {}
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.types = ['mysql', 'eXist', 'mongo']
        for i in self.types:
            add_type(i, {'desc': 'description'})

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
        self.instance_ids = []
        for i in range(0, 3):
            inst = create_instance(instance_type=self.types[0],
                                   uid='2')
            self.instance_ids.append(inst['id'])

        for i in range(0, 2):
            inst = create_instance(instance_type=self.types[1],
                                   uid='2')
            self.instance_ids.append(inst['id'])

        self.instance_owner = self.user_list['2'].copy()
        self.instance_owner['id'] = '2'
        self.app = app.test_client()

    def tearDown(self):
        for i in self.types:
            remove_type(i)
        # self.assertEquals(0, len(get_types()), 'TearDown failed')

        for ids in self.instance_ids:
            delete_instance(ids, self.instance_owner['id'])

        drop_all_users()
        drop_ownerships()
        facade.instances = {}

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
        rv = self.app.get('/types/')
        for t in self.types:
            self.assertTrue(t in rv.data)

    def test_get_instances(self):
        # not available until logged in
        rv = self.app.get('/instances/')
        self.assertEquals(rv.status_code, 302)

        self.login(self.user_list['1'])
        rv = self.app.get('/instances/')
        self.assertEquals(rv.status_code, 200)
        self.assertTrue('No instances' in rv.data)
        self.logout()
        rv = self.app.get('/instances/')
        self.assertEquals(rv.status_code, 302)

        self.login(self.instance_owner)
        rv = self.app.get('/instances/')
        self.assertEquals(rv.status_code, 200)
        for iid in self.instance_ids:
            self.assertTrue(iid in rv.data)
        self.logout()

    def test_single_instance(self):
        # not available until logged in (even if not existing)
        rv = self.app.get('/instances/311')
        self.assertEquals(rv.status_code, 302)

        rv = self.app.get('/instances/' + self.instance_ids[0])
        self.assertEquals(rv.status_code, 302)

        self.login(self.user_list['1'])

        # not existing
        rv = self.app.get('/instances/311')
        self.assertEquals(rv.status_code, 404)

        # existing but not his
        rv = self.app.get('/instances/' + self.instance_ids[0])
        self.assertEquals(rv.status_code, 404)
        self.logout()

        self.login(self.instance_owner)
        # able to access all its instances
        for i in self.instance_ids:
            rv = self.app.get('/instances/' + i)
            self.assertEquals(rv.status_code, 200)

        # not existing instance for logged in user
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
            self.assertFalse('Instances of this type' in rv.data)

        self.logout()

        self.login(self.instance_owner)
        # logged user should access all types
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
        self.assertTrue('Unable to create instance' in rv.data)

        # existing type:
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
