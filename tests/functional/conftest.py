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
def userfb0(db):
    return User.objects.create_user(
        email='alex@example.com',
        first_name='Alex',
        last_name='Facebook',
        facebook_id='1234dddd',
        facebook_access_token='oauthtoken1111',
        is_active=True,
    )


@pytest.fixture
def token0(user0):
    return APIToken.objects.create_token(
        user=user0,
    )

@pytest.fixture
def token1(userfb0):
    return APIToken.objects.create_token(
        user=userfb0,
    )