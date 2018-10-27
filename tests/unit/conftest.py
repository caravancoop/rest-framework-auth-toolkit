import pytest

from demo.accounts.models import User


@pytest.fixture
def user0(db):
    return User.objects.create(
        email='bob@example.com',
    )
