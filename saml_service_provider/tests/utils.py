import base64

from django.contrib.auth.models import User
from django.test import TestCase, override_settings


HOST = 'sp.example.com'
ROOT_URL = 'http://{host}'.format(host=HOST)
METADATA_URL = '{root}/metadata/'.format(root=ROOT_URL)


@override_settings(
    ONELOGIN_X509_CERT=base64.b64encode('abc123'),
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

    @classmethod
    def setUpTestData(cls):
        # Create user
        cls.user = User.objects.create_user(username=cls.USER_USERNAME)
