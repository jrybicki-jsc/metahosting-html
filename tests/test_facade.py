import unittest
from facade import get_types, add_type, remove_type, create_instance, \
    get_instance, get_all_instances, delete_instance, get_instances_of_type


class FacadeTest(unittest.TestCase):
    def setUp(self):
        self.service_name1 = 'service1'
        self.service_name2 = 'service2'

        add_type(self.service_name1, {'value': 'some'})
        add_type(self.service_name2, {'value': 'oooa'})
        self.assertEquals(2, len(get_types()))
        self.non_existing_type = 'non-existing'
        self.assertTrue(self.non_existing_type not in get_types())

        self.user_id = '90210'
        self.instance1 = create_instance(instance_type=self.service_name1,
                                         uid=self.user_id)
        self.instance2 = create_instance(instance_type=self.service_name1,
                                         uid=self.user_id)
        self.instance3 = create_instance(instance_type=self.service_name2,
                                         uid=self.user_id)
        self.assertEquals(3, len(get_all_instances(uid=self.user_id)))

        self.assertIsNotNone(self.instance1, 'Initialization failed')
        self.assertIsNotNone(self.instance2, 'Initialization failed')
        self.assertIsNotNone(self.instance3, 'Initialization failed')

        self.unauthorized_user1 = '42'
        self.unauthorized_user2 = 'aa19991111'

    def tearDown(self):
        remove_type(self.service_name1)
        remove_type(self.service_name2)
        self.assertEquals(0, len(get_types()))

        delete_instance(self.instance1['id'], self.user_id)
        delete_instance(self.instance2['id'], self.user_id)
        delete_instance(self.instance3['id'], self.user_id)
        self.assertEquals(0, len(get_all_instances(self.user_id)))

    def test_get_types(self):
        types = get_types()
        self.assertIsNotNone(types)
        self.assertTrue(self.service_name1 in types)
        self.assertTrue(self.service_name2 in types)
        self.assertEqual(len(types), 2)

    def test_add_type(self):
        new_type = 'new_service'
        new_type_desc = {'ooo'}
        self.assertFalse(new_type in get_types())

        add_type(new_type, new_type_desc)
        types = get_types()
        self.assertTrue(new_type in types)

        add_type(new_type, new_type_desc)
        add_type(new_type, new_type_desc)
        add_type(new_type, new_type_desc)
        self.assertTrue(new_type in get_types())

        add_type(new_type, {'other desc'})
        self.assertTrue(new_type in get_types())
        result = remove_type(new_type)
        self.assertTrue(result)
        self.assertFalse(new_type in get_types())
        result = remove_type(new_type)
        self.assertFalse(result)
        self.assertFalse(new_type in get_types())

        self.assertTrue(self.service_name1 in get_types())
        self.assertTrue(self.service_name2 in get_types())

    def test_remove_type(self):
        result = remove_type(self.non_existing_type)
        self.assertFalse(result)
        result = remove_type(self.non_existing_type)
        self.assertFalse(result)

        self.assertTrue(self.service_name1 in get_types())
        result = remove_type(self.service_name1)
        self.assertTrue(result)
        self.assertFalse(self.service_name1 in get_types())
        add_type(self.service_name1, {'value': 'some'})
        self.assertTrue(self.service_name1 in get_types())

    def test_create_instance(self):
        # not possible to start an instance of unknown type
        result = create_instance(instance_type=self.non_existing_type,
                                 uid=self.user_id)
        self.assertIsNone(result)

        count = len(get_all_instances(uid=self.user_id))
        result = create_instance(instance_type=self.service_name1,
                                 uid=self.user_id)
        self.assertIsNotNone(result)
        self.assertEquals(count+1, len(get_all_instances(uid=self.user_id)))
        # expect following fields:
        self.assertEqual(result['type'], self.service_name1)
        self.assertTrue('ts' in result)
        self.assertTrue('id' in result)
        self.assertTrue('status' in result)
        delete_instance(instance_id=result['id'], uid=self.user_id)
        self.assertEquals(count, len(get_all_instances(uid=self.user_id)))

        ts1 = result['ts']
        result = create_instance(instance_type=self.service_name1,
                                 uid=self.user_id)
        self.assertEquals(count+1, len(get_all_instances(uid=self.user_id)))
        self.assertIsNotNone(result)
        self.assertTrue('ts' in result)
        #time runs, timestamp increases
        self.assertGreater(result['ts'], ts1)
        delete_instance(instance_id=result['id'], uid=self.user_id)
        self.assertEquals(count, len(get_all_instances(uid=self.user_id)))

    def test_get_instance(self):
        # non-existing instances
        self.assertIsNone(get_instance(instance_id='33322211',
                                       uid=self.user_id))
        self.assertIsNone(get_instance(instance_id='333222111',
                                       uid=self.user_id))

        # not authorized
        self.assertIsNone(get_instance(instance_id=self.instance1['id'],
                                       uid=self.unauthorized_user1))
        self.assertIsNone(get_instance(instance_id=self.instance1['id'],
                                       uid=self.unauthorized_user2))

        result = get_instance(instance_id=self.instance1['id'],
                              uid=self.user_id)
        self.assertIsNotNone(result)
        self.assertTrue('id' in result)
        self.assertEqual(result['id'], self.instance1['id'])
        self.assertTrue('ts' in result)
        self.assertTrue('status' in result)

    def test_get_all_instances(self):
        instances = get_all_instances(uid=self.unauthorized_user1)
        self.assertIsNotNone(instances)
        self.assertEquals(0, len(instances))

        instances = get_all_instances(uid=self.user_id)
        self.assertIsNotNone(instances)
        self.assertEqual(len(instances), 3)
        self.assertTrue(self.instance1['id'] in instances)
        self.assertTrue(self.instance2['id'] in instances)
        self.assertTrue(self.instance3['id'] in instances)

    def test_get_instances_of_type(self):
        # non-existing type
        result = get_instances_of_type(self.non_existing_type, self.user_id)
        self.assertIsNotNone(result)
        self.assertEquals(0, len(result))
        # not-authorized
        instances = get_instances_of_type(self.service_name1,
                                          self.unauthorized_user1)
        self.assertIsNotNone(result)
        self.assertEquals(0, len(result))

        instances = get_instances_of_type(self.service_name1,
                                          self.user_id)
        self.assertIsNotNone(instances)

        self.assertEquals(2, len(instances))
        self.assertTrue(self.instance1['id'] in instances)
        self.assertTrue(self.instance2['id'] in instances)

        instances = get_instances_of_type(self.service_name2,
                                          self.user_id)
        self.assertIsNotNone(instances)
        self.assertEquals(1, len(instances))
        self.assertTrue(self.instance3['id'] in instances)
