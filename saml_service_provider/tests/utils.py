import base64

import django
from django.contrib.auth.models import User
from django.test import TestCase, override_settings


HOST = 'sp.example.com'
ROOT_URL = 'http://{host}'.format(host=HOST)
METADATA_URL = '{root}/metadata/'.format(root=ROOT_URL)


@override_settings(
    ONELOGIN_X509_CERT=base64.b64encode(b'abc123').decode('utf-8'),
    SP_METADATA_URL=METADATA_URL,
    SP_LOGIN_URL='{root}/complete-login/'.format(root=ROOT_URL)
)
class SamlServiceProviderTestCase(TestCase):

    HOST = HOST
    ROOT_URL = ROOT_URL
    METADATA_URL = METADATA_URL

    USER_USERNAME = 'msmith'
    USER_FIRST_NAME = 'Mary'
    USER_LAST_NAME = 'Smith'

    @staticmethod
    def user_is_authenticated(user):
        if django.VERSION < (1, 10,):
            return user.is_authenticated()
        return user.is_authenticated

    @classmethod
    def setUpTestData(cls):
        # Create user
        cls.user = User.objects.create_user(username=cls.USER_USERNAME)
