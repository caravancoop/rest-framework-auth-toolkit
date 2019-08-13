from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _

from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import FacebookLoginDeserializer, LoginDeserializer, SignupDeserializer
from .utils import get_object_from_setting, get_setting, MissingSetting

try:
    import facepy
except ImportError:
    facepy = None


User = get_user_model()
Token = get_object_from_setting('api_token_class')


class SignupView(generics.GenericAPIView):
    """Email address sign-up endpoint.

    If the setting email_confirmation_send_email is true (default),
    the function send_email will be called.  That function requires
    that your app define a route named app-auth:email-confirmation
    with an id parameter; the view for this route should get an
    email confirmation instance using the ID and call the confirm
    method.  To use a field that's not named 'id', define the setting
    email_confirmation_lookup_param (this will change the URL pattern).
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = get_object_from_setting('signup_serializer_class',
                                               SignupDeserializer)
    email_confirmation_class = get_object_from_setting('email_confirmation_class',
                                                       None)

    def post(self, request):
        """Create a user and send a confirmation email.

        Response

        `201 Created`
        """
        deserializer = self.get_serializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        user = deserializer.save()

        if self.email_confirmation_class is None:
            raise MissingSetting('email_confirmation_class')

        confirmation = self.email_confirmation_class.objects.create(user=user)
        if get_setting('email_confirmation_send_email', True):
            email_field = user.get_email_field_name()
            send_email(request, user, getattr(user, email_field), confirmation)

        return Response(status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """Email address log-in endpoint.

    To customize the request, define settings api_token_class and
    login_serializer_class.  The data validated by the serializer is
    passed to token_class.objects.create_token; for example, if you
    have a subclass of LoginDeserializer that adds an optional field
    "ip_address", you need a BaseAPITokenManager subclass that defines
    create_token(self, user, ip_address=None).
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = get_object_from_setting('login_serializer_class',
                                               LoginDeserializer)

    def post(self, request):
        """Authenticate a user, return an API auth token if valid.

        Response

        ```json
        {"token": "string"}
        ```
        """
        deserializer = self.get_serializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        data = deserializer.validated_data

        token = Token.objects.create_token(**data)
        return Response({'token': token.key})


class FacebookLoginView(generics.GenericAPIView):
    """Create a user from a Facebook signed request (from JS auth response).

    The user will be active immediately, with an unusable password.

    Response

    ```json
    {"token": "string"}
    ```
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = get_object_from_setting('facebook_login_serializer_class',
                                               FacebookLoginDeserializer)

    @classmethod
    def as_view(cls, *args, **kwargs):
        if facepy is None:
            raise TypeError('install rest-framework-auth-toolkit[facebook] '
                            'to enable Facebook logins')

        # TODO error if settings are missing

        return super(FacebookLoginView, cls).as_view(*args, **kwargs)

    def post(self, request):
        deserializer = self.get_serializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        data = deserializer.validated_data

        token = Token.objects.create_token(**data)
        return Response({'token': token.key})


class LogoutView(views.APIView):
    """Revoke current API auth token.

    Response

    `200 OK`
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.auth
        if isinstance(token, Token):
            token.revoke()

        return Response(status=status.HTTP_200_OK)


def send_email(request, user, address, confirmation):
    """Send the confirmation email for a new user."""
    subject = _('Confirm your email address')
    from_address = get_setting('email_confirmation_from')

    lookup_field = get_setting('email_confirmation_lookup_field', 'id')
    confirmation_url = request.build_absolute_uri(
        reverse('app-auth:email-confirmation',
                kwargs={lookup_field: getattr(confirmation, lookup_field)}))
    # The url template tag doesn't include scheme/domain/port, pass a helper
    base_url = request.build_absolute_uri('/')[:-1]

    context = {'base_url': base_url, 'confirmation_url': confirmation_url}
    txt_content = render_to_string('rest_auth_toolkit/email_confirmation.txt', context)
    html_content = render_to_string('rest_auth_toolkit/email_confirmation.html', context)

    send_mail(subject=subject,
              from_email=from_address, recipient_list=[address],
              message=txt_content, html_message=html_content,
              fail_silently=False)


def activate_user(sender, **kwargs):
    """Mark user as active when a confirmation link is visited.

    This handler is connected to the email_confirmed signal in
    RestAuthToolkitConfig.ready.
    """
    kwargs['user'].is_active = True
    kwargs['user'].save(update_fields=['is_active'])
