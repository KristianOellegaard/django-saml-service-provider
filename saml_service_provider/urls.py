from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from saml_service_provider.views import MetadataView, CompleteAuthenticationView, InitiateAuthenticationView

urlpatterns = patterns('',
    url(r'^initiate-login/$', InitiateAuthenticationView.as_view(), name="saml_login_initiate"),
    url(r'^complete-login/$', csrf_exempt(CompleteAuthenticationView.as_view()), name="saml_login_complete"),
    url(r'^metadata/$', MetadataView.as_view(), name="saml_metadata"),
)
