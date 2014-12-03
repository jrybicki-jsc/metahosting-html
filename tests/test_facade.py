import unittest
from facade import get_types, add_type, remove_type, create_instance, get_instance


class FacadeTest(unittest.TestCase):
    def setUp(self):
        self.service_name1 = 'service1'
        self.service_name2 = 'service2'

        add_type(self.service_name1, {'value': 'some'})
        add_type(self.service_name2, {'value': 'oooa'})

        self.user_id = '90210'
        self.instance1 = create_instance(instance_type=self.service_name1, uid=self.user_id)
        self.instance2 = create_instance(instance_type=self.service_name1, uid=self.user_id)
        self.instance3 = create_instance(instance_type=self.service_name2, uid=self.user_id)

        self.assertIsNotNone(self.instance1, 'Initialization failed')
        self.assertIsNotNone(self.instance2, 'Initialization failed')
        self.assertIsNotNone(self.instance3, 'Initialization failed')


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

    def test_create_instance(self):
        # not possible to start an instance of unknown type
        result = create_instance(instance_type='someNonExisting', uid=self.user_id)
        self.assertIsNone(result)

        result = create_instance(instance_type=self.service_name1, uid=self.user_id)
        self.assertIsNotNone(result)
        # expect following fields:
        self.assertEqual(result['type'], self.service_name1)
        self.assertTrue('ts' in result)
        self.assertTrue('id' in result)
        self.assertTrue('status' in result)

        ts1 = result['ts']
        result = create_instance(instance_type=self.service_name1, uid=self.user_id)
        self.assertIsNotNone(result)
        self.assertTrue('ts' in result)
        #time runs, timestamp increases
        self.assertGreater(result['ts'], ts1)

    def test_get_instance(self):
        # non-existing instances
        self.assertIsNone(get_instance(instance_id='33322211', uid=self.user_id))
        self.assertIsNone(get_instance(instance_id='333222111', uid=self.user_id))

        # not authorized
        self.assertIsNone(get_instance(instance_id=self.instance1['id'], uid=43222))
        self.assertIsNone(get_instance(instance_id=self.instance1['id'], uid=0))

        result = get_instance(instance_id=self.instance1['id'], uid=self.user_id)
        self.assertIsNotNone(result)
        self.assertTrue('id' in result)
        self.assertEqual(result['id'], self.instance1['id'])
        self.assertTrue('ts' in result)
        self.assertTrue('status' in result)

    def test_get_instances_of_type(self):
        pass

    def test_get_all_instances(self):
        pass
















