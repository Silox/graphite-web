from django.http import HttpResponseRedirect
from django.conf import settings

class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than the LOGIN_URL.
    """
    def process_request(self, request):
        path = request.path_info.rstrip('/')
        print "Path: " + path

        # No token yet and not logging out? Onto the login! Also: urgh for favicons
        if path != settings.LOGOUT_URL and path != "/favicon.ico" and ('oauth_token' not in request.session or
                'oauth_state' not in request.session):

            print "Logging in!"
            if path != settings.LOGIN_URL and path != settings.CALLBACK_URL:
                return HttpResponseRedirect(settings.LOGIN_URL)
