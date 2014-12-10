__author__ = 'jj'
from local import LocalAuthorizer
from remote import RemoteAuthorizer


def get_authorizer():
    # RemoteAuthorizer('http://localhost:6000', 'service2', 'simple')
    return LocalAuthorizer()
