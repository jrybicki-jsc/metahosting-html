_ownership = {}


def is_user_instance(instance_id, user_id):
    global _ownership
    if user_id not in _ownership:
        return False
    return instance_id in _ownership[user_id]


def get_user_instances(user_id):
    if user_id in _ownership:
        return _ownership[user_id].copy()
    return set()


def make_owner(user_id, instance_id):
    global _ownership
    if user_id not in _ownership:
        _ownership[user_id] = set()

    _ownership[user_id].add(instance_id)


def revoke_ownership(user_id, instance_id):
    global _ownership
    if user_id not in _ownership:
        return False
    if instance_id not in _ownership[user_id]:
        return False

    _ownership[user_id].remove(instance_id)
    return True
