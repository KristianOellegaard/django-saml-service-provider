import base64
import os

from django.contrib.auth import get_user
import mock

from saml_service_provider.settings import OneloginServiceProviderSettings
from saml_service_provider.tests.utils import SamlServiceProviderTestCase


class InitiateAuthenticationViewTestCase(SamlServiceProviderTestCase):

    def assertStartsWith(self, full_string, expected_substring):
        return self.assertEquals(full_string[:len(expected_substring)], expected_substring)

    @mock.patch('saml_service_provider.views.OneloginMixin.get_onelogin_settings')
    def testInitiateAuthenticationRedirectsToIDP(self, mock_get_onelogin_settings):
        mock_get_onelogin_settings.return_value = OneloginServiceProviderSettings(
            onelogin_x509_cert=base64.b64encode('abc123'),
            sp_metadata_url=self.METADATA_URL,
            sp_login_url='{root}/complete-login/'.format(root=self.ROOT_URL),
            sp_x509cert="",
            sp_private_key=""
        ).settings

        # Verify that the user is not yet authenticated
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated())

        # Verify that unauthenticated requests to initate login redirect the user to complete login
        response = self.client.get('/initiate-login/', follow=True, HTTP_HOST=self.HOST)
        redirect_url, redirect_status_code = response.redirect_chain[0]
        self.assertEquals(redirect_status_code, 302)
        self.assertStartsWith(redirect_url, 'https://app.onelogin.com/trust/saml2/http-post/sso/')


class CompleteAuthenticationViewTestCase(SamlServiceProviderTestCase):

    @classmethod
    def generate_saml_response(cls, username, first_name, last_name):
        # Read in SAML response from testdata
        cwd = os.path.dirname(os.path.abspath(__file__))
        saml_response_xml_filename = os.path.join(cwd, 'testdata', 'saml-response.xml')
        with open(saml_response_xml_filename, 'r') as f:
            saml_response_xml = f.read().format(
                metadata_url=cls.METADATA_URL,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
        return base64.b64encode(saml_response_xml)

    @classmethod
    def generate_basic_saml_response(cls):
        return cls.generate_saml_response(
            username=cls.USER_USERNAME,
            first_name=cls.USER_FIRST_NAME,
            last_name=cls.USER_LAST_NAME
        )

    @mock.patch('onelogin.saml2.response.OneLogin_Saml2_Response.is_valid')
    @mock.patch('saml_service_provider.views.OneloginMixin.get_onelogin_settings')
    def testUserRedirectsToRelayState(self, mock_get_onelogin_settings, mock_is_valid):
        mock_get_onelogin_settings.return_value = OneloginServiceProviderSettings(
            onelogin_x509_cert=base64.b64encode('abc123'),
            sp_metadata_url=self.METADATA_URL,
            sp_login_url='{root}/complete-login/'.format(root=self.ROOT_URL),
            sp_x509cert="",
            sp_private_key=""
        ).settings
        mock_is_valid.return_value = True

        # Verify that the user is not yet authenticated
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated())

        # Simulate a POST request from OneLogin to log a user in
        relay_url = '/relay/'
        data = {
            'SAMLResponse': self.generate_basic_saml_response(),
            'RelayState': relay_url,
        }
        response = self.client.post(
            '/complete-login/',
            data=data,
            follow=True,
            HTTP_HOST=self.HOST
        )

        # Verify that the user is now authenticated
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated())

        # Verify that the user is the one in the SAML response
        self.assertEquals(user.username, self.USER_USERNAME)

        # Verify that the user redirects to the relay
        redirect_url, redirect_status_code = response.redirect_chain[0]
        self.assertEquals(redirect_status_code, 302)
        self.assertEquals(redirect_url.replace(self.ROOT_URL, ''), relay_url)

    @mock.patch('onelogin.saml2.response.OneLogin_Saml2_Response.is_valid')
    @mock.patch('saml_service_provider.views.OneloginMixin.get_onelogin_settings')
    def testUserRedirectsToRootWithoutRelayState(self, mock_get_onelogin_settings, mock_is_valid):
        mock_get_onelogin_settings.return_value = OneloginServiceProviderSettings(
            onelogin_x509_cert=base64.b64encode('abc123'),
            sp_metadata_url=self.METADATA_URL,
            sp_login_url='{root}/complete-login/'.format(root=self.ROOT_URL),
            sp_x509cert="",
            sp_private_key=""
        ).settings
        mock_is_valid.return_value = True

        # Simulate a POST request from OneLogin to log a user in
        response = self.client.post(
            '/complete-login/',
            data={'SAMLResponse': self.generate_basic_saml_response()},
            follow=True,
            HTTP_HOST=self.HOST
        )

        # Verify that the user is now authenticated
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated())

        # Verify that the user redirects to the root
        redirect_url, redirect_status_code = response.redirect_chain[0]
        self.assertEquals(redirect_status_code, 302)
        self.assertEquals(redirect_url.replace(self.ROOT_URL, ''), '/')

    @mock.patch('saml_service_provider.views.OneloginMixin.get_onelogin_settings')
    def testBadSamlResponse(self, mock_get_onelogin_settings):
        mock_get_onelogin_settings.return_value = OneloginServiceProviderSettings(
            onelogin_x509_cert=base64.b64encode('abc123'),
            sp_metadata_url=self.METADATA_URL,
            sp_login_url='{root}/complete-login/'.format(root=self.ROOT_URL),
            sp_x509cert="",
            sp_private_key=""
        ).settings

        # Simulate a POST request with an invalid SAMLResponse
        # This response is invalid naturally, since we're not
        # mocking the OneLogin_Saml2_Response.is_valid() method
        response = self.client.post(
            '/complete-login/',
            data={'SAMLResponse': self.generate_basic_saml_response()},
            HTTP_HOST=self.HOST
        )

        # Verify that the user is returned a 400
        self.assertEquals(response.status_code, 400)


class MetadataViewTestCase(SamlServiceProviderTestCase):

    @mock.patch('saml_service_provider.views.OneloginMixin.get_onelogin_settings')
    def testMetadataView(self, mock_get_onelogin_settings):
        mock_get_onelogin_settings.return_value = OneloginServiceProviderSettings(
            onelogin_x509_cert=base64.b64encode('abc123'),
            sp_metadata_url=self.METADATA_URL,
            sp_login_url='{root}/complete-login/'.format(root=self.ROOT_URL),
            sp_x509cert="",
            sp_private_key=""
        ).settings

        # Verify that the metadata requests render successfully
        response = self.client.get('/metadata/', HTTP_HOST=self.HOST)
        self.assertEquals(response.status_code, 200)
        self.assertIn('Content-Type', response)
        self.assertEquals(response['Content-Type'], 'text/xml')
