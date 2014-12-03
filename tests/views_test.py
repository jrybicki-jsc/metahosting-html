import unittest
from myapp import app
from helpers import set_up_test_app


class ViewsTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        set_up_test_app()
        self.app = app.test_client()

    def test_first(self):
        result = self.app.get('/')

    def test_login(self):
        rv = self.login('admin', 'admin')
        self.assertEquals(rv.status_code, 200)
        self.assertTrue('Logged in successfully' in rv.data)
        rv = self.logout()
        self.assertEquals(rv.status_code, 200)
        self.assertTrue('Logged out' in rv.data)

        rv = self.login('admin', 'wrong')
        self.assertTrue('Unable to validate password' in rv.data)

        rv = self.login('admin', '')
        self.assertTrue('This field is required' in rv.data)
        rv = self.login('', 'password')
        self.assertTrue('This field is required' in rv.data)

    

    def login(self, username, password):
        return self.app.post('/login',
                             data={'username': username, 'password': password},
                             follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)