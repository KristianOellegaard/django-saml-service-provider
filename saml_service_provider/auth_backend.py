from django.contrib.auth.models import User


class SAMLServiceProviderBackend(object):

    NAMEID_ATTRIBUTE = 'username'
    ATTRIBUTE_NAME_FIRST_NAME = 'First name'
    ATTRIBUTE_NAME_LAST_NAME = 'Last name'

    @staticmethod
    def get_attribute_or_none(attributes, attribute_name):
        try:
            return attributes[attribute_name][0]
        except IndexError:
            return

    def post_init_user(self, user):
        pass

    def update_attributes(self, user, attributes):
        # Set name
        user.first_name = self.get_attribute_or_none(attributes, self.ATTRIBUTE_NAME_FIRST_NAME) or ''
        user.last_name = self.get_attribute_or_none(attributes, self.ATTRIBUTE_NAME_LAST_NAME) or ''
        user.save()

    def authenticate(self, saml_authentication=None):
        if not saml_authentication:  # Using another authentication method
            return

        if saml_authentication.is_authenticated():
            kwargs = {self.NAMEID_ATTRIBUTE: saml_authentication.get_nameid()}
            try:
                user = User.objects.get(**kwargs)
            except User.DoesNotExist:
                user = User(**kwargs)
                user.set_unusable_password()
                self.post_init_user(user)

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
