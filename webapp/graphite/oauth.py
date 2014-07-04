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
scope = settings.OAUTH2_SCOPE

def authorize(request):
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """

    # Create a new session
    session = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    # Get the authorization url and state
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

    # Create a new session with the state token obtained in Step 1
    session = OAuth2Session(client_id, state=request.session['oauth_state'], scope=scope, redirect_uri=redirect_uri)

    # Get the token
    token = session.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.build_absolute_uri(),
                               verify=False)

    # Save the token in the session
    request.session['oauth_token'] = token

    # Get the user id
    response = get_protected_url(token, account_url)

    # Create a new user if needed and log him in
    user = authenticate(userdict=response)
    login(request, user)
    request.user = user

    # Redirect the logged in user to the index
    return HttpResponseRedirect("/")

def get_protected_url(token, url):
    """ Returns a hash of the returned content from the protected url """

    # Create a session
    session = OAuth2Session(client_id, token=token, scope=scope, redirect_uri=redirect_uri)

    # Get the content
    content = session.get(url, verify=False).content

    # Return it
    return json.loads(content)
