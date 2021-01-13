from django.contrib.auth import get_user_model

from rest_framework.fields import EmailField, empty


User = get_user_model()


class CustomEmailField(EmailField):
    """Subclass of EmailField that adds normalization."""

    def run_validation(self, data=empty):
        if data != empty:
            data = User.objects.normalize_email(data)
        return super().run_validation(data)
