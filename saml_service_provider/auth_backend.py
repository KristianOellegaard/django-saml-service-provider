from django.contrib.auth.models import User


class SAMLServiceProviderBackend(object):

    def update_attributes(self, user, attributes):
        # Set name
        user.first_name = attributes['First name'][0]
        user.last_name = attributes['Last name'][0]
        user.save()

    def authenticate(self, saml_authentication=None):
        if not saml_authentication:  # Using another authentication method
            return

        if saml_authentication.is_authenticated():
            try:
                user = User.objects.get(username=saml_authentication.get_nameid())
            except User.DoesNotExist:
                user = User(username=saml_authentication.get_nameid())
                user.set_unusable_password()

            # Set attributes (and create user, if not yet created)
            attributes = saml_authentication.get_attributes()
            self.update_attributes(user, attributes)

            return user
        return

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return
