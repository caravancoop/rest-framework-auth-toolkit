from datetime import datetime

from django.urls import reverse

import pytest

from demo.accounts.models import User, APIToken


@pytest.mark.parametrize("email", [
    "zack@example.com",
    "zack@EXAMPLE.COM",
])
def test_signup(db, django_app, mailoutbox, email):
    params = {"email": email, "password": "correct battery horse staple"}
    resp = django_app.post_json(reverse("auth:signup"), params=params, status=201)

    assert resp.json == {"email": "zack@example.com"}
    user = User.objects.last()
    assert user.email == "zack@example.com"
    assert user.has_usable_password()
    m = mailoutbox[0]
    assert len(mailoutbox) == 1
    assert list(m.to) == ["zack@example.com"]


def test_signup_same_as_password(db, django_app):
    params = {"email": "bobby@example.com", "password": "bobby@example.com"}
    resp = django_app.post_json(reverse("auth:signup"), params=params, status=400)

    assert "password" in resp.json


def test_signup_missing_email(db, django_app):
    params = {"password": "little bobby passwords"}
    resp = django_app.post_json(reverse("auth:signup"), params=params, status=400)

    assert "email" in resp.json


def test_signup_invalid_email(db, django_app):
    params = {"email": "bobby", "password": "bobby@example.com"}
    resp = django_app.post_json(reverse("auth:signup"), params=params, status=400)

    assert "email" in resp.json


@pytest.mark.parametrize("email", [
    "bob@example.com",
    "bob@example.COM",
])
def test_signup_already_exists(db, django_app, user0, email):
    params = {"email": email, "password": "pass123@!!"}
    resp = django_app.post_json(reverse("auth:signup"), params=params, status=400)

    assert "email" in resp.json


def test_signup_different_address(db, django_app, user0):
    params = {"email": "ZACK@EXAMPLE.com", "password": "goodpass"}
    resp = django_app.post_json(reverse("auth:signup"), params=params, status=201)

    assert resp.json == {"email": "ZACK@example.com"}


def test_confirm_email(db, django_app, user0, emailconfirmation0):
    assert not user0.is_active
    assert emailconfirmation0.confirmed is None

    django_app.get(reverse("app-auth:email-confirmation",
                           kwargs={"external_id": emailconfirmation0.external_id}))

    user0.refresh_from_db()
    emailconfirmation0.refresh_from_db()
    assert user0.is_active
    assert isinstance(emailconfirmation0.confirmed, datetime)


@pytest.mark.parametrize("email", [
    "bob@example.com",
    "bob@example.COM",
])
def test_login(db, django_app, user0, email):
    assert user0.last_login is None

    params = {"email": email, "password": "pass123"}
    resp = django_app.post_json(reverse("auth:login"), params=params, status=200)

    assert "token" in resp.json
    user0.refresh_from_db()
    assert isinstance(user0.last_login, datetime)


def test_login_unknown_user(db, django_app):
    params = {"email": "pierre@example.com", "password": "correct battery horse staple"}
    resp = django_app.post_json(reverse("auth:login"), params=params, status=400)

    assert "errors" in resp.json


def test_logout(db, django_app, token0):
    headers = {"Authorization": "Bearer {}".format(token0.key)}
    django_app.post_json(reverse("auth:logout"), headers=headers, status=200)

    assert APIToken.objects.filter(key=token0.key).first() is None
