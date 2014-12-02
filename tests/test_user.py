import unittest
from user import User, get_user_for_id, drop_all_users, add_user, get_all_users, remove_user, get_user_for_name, \
    get_user_for_api_key


class UserTest(unittest.TestCase):
    def setUp(self):
        drop_all_users()
        my_list = {'1': {'name': 'jj', 'pass': 'pass', 'api_key': '661'},
                   '2': {'name': 'admin', 'pass': 'admin', 'api_key': '88121'},
                   '3': {'name': 'ivan', 'pass': 'ivan', 'api_key': '771'}}
        for k, v in my_list.iteritems():
            add_user(uid=k, name=v['name'], password=v['pass'], api_key=v['api_key'])

    def test_first(self):
        print 'Testing first'
        self.assertTrue(True)

    def test_get_all_users(self):
        ll = get_all_users()
        self.assertEqual(len(ll), 3, 'Not enough users')

    def test_get_user_for_id(self):
        # function expects opaque string
        result = get_user_for_id(0001)
        self.assertIsNone(result, 'Non-existing user is not none')

        # not-existing user gives None
        result = get_user_for_id('111')
        self.assertIsNone(result, 'Non-existing string-based user is not none')

        # existing user:
        result = get_user_for_id('2')
        # '2': {'name': 'admin', 'pass': 'admin', 'api_key': '88121'},
        self.assertIsNotNone(result)
        self.assertIsInstance(result, User)
        self.assertEqual(result.get('name'), 'admin')
        self.assertTrue(result.validate_password('admin'), 'Wrong password')
        self.assertEqual(result.get('api_key'), '88121')

    def test_add_user(self):
        count = len(get_all_users())
        self.assertIsNone(get_user_for_id(111))
        self.assertIsNone(get_user_for_name('Bob'))
        self.assertIsNone(get_user_for_api_key('006612'))

        result = add_user(111, name='Bob', password='Dylan', api_key='006612')
        self.assertTrue(result)
        self.assertEqual(len(get_all_users()), count+1)

        r2 = get_user_for_id(111)
        self.assertIsNotNone(r2)
        self.assertEqual(r2.get('name'), 'Bob')
        self.assertEqual(r2.get('api_key'), '006612')
        self.assertTrue(r2.validate_password('Dylan'))

        r2 = get_user_for_name('Bob')
        self.assertIsNotNone(r2)
        self.assertEqual(r2.get('name'), 'Bob')
        self.assertEqual(r2.get('api_key'), '006612')
        self.assertTrue(r2.validate_password('Dylan'))

        r2 = get_user_for_api_key('006612')
        self.assertIsNotNone(r2)
        self.assertEqual(r2.get('name'), 'Bob')
        self.assertEqual(r2.get('api_key'), '006612')
        self.assertTrue(r2.validate_password('Dylan'))

        r3 = remove_user(111)
        self.assertTrue(r3)
        self.assertEqual(len(get_all_users()), count)

    def test_remove_user(self):
        count = len(get_all_users())
        result = add_user(111, name='Bob', password='Dylan', api_key='006612')
        self.assertTrue(result)
        self.assertEqual(len(get_all_users()), count+1)

        result = remove_user(222)
        self.assertFalse(result)

        result = remove_user(111)
        self.assertTrue(result)
        self.assertEqual(len(get_all_users()), count)
        r2 = get_user_for_id(111)
        self.assertIsNone(r2)
        r2 = get_user_for_name('Bob')
        self.assertIsNone(r2)
        r2 = get_user_for_api_key('006612')
        self.assertIsNone(r2)










