from django.http import HttpResponse, HttpResponseRedirect
from graphite.util import json
from requests_oauthlib import OAuth2Session
from django.conf import settings

# This information is obtained upon registration of a new GitHub OAuth
# application here: https://github.com/settings/applications/new
client_id = settings.OAUTH2_CLIENT_ID
client_secret = settings.OAUTH2_CLIENT_SECRET
authorization_base_url = settings.OAUTH2_AUTH_BASE_URL
token_url = settings.OAUTH2_TOKEN_URL
token_url = settings.OAUTH2_TOKEN_URL

def login(request):
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    print "Enter login"

    session = OAuth2Session(client_id, redirect_uri='http://test.local:8001/callback')
    authorization_url, state = session.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    request.session['oauth_state'] = state

    print "Exit login"

    return HttpResponseRedirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

def callback(request):
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """
    print "Enter callback"

    session = OAuth2Session(client_id, state=request.session['oauth_state'], redirect_uri='http://test.local:8001/callback')
    token = session.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.build_absolute_uri())

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    request.session['oauth_token'] = token

    print "Token obtained"
    print "Exit callback"

    get_protected_url(request, 'http://localhost:8000/api/current_user/')

    return HttpResponseRedirect("/")

def get_protected_url(request, url):
    print "Getting protected URL"

    session = OAuth2Session(client_id, token=request.session['oauth_token'])
    r = json.loads(session.get(url))

    return r

def logout(request):
    print "Logging out!"
    request.session.flush()
    return HttpResponse("Logged out!")
