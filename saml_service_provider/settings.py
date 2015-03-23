
class SAMLServiceProviderSettings(object):
    contact_info = {
        # Contact information template, it is recommended to suply a
        # technical and support contacts.
        "technical": {
            "givenName": "technical_name",
            "emailAddress": "technical@example.com"
        },
        "support": {
            "givenName": "support_name",
            "emailAddress": "support@example.com"
        }
    }

    organization_info = {
        # Organization information template, the info in en_US lang is
        # recommended, add more if required.
        "en-US": {
            "name": "organization",
            "displayname": "Organization Name",
            "url": "https://www.example.org/"
        }
    }

    def __init__(self,
                 debug=False,
                 strict=True,
                 sp_metadata_url=None, sp_login_url=None, sp_logout_url=None, sp_x509cert=None, sp_private_key=None,  # Service provider settings (e.g. us)
                 idp_metadata_url=None, idp_sso_url=None, idp_slo_url=None, idp_x509cert=None, idp_x509_fingerprint=None,  # Identify provider settings (e.g. onelogin)

    ):
        super(SAMLServiceProviderSettings, self).__init__()
        self.settings = default_settings = {
            # If strict is True, then the Python Toolkit will reject unsigned
            # or unencrypted messages if it expects them to be signed or encrypted.
            # Also it will reject the messages if the SAML standard is not strictly
            # followed. Destination, NameId, Conditions ... are validated too.
            "strict": strict,

            # Enable debug mode (outputs errors).
            "debug": debug,

            # Service Provider Data that we are deploying.
            "sp": {
                # Identifier of the SP entity  (must be a URI)
                "entityId": sp_metadata_url,
                # Specifies info about where and how the <AuthnResponse> message MUST be
                # returned to the requester, in this case our SP.
                "assertionConsumerService": {
                    # URL Location where the <Response> from the IdP will be returned
                    "url": sp_login_url,
                    # SAML protocol binding to be used when returning the <Response>
                    # message. OneLogin Toolkit supports this endpoint for the
                    # HTTP-POST binding only.
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
                },
                # Specifies info about where and how the <Logout Response> message MUST be
                # returned to the requester, in this case our SP.
                "singleLogoutService": {
                    # URL Location where the <Response> from the IdP will be returned
                    "url": sp_logout_url,
                    # SAML protocol binding to be used when returning the <Response>
                    # message. OneLogin Toolkit supports the HTTP-Redirect binding
                    # only for this endpoint.
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
                },
                # Specifies the constraints on the name identifier to be used to
                # represent the requested subject.
                # Take a look on src/onelogin/saml2/constants.py to see the NameIdFormat that are supported.
                "NameIDFormat": "urn:oasis:names:tc:SAML:2.0:nameid-format:unspecified",
                # Usually x509cert and privateKey of the SP are provided by files placed at
                # the certs folder. But we can also provide them with the following parameters
                'x509cert': sp_x509cert,
                'privateKey': sp_private_key
            },

            # Identity Provider Data that we want connected with our SP.
            "idp": {
                # Identifier of the IdP entity  (must be a URI)
                "entityId": idp_metadata_url,
                # SSO endpoint info of the IdP. (Authentication Request protocol)
                "singleSignOnService": {
                    # URL Target of the IdP where the Authentication Request Message
                    # will be sent.
                    "url": idp_sso_url,
                    # SAML protocol binding to be used when returning the <Response>
                    # message. OneLogin Toolkit supports the HTTP-Redirect binding
                    # only for this endpoint.
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
                },
                # SLO endpoint info of the IdP.
                "singleLogoutService": {
                    # URL Location of the IdP where SLO Request will be sent.
                    "url": idp_slo_url,
                    # SAML protocol binding to be used when returning the <Response>
                    # message. OneLogin Toolkit supports the HTTP-Redirect binding
                    # only for this endpoint.
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
                },
                # Public x509 certificate of the IdP
                "x509cert": idp_x509cert,
                #   Instead of use the whole x509cert you can use a fingerprint
                #   (openssl x509 -noout -fingerprint -in "idp.crt" to generate it)
                "certFingerprint": idp_x509_fingerprint

            },
            # Security settings
            # "security": {
            #
            #     # /** signatures and encryptions offered **/
            #
            #     # Indicates that the nameID of the <samlp:logoutRequest> sent by this SP
            #     # will be encrypted.
            #     "nameIdEncrypted": False,
            #
            #     # Indicates whether the <samlp:AuthnRequest> messages sent by this SP
            #     # will be signed.  [Metadata of the SP will offer this info]
            #     "authnRequestsSigned": False,
            #
            #     # Indicates whether the <samlp:logoutRequest> messages sent by this SP
            #     # will be signed.
            #     "logoutRequestSigned": False,
            #
            #     # Indicates whether the <samlp:logoutResponse> messages sent by this SP
            #     # will be signed.
            #     "logoutResponseSigned": False,
            #
            #     # /* Sign the Metadata
            #     #  false || true (use sp certs) || {
            #     #                                     "keyFileName": "metadata.key",
            #     #                                     "certFileName": "metadata.crt"
            #     #                                  }
            #     # */
            #     "signMetadata": False,
            #
            #     # /** signatures and encryptions required **/
            #
            #     # Indicates a requirement for the <samlp:Response>, <samlp:LogoutRequest>
            #     # and <samlp:LogoutResponse> elements received by this SP to be signed.
            #     "wantMessagesSigned": False,
            #
            #     # Indicates a requirement for the <saml:Assertion> elements received by
            #     # this SP to be signed. [Metadata of the SP will offer this info]
            #     "wantAssertionsSigned": False,
            #
            #     # Indicates a requirement for the NameID received by
            #     # this SP to be encrypted.
            #     "wantNameIdEncrypted": False,
            #
            #     # Authentication context.
            #     # Set to false and no AuthContext will be sent in the AuthNRequest,
            #     # Set true or don't present thi parameter and you will get an AuthContext 'exact' 'urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport'
            #     # Set an array with the possible auth context values: array ('urn:oasis:names:tc:SAML:2.0:ac:classes:Password', 'urn:oasis:names:tc:SAML:2.0:ac:classes:X509'),
            #     'requestedAuthnContext': True,
            # },
            "organization": self.organization_info,
            'contactPerson': self.contact_info,
        }
        if not idp_x509cert:
            del self.settings['idp']['x509cert']
        if not idp_x509_fingerprint:
            del self.settings['idp']['certFingerprint']


class OneloginServiceProviderSettings(SAMLServiceProviderSettings):
    def __init__(self, onelogin_connector_id=None, onelogin_x509_cert=None, onelogin_x509_fingerprint=None, **kwargs):
        kwargs['idp_metadata_url'] = 'https://app.onelogin.com/saml/metadata/%s' % onelogin_connector_id
        kwargs['idp_sso_url'] = 'https://app.onelogin.com/trust/saml2/http-post/sso/%s/' % onelogin_connector_id
        kwargs['idp_slo_url'] = 'https://app.onelogin.com/trust/saml2/http-redirect/slo/%s/' % onelogin_connector_id
        if onelogin_x509_cert:
            kwargs['idp_x509cert'] = onelogin_x509_cert
        elif onelogin_x509_fingerprint:
            kwargs['idp_x509_fingerprint'] = onelogin_x509_fingerprint
        else:
            raise Exception("Please provider either onelogin_x509_cert or onelogin_x509_fingerprint")
        super(OneloginServiceProviderSettings, self).__init__(**kwargs)