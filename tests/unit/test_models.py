import pytest

from demo.accounts.models import User, APIToken


def test_user_str(user0):
    assert str(user0) == 'bob@example.com'


def test_user_get_short_name(user0):
    assert user0.get_short_name() == 'bob@example.com'


def test_user_natural_key(user0):
    assert user0.natural_key() == ('bob@example.com',)


def test_user_manager_get_by_natural_key(user0, user1):
    user = User.objects.get_by_natural_key('julien@example.com')

    assert user == user1


def test_user_manager_create_user(db):
    user = User.objects.create_user('frank@eXaMPle.com', 'superpassword')

    assert user.id >= 1
    assert user.email == 'frank@example.com'
    assert user.has_usable_password()
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


def test_user_manager_create_superuser(db):
    user = User.objects.create_superuser('staff@EXAMPLE.COM', 'wowpassword')

    assert user.id >= 1
    assert user.email == 'staff@example.com'
    assert user.has_usable_password()
    assert user.is_active
    assert user.is_staff
    assert user.is_superuser


@pytest.mark.parametrize('fields', [
    {'is_staff': False},
    {'is_superuser': False},
    {'is_staff': False, 'is_superuser': False},
])
def test_user_manager_create_superuser_bad_fields(db, fields):
    with pytest.raises(ValueError):
        User.objects.create_superuser('staff@example.com', 'wowpassword', **fields)


def test_apitoken_str(token0):
    assert str(token0) == 'API token for bob@example.com'


def test_apitoken_save_create_generates_key(user0):
    token = APIToken(user=user0)
    assert token.key == ''

    token.save()

    assert isinstance(token.key, str)
    assert len(token.key) == 40


def test_apitoken_save_create_keeps_key(user0):
    token = APIToken(user=user0, key='1234abcd')

    token.save()

    assert token.key == '1234abcd'


def test_apitoken_save_update_keeps_key(token0, user1):
    key = token0.key

    token0.user = user1
    token0.save()

    assert token0.key == key


def test_apitoken_custom_generate_key(monkeypatch, user0):
    monkeypatch.setattr(APIToken, 'generate_key', lambda self: '2345bcde')
    token = APIToken(user=user0)

    token.save()

    assert token.key == '2345bcde'


def test_apitoken_manager_create_token(user0):
    token = APIToken.objects.create_token(user=user0)

    assert len(token.key) == 40
