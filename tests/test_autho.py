import unittest
from autho import make_owner, is_user_instance, revoke_ownership, get_user_instances
import autho


class AuthoTest(unittest.TestCase):
    def setUp(self):
        self.uid = 661
        self.instance_id1 = 13311
        make_owner(user_id=self.uid, instance_id=self.instance_id1)
        self.instance_id2 = 13312
        make_owner(user_id=self.uid, instance_id=self.instance_id2)

    def test_make_owner(self):
        make_owner(user_id=111, instance_id=222)
        self.assertTrue(is_user_instance(instance_id=222, user_id=111))
        self.assertFalse(is_user_instance(instance_id=223, user_id=111))
        self.assertFalse(is_user_instance(instance_id=222, user_id=112))
        revoke_ownership(user_id=111, instance_id=222)

    def test_get_user_instances(self):
        instances = get_user_instances(user_id=self.uid)
        self.assertEqual(len(instances), 2)
        self.assertTrue(self.instance_id1 in instances)
        self.assertTrue(self.instance_id2 in instances)
        self.assertFalse(12221 in instances)

        instances = get_user_instances(user_id=662)
        self.assertEqual(len(instances), 0)
        self.assertFalse(self.instance_id1 in instances)
        self.assertFalse(self.instance_id2 in instances)
        self.assertFalse(12221 in instances)

    def test_is_user_instance(self):
        self.assertTrue(is_user_instance(user_id=self.uid, instance_id=self.instance_id1))
        self.assertTrue(is_user_instance(user_id=self.uid, instance_id=self.instance_id2))

        self.assertFalse(is_user_instance(user_id=self.uid, instance_id=77711))
        self.assertFalse(is_user_instance(user_id=20011, instance_id=self.instance_id1))

    def test_multiple_ownership(self):
        uid = '111'
        instance_id = '5671'
        make_owner(user_id=uid, instance_id=instance_id)
        self.assertTrue(is_user_instance(instance_id, uid))
        self.assertEqual(len(get_user_instances(uid)), 1)
        revoke_ownership(user_id=uid, instance_id=instance_id)
        self.assertFalse(is_user_instance(instance_id, uid))
        self.assertEqual(len(get_user_instances(uid)), 0)

        make_owner(user_id=uid, instance_id=instance_id)
        make_owner(user_id=uid, instance_id=instance_id)
        make_owner(user_id=uid, instance_id=instance_id)
        self.assertEqual(len(get_user_instances(uid)), 1)
        revoke_ownership(user_id=uid, instance_id=instance_id)
        self.assertFalse(is_user_instance(instance_id, uid))
        self.assertFalse(instance_id in get_user_instances(uid))
        self.assertEqual(len(get_user_instances(uid)), 0)

    def test_revoke_ownership(self):
        self.assertTrue(is_user_instance(instance_id=self.instance_id1, user_id=self.uid))
        self.assertTrue(is_user_instance(instance_id=self.instance_id2, user_id=self.uid))

        result = revoke_ownership(user_id=self.uid, instance_id=122111)
        self.assertFalse(result)

        result = revoke_ownership(user_id=2221, instance_id=self.instance_id1)
        self.assertFalse(result)
        result = revoke_ownership(user_id=self.uid, instance_id=self.instance_id1)
        self.assertTrue(result)
        self.assertTrue(is_user_instance(user_id=self.uid, instance_id=self.instance_id2))
        self.assertFalse(is_user_instance(user_id=self.uid, instance_id=self.instance_id1))
        instances = get_user_instances(user_id=self.uid)
        self.assertFalse(self.instance_id1 in instances)
        self.assertTrue(self.instance_id2 in instances)

        make_owner(user_id=self.uid, instance_id=self.instance_id1)



