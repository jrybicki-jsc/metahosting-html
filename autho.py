# mapping: uid->instance_id (shall we use ints? or strings?
ownership = {
    '2': ['0df959386fee11e4a350f0def1d0c536', '666'],
    '3': ['828d548e6fe411e495bff0def1d0c536']
}


def instance_belong_to_user(instance_id, user_id):
    if user_id not in ownership:
        return False
    return instance_id in ownership[user_id]


def get_user_instances(user_id):
    if user_id in ownership:
        return ownership[user_id]
    return []


def make_owner(uid, instance_id):
    global ownership
    if uid not in ownership:
        ownership[uid] = []

    ownership[uid].append(instance_id)

