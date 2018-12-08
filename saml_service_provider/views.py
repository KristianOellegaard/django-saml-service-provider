from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseServerError
from django.views.generic import View
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils

from saml_service_provider.settings import OneloginServiceProviderSettings
from saml_service_provider.utils import prepare_from_django_request


class OneloginMixin(object):

    def get_onelogin_settings(self):
        return OneloginServiceProviderSettings(
            onelogin_connector_id=getattr(settings, 'ONELOGIN_CONNECTOR_ID', None),
            onelogin_x509_cert=getattr(settings, 'ONELOGIN_X509_CERT', None),
            onelogin_x509_fingerprint=getattr(settings, 'ONELOGIN_X509_FINGERPRINT', None),
            sp_metadata_url=getattr(settings, 'SP_METADATA_URL', None),
            sp_login_url=getattr(settings, 'SP_LOGIN_URL', None),
            sp_logout_url=getattr(settings, 'SP_LOGOUT_URL', None),
            debug=getattr(settings, 'SP_DEBUG', settings.DEBUG),
            strict=getattr(settings, 'SP_STRICT', True),
            sp_x509cert=getattr(settings, 'SP_X509_CERT', ""),
            sp_private_key=getattr(settings, 'SP_PRIVATE_KEY', "")
        ).settings


class InitiateAuthenticationView(OneloginMixin, View):

    def get(self, *args, **kwargs):
        req = prepare_from_django_request(self.request)
        auth = OneLogin_Saml2_Auth(req, self.get_onelogin_settings())

        return_url = self.request.GET.get('next', settings.LOGIN_REDIRECT_URL)

        return HttpResponseRedirect(auth.login(return_to=return_url))  # Method that builds and sends the AuthNRequest


class CompleteAuthenticationView(OneloginMixin, View):

    def post(self, request):
        req = prepare_from_django_request(request)
        auth = OneLogin_Saml2_Auth(req, self.get_onelogin_settings())
        auth.process_response()
        errors = auth.get_errors()
        if not errors:
            if auth.is_authenticated():
                user = authenticate(request=req, saml_authentication=auth)
                login(self.request, user)
                if (
                    'RelayState' in req['post_data']
                    and OneLogin_Saml2_Utils.get_self_url(req) != req['post_data']['RelayState']
                ):
                    return HttpResponseRedirect(auth.redirect_to(req['post_data']['RelayState']))
                else:
                    return HttpResponseRedirect("/")
            else:
                raise PermissionDenied()
        else:
            if settings.DEBUG:
                print(auth.get_last_error_reason())
            return HttpResponseBadRequest(
                "Error when processing SAML Response: {errors}".format(errors=', '.join(errors))
            )


class MetadataView(OneloginMixin, View):

    def get(self, request, *args, **kwargs):
        req = prepare_from_django_request(request)
        auth = OneLogin_Saml2_Auth(req, self.get_onelogin_settings())
        saml_settings = auth.get_settings()
        metadata = saml_settings.get_sp_metadata()
        errors = saml_settings.validate_metadata(metadata)
        if len(errors) == 0:
            return HttpResponse(content=metadata, content_type='text/xml')
        else:
            return HttpResponseServerError(content=', '.join(errors))
