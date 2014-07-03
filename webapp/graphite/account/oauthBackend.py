from django.contrib.auth.models import User

class OAuthBackend(object):

    def authenticate(self, userdict):
        username = userdict.get('id')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username)
            user.save()

        print user
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

