from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
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
    """Create a user and send a confirmation email.

    Response: 201 Created.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = get_object_from_setting('signup_serializer_class',
                                               SignupDeserializer)
    email_confirmation_class = get_object_from_setting('email_confirmation_class',
                                                       None)

    def post(self, request):
        """Handle the request.

        If the setting email_confirmation_send_email is true (default),
        the function send_email will be called.  That function requires
        that your project defines defines two email templates:
            - rest_auth_toolkit/email_confirmation.txt
            - rest_auth_toolkit/email_confirmation.html

        The templates will be passed the User and EmailConfirmation instances
        (as variables *user* and *confirmation*).  To help generating links,
        a variable *base_url* with a value like "https://domain" (scheme,
        domain and optional port depending on the request, but no path), which
        lets you write code like `{{ base_url }}{% url "my-route" %}`.

        It is up to your project to define what the link is.  The demo app
        demonstrates a simple Django view that validates the email validation
        token in the URL; for a project with a front-end site (e.g. a JavaScript
        app) on a different domain than the Django API, a custom template tag
        could be used to generate the right URL for the front-end site.

        If the setting is false, the user will be active immediately.
        """
        deserializer = self.get_serializer(data=request.data)
        deserializer.is_valid(raise_exception=True)

        confirm_email = get_setting('email_confirmation_send_email', True)

        if not confirm_email:
            deserializer.save(is_active=True)
        else:
            user = deserializer.save()

            if self.email_confirmation_class is None:
                raise MissingSetting('email_confirmation_class')

            confirmation = self.email_confirmation_class.objects.create(user=user)
            email_field = user.get_email_field_name()
            send_email(request, user, getattr(user, email_field), confirmation)

        return Response(status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """Authenticate a user, return an API auth token if valid.

    Response:

    ```json
    {"token": "string"}
    ```
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = get_object_from_setting('login_serializer_class',
                                               LoginDeserializer)

    def post(self, request):
        deserializer = self.get_serializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        data = deserializer.validated_data

        token = Token.objects.create_token(**data)
        return Response({'token': token.key})


class FacebookLoginView(generics.GenericAPIView):
    """Create a user from a Facebook signed request (from auth response).

    The user will be active immediately, with an unusable password.

    Response:

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

    Response: 200 OK.
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

    # The url template tag doesn't include scheme/domain/port, pass a helper
    base_url = request.build_absolute_uri('/')[:-1]

    context = {
        'user': user,
        'confirmation': confirmation,
        'base_url': base_url,
    }
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
