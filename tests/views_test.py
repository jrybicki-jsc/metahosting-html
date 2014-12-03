import unittest
from myapp import app
from facade import add_type, create_instance, remove_type, get_types, \
    delete_instance, get_all_instances
from myapp.views import logout
from user import add_user


class ViewsTest(unittest.TestCase):
    def setUp(self):
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

        self.assertEquals(len(self.instance_ids), 5, 'Setup failed')
        self.instance_owner = self.user_list['2']
        self.instance_owner['id'] = '2'
        self.app = app.test_client()

    def tearDown(self):
        for i in self.types:
            remove_type(i)
        self.assertEquals(0, len(get_types()), 'TearDown failed')

        for ids in self.instance_ids:
            delete_instance(ids, self.instance_owner['id'])

        self.assertEquals(0, len(get_all_instances(self.instance_owner['id'])),
                          'TearDown failed')

    def test_login(self):
        for uid, user in self.user_list.iteritems():
            rv = self.login(user['name'], user['password'])
            self.assertEquals(rv.status_code, 200)
            self.assertTrue('Logged in successfully' in rv.data)
            rv = self.logout()
            self.assertEquals(rv.status_code, 200)
            self.assertTrue('Logged out' in rv.data)

        for uid, user in self.user_list.iteritems():
            rv = self.login(user['name'], 'wrong')
            self.assertTrue('Unable to validate password' in rv.data)

        rv = self.login(self.non_existing_user['name'],
                        self.non_existing_user['password'])
        self.assertTrue('Unable to validate password' in rv.data)

        rv = self.login(self.user_list['1']['name'], '')
        self.assertTrue('This field is required' in rv.data)
        rv = self.login('', 'password')
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

        self.login(self.user_list['1']['name'],
                   self.user_list['1']['password'])
        rv = self.app.get('/instances/')
        self.assertEquals(rv.status_code, 200)
        self.assertTrue('No instances' in rv.data)
        self.logout()
        rv = self.app.get('/instances/')
        self.assertEquals(rv.status_code, 302)

        self.login(self.instance_owner['name'],
                   self.instance_owner['password'])
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

        self.login(self.user_list['1']['name'],
                   self.user_list['1']['password'])

        # not existing
        rv = self.app.get('/instances/311')
        self.assertEquals(rv.status_code, 404)

        # existing but not his
        rv = self.app.get('/instances/' + self.instance_ids[0])
        self.assertEquals(rv.status_code, 404)
        self.logout()

        self.login(self.instance_owner['name'],
                   self.instance_owner['password'])
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

        self.login(self.user_list['1']['name'],
                   self.user_list['1']['password'])

        # logged user should access all types
        for t in self.types:
            rv = self.app.get('/types/' + t)
            self.assertEquals(rv.status_code, 200)
            # but must not view instances unless he has some
            self.assertFalse('Instances of this type' in rv.data)

        self.logout()

        self.login(self.instance_owner['name'],
                   self.instance_owner['password'])
        # logged user should access all types
        for t in self.types[:-1]:
            rv = self.app.get('/types/' + t)
            self.assertEquals(rv.status_code, 200)
            # type view includes instances
            self.assertTrue('Instances of this type' in rv.data)

        self.logout()

    def login(self, username, password):
        return self.app.post('/login',
                             data={'username': username, 'password': password},
                             follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
