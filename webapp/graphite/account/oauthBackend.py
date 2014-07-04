from django.contrib.auth.models import User

class OAuthBackend(object):

    def authenticate(self, userdict):
        username = userdict.get('id')
        email = userdict.get('email')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # The password is required, so we'll make a random one
            # to prevent the user from logging into graphite itself
            random_pass = User.objects.make_random_password(length=16)
            user = User.objects.create_user(username, email, random_pass)
            user.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

