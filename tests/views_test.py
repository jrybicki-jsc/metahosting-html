import unittest
from myapp import app
from facade import add_type
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

        self.app = app.test_client()

    def test_first(self):
        result = self.app.get('/')

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

    def test_


    def login(self, username, password):
        return self.app.post('/login',
                             data={'username': username, 'password': password},
                             follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)