from django.contrib.auth.models import User
from django.test import TestCase


class SamlServiceProviderTestCase(TestCase):

    HOST = 'sp.example.com'
    ROOT_URL = 'http://{host}'.format(host=HOST)
    METADATA_URL = '{root}/metadata/'.format(root=ROOT_URL)

    USER_USERNAME = 'msmith'
    USER_FIRST_NAME = 'Mary'
    USER_LAST_NAME = 'Smith'

    @classmethod
    def setUpTestData(cls):
        # Create user
        cls.user = User.objects.create_user(username=cls.USER_USERNAME)
