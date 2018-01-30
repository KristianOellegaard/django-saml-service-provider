from django.contrib.auth.models import User
import mock

from saml_service_provider.auth_backend import SAMLServiceProviderBackend
from saml_service_provider.tests.utils import SamlServiceProviderTestCase


class SAMLServiceProviderBackendTestCase(SamlServiceProviderTestCase):

    NEW_USER_USERNAME = 'jdoe'
    NEW_USER_FIRST_NAME = 'John'
    NEW_USER_LAST_NAME = 'Doe'

    @classmethod
    def setUpTestData(cls):
        super(SAMLServiceProviderBackendTestCase, cls).setUpTestData()
        cls.auth_backend = SAMLServiceProviderBackend()

    def testNoAuthenticationMeansDifferentBackend(self):
        self.assertIsNone(self.auth_backend.authenticate())

    def testNoUserIsReturnedIfNoneIsAuthenticated(self):
        saml_authentication = mock.Mock(is_authenticated=lambda: False)
        self.assertIsNone(self.auth_backend.authenticate(saml_authentication))

    def testExistingUserIsAuthenticated(self):
        # Authenticate with the SAMLServiceProvider backend
        saml_authentication = mock.Mock(is_authenticated=lambda: True, get_nameid=lambda: self.USER_USERNAME)
        user = self.auth_backend.authenticate(saml_authentication)

        # Verify that the user authenticated is the existing user
        self.assertEquals(user, User.objects.get(username=self.USER_USERNAME))

    def testNewUserIsCreatedAndAuthenticated(self):
        # Count the number of users
        num_users = User.objects.count()

        # Authenticate with the SAMLServiceProvider backend
        saml_authentication = mock.Mock(
            is_authenticated=lambda: True,
            get_attributes=lambda: {'First name': [self.NEW_USER_FIRST_NAME], 'Last name': [self.NEW_USER_LAST_NAME]},
            get_nameid=lambda: self.NEW_USER_USERNAME
        )
        user = self.auth_backend.authenticate(saml_authentication)

        # Verify that the user authenticated is the new user
        self.assertEquals(user, User.objects.get(username=self.NEW_USER_USERNAME))

        # Verify that the user has the first and last name attributes set
        self.assertEquals(user.first_name, self.NEW_USER_FIRST_NAME)
        self.assertEquals(user.last_name, self.NEW_USER_LAST_NAME)

        # Verify that a new user was created
        self.assertEquals(User.objects.count(), num_users + 1)

    def testGetUserUsesAuthUser(self):
        # Verify that the user is looked up by PK
        self.assertEquals(self.auth_backend.get_user(self.user.pk), self.user)

        # Verify that no user is returned when an invalid PK is provided
        invalid_pk = User.objects.order_by('pk').last().pk + 1
        self.assertIsNone(self.auth_backend.get_user(invalid_pk))
