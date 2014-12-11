import os
from autho.local import LocalAuthorizer
from autho.remote import RemoteAuthorizer


def get_authorizer():
    if 'AUTHO_PORT_5000_TCP_PORT' in os.environ \
            and 'AUTHO_PORT_5000_TCP_ADDR' in os.environ:
        url = 'http://%s:%s' % (os.environ.get('AUTHO_PORT_5000_TCP_PORT'),
                                os.environ.get('AUTHO_PORT_5000_TCP_ADDR'))
        return RemoteAuthorizer(url=url, user='', password='')
    return LocalAuthorizer()
