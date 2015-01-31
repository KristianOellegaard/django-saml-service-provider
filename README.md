# django-saml-service-provider
Easily let users sign in via SAML 2.0 to your django app. Based on python-saml and comes with a Onelogin.com provider, so you
need to do very little work to get started.

# Get started
You need to extend the three default views provided by this library and use your own settings. It can be done easily with
a single mixin. Consider the following simple example, using the Onelogin provider. You can also do the same with the
regular SAMLServiceProvider - you just need to provide all the urls manually.

```python
class SettingsMixin(object):
    def get_onelogin_settings(self):
        return OneloginServiceProviderSettings(
            onelogin_connector_id=1234,
            onelogin_x509_cert="""-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----""",

            sp_metadata_url="http://localhost:8000%s" % reverse("saml_metadata"),
            sp_login_url="http://localhost:8000%s" % reverse("saml_login_complete"),
            sp_logout_url="http://localhost:8000%s" % reverse("logout"),

            debug=settings.DEBUG,
            strict=not settings.DEBUG,

            sp_x509cert="""-----BEGIN CERTIFICATE-----
        -----END CERTIFICATE-----""",
            sp_private_key="""-----BEGIN RSA PRIVATE KEY-----
        -----END RSA PRIVATE KEY-----"""
            ).settings
            
class LoginView(SettingsMixin, InitiateAuthenticationView):
    pass
    
class Authenticateview(SettingsMixin, CompleteAuthenticationView):
    pass
    
class XMLMetadataView(SettingsMixin, MetadataView):
    pass
```

# Django authentication backend
This project conveniently ships with an authentication backend - just add it to AUTHENTICATION_BACKENDS in settings and you're
good to go - e.g.:

```python
AUTHENTICATION_BACKENDS = (
    # 'django.contrib.auth.backends.ModelBackend',
    'saml_service_provider.auth_backend.SAMLServiceProviderBackend',
)
```
