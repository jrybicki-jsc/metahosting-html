import uuid
from time import time


class Facade(object):
    def __init__(self, authorization):
        self.authorization = authorization
        self._types = dict()
        self._instances = dict()

    def get_types(self):
        return self._types.copy()

    def add_type(self, name, description):
        self._types[name] = description

    def remove_type(self, name):
        if name not in self._types:
            return False
        self._types.pop(name)
        return True

    def create_instance(self, instance_type, uid):
        if instance_type not in self.get_types():
            # exception?
            return None

        instance = dict()
        instance['id'] = self._generate_id()
        instance['status'] = 'starting'
        instance['type'] = instance_type
        instance['ts'] = time()
        # return value ignored?
        self.authorization.make_owner(uid, instance['id'])
        self._instances[instance['id']] = instance
        return instance

    def delete_instance(self, instance_id, uid):
        if instance_id not in self._instances or not \
                self.authorization.is_user_instance(instance_id=instance_id,
                                                    user_id=uid):
            return False
        self._instances.pop(instance_id)
        return self.authorization.revoke_ownership(user_id=uid,
                                                   instance_id=instance_id)

    def get_instances_of_type(self, instance_type_name, uid):
        if instance_type_name not in self._types:
            return {}
        return {iid: desc
                for iid, desc in self.get_all_instances(uid).iteritems()
                if desc['type'] == instance_type_name}

    def get_instance(self, instance_id, uid):
        if instance_id not in self._instances or not \
                self.authorization.is_user_instance(instance_id, uid):
            return None

        return self._instances[instance_id]

    def get_all_instances(self, uid):
        user_instances = self.authorization.get_user_instances(uid)
        return {instanceId: self._instances[instanceId] for instanceId in
                user_instances}

    @staticmethod
    def _generate_id():
        return uuid.uuid1().hex
