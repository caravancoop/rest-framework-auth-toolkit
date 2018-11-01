from django.urls import reverse

from demo.accounts.models import User


def test_signup(db, django_app, mailoutbox):
    params = {"email": "zack@example.com", "password": "correct battery horse staple"}
    django_app.post_json(reverse("auth:signup"), params=params, status=201)

    m = mailoutbox[0]
    assert len(mailoutbox) == 1
    assert list(m.to) == ['zack@example.com']
    users = User.objects.all()
    assert len(users) == 1
    user = users[0]
    assert user.email == 'zack@example.com'
    assert user.has_usable_password()


def test_signup_same_as_password(db, django_app):
    params = {"email": "bobby@example.com", "password": "bobby@example.com"}
    resp = django_app.post_json(reverse("auth:signup"), params=params, status=400)

    assert 'password' in resp.json


def test_signup_invalid_email(db, django_app):
    params = {"email": "bobby", "password": "bobby@example.com"}
    resp = django_app.post_json(reverse("auth:signup"), params=params, status=400)

    assert 'email' in resp.json


def test_signup_already_exists(db, django_app):
    User.objects.create(
        email='julien@example.com',
        password='unitpass123',
        is_active=True,
    )
    params = {"email": "julien@example.com", "password": "pass123", "is_active": True}
    resp = django_app.post_json(reverse("auth:signup"), params=params, status=400)

    assert 'email' in resp.json


def test_login(db, django_app):
    User.objects.create_user(
        email='bob@example.com',
        password='unitpass123',
        is_active=True,
    )
    params = {"email": "bob@example.com", "password": "unitpass123"}
    resp = django_app.post_json(reverse("auth:login"), params=params, status=200)

    assert 'token' in resp.json


def test_login_unknown_user(db, django_app):
    params = {"email": "pierre@example.com", "password": "correct battery horse staple"}
    resp = django_app.post_json(reverse("auth:login"), params=params, status=400)

    assert 'errors' in resp.json
