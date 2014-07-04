from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login

from requests_oauthlib import OAuth2Session

from graphite.util import json

# This information is obtained upon registration of a new GitHub OAuth
# application here: https://github.com/settings/applications/new
client_id = settings.OAUTH2_CLIENT_ID
client_secret = settings.OAUTH2_CLIENT_SECRET
redirect_uri = settings.OAUTH2_REDIRECT_URI
authorization_base_url = settings.OAUTH2_AUTH_BASE_URL
token_url = settings.OAUTH2_TOKEN_URL
account_url = settings.OAUTH2_ACCOUNT_URL

def authorize(request):
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """

    session = OAuth2Session(client_id, scope=['read', 'account_rest_cmdline'], redirect_uri=redirect_uri)
    authorization_url, state = session.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    request.session['oauth_state'] = state

    return HttpResponseRedirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

def callback(request):
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    session = OAuth2Session(client_id, state=request.session['oauth_state'], scope=['read', 'account_rest_cmdline'], redirect_uri=redirect_uri)

    token = session.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.build_absolute_uri(),
                               verify=False)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    request.session['oauth_token'] = token

    response = get_protected_url(token, account_url)

    user = authenticate(userdict=response)

    login(request, user)
    request.user = user

    return HttpResponseRedirect("/")

def get_protected_url(token, url):
    session = OAuth2Session(client_id, token=token, scope=['read', 'account_rest_cmdline'], redirect_uri=redirect_uri)
    content = session.get(url, verify=False).content
    r = json.loads(content)

    return r
