from django.http import HttpResponseRedirect
from django.conf import settings

class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than the LOGIN_URL.
    """
    def process_request(self, request):
        if not request.user.is_authenticated():
            if path != settings.LOGIN_URL and path != settings.CALLBACK_URL:
                print "Logging in!"
                return HttpResponseRedirect(settings.LOGIN_URL)
