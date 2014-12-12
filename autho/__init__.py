import os
from autho.local import LocalAuthorizer
from autho.remote import RemoteAuthorizer


def get_authorizer():
    if 'AUTHO_PORT_5000_TCP_PORT' in os.environ \
            and 'AUTHO_PORT_5000_TCP_ADDR' in os.environ:
        url = 'http://%s:%s' % (os.environ.get('AUTHO_PORT_5000_TCP_ADDR'),
                                os.environ.get('AUTHO_PORT_5000_TCP_PORT'))
        return RemoteAuthorizer(url=url, user='service2', password='simple')
    return LocalAuthorizer()
