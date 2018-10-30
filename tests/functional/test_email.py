from django.urls import reverse

from demo.accounts.models import User, APIToken


def test_signup(db, django_app, mailoutbox):
    params = {"email": "zack@example.com", "password": "correct battery horse staple"}
    django_app.post_json(reverse("auth:signup"), params=params, status=201)

    m = mailoutbox[0]
    assert len(mailoutbox) == 1
    assert list(m.to) == ['zack@example.com']


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
    params = {"email": "julien@example.com", "password": "unitpass123", "is_active": True}
    resp = django_app.post_json(reverse("auth:signup"), params=params, status=400)

    assert 'email' in resp.json


def test_login_unknown_user(db, django_app):
    params = {"email": "pierre@example.com", "password": "correct battery horse staple"}
    resp = django_app.post_json(reverse("auth:login"), params=params, status=400)

    assert 'errors' in resp.json
