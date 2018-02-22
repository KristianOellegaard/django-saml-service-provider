import base64
import hashlib
import unittest

from saml_service_provider.settings import OneloginServiceProviderSettings


class SAMLServiceProviderSettingsTestCase(unittest.TestCase):

    def testOneloginServiceProviderSettingsRequiresCertOrFingerprint(self):
        with self.assertRaises(Exception) as e:
            OneloginServiceProviderSettings()
        self.assertEquals(str(e.exception), "Please provider either onelogin_x509_cert or onelogin_x509_fingerprint")

    def testOneloginX509CertSetsIDPX509Cert(self):
        x509_cert = base64.b64encode('abc123')
        settings = OneloginServiceProviderSettings(onelogin_x509_cert=x509_cert).settings

        # Verify that the IDP X509 cert matches the one provided to OneloginServiceProviderSettings
        self.assertIn('idp', settings)
        self.assertIn('x509cert', settings['idp'])
        self.assertEquals(settings['idp']['x509cert'], x509_cert)

    def testOneloginX509FingerprintSetsIDPX509Fingerprint(self):
        x509_fingerprint = hashlib.sha1('abc123').hexdigest()
        settings = OneloginServiceProviderSettings(onelogin_x509_fingerprint=x509_fingerprint).settings

        # Verify that the IDP X509 fingerprint matches the one provided to OneloginServiceProviderSettings
        self.assertIn('idp', settings)
        self.assertIn('certFingerprint', settings['idp'])
        self.assertEquals(settings['idp']['certFingerprint'], x509_fingerprint)
