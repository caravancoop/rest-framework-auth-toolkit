from rest_framework.authentication import TokenAuthentication

from .utils import get_object_from_setting


Token = get_object_from_setting("api_token_class")


class TokenAuthentication(TokenAuthentication):
    """DRF authentication backend for API requests.

    Parses headers like "Authorization: Bearer user-api-token".

    Override authenticate_credentials in a subclass if you need
    special behaviour to get a Token object from a string value.
    Default behaviour is to fetch a token via "key" field and
    check that token.user.is_active is true.
    """

    keyword = "Bearer"
    model = Token
