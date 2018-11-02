import pytest

from demo.accounts.models import User, APIToken


@pytest.fixture
def user0(db):
    return User.objects.create_user(
        email='bob@example.com',
        password='pass123',
        is_active=True,
    )


@pytest.fixture
def token0(user0):
    return APIToken.objects.create_token(
        user=user0,
    )
