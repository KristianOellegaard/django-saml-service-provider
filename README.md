# django-saml-service-provider
Easily let users sign in via SAML 2.0 to your django app. Based on python-saml and comes with a Onelogin.com provider, so you
need to do very little work to get started.

[![Build Status](https://travis-ci.org/KristianOellegaard/django-saml-service-provider.svg?branch=master)](https://travis-ci.org/KristianOellegaard/django-saml-service-provider)
[![codecov](https://codecov.io/gh/KristianOellegaard/django-saml-service-provider/branch/master/graph/badge.svg)](https://codecov.io/gh/KristianOellegaard/django-saml-service-provider)

# Get started
If you are using OneLogin as your identity provider, you can simply add the following to your `urls.py` file to add
all necessary authentication views:

```python
# urls.py
urlpatterns = [
    url(r'^saml/', include('saml_service_provider.urls')),
    ...
]
```

For these views to work, you will have to add a few new settings to your `settings.py` file:

```python
# settings.py
ONELOGIN_CONNECTOR_ID = 1234
ONELOGIN_X509_CERT = """-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----"""  # You may provide ONELOGIN_X509_FINGERPRINT instead
SP_METADATA_URL = 'http://localhost:8000/saml/metadata/'  # from saml_service_provider.urls
SP_LOGIN_URL = 'http://localhost:8000/saml/initiate-login/'  # from saml_service_provider.urls
SP_LOGOUT_URL = 'http://localhost:8000/logout/'
```

If you are using a different service provider, you will have to initialize `saml_service_provider.settings.SAMLServiceProviderSettings` directly, and you will need to create your own views, overriding the views in `saml_service_provider.views`.

# Django authentication backend
This project conveniently ships with an authentication backend - just add it to AUTHENTICATION_BACKENDS in settings and you're
good to go - e.g.:

```python
AUTHENTICATION_BACKENDS = (
    # 'django.contrib.auth.backends.ModelBackend',
    'saml_service_provider.auth_backend.SAMLServiceProviderBackend',
)
```
