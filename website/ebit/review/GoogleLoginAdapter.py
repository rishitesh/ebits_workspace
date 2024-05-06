from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


class GoogleLoginAdapter(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "https://eqbits.in/login"
    client_class = OAuth2Client
