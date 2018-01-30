from django.contrib.auth.models import User


class SAMLServiceProviderBackend(object):

    @staticmethod
    def get_attribute_or_none(attributes, attribute_name):
        try:
            return attributes[attribute_name][0]
        except IndexError:
            return

    def update_attributes(self, user, attributes):
        # Set name
        user.first_name = self.get_attribute_or_none(attributes, 'First name') or ''
        user.last_name = self.get_attribute_or_none(attributes, 'Last name') or ''
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
