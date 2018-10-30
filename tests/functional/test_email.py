from django.urls import reverse


def test_signup(db, django_app):
    params = {"email": "zack@example.com", "password": "correct battery horse staple"}
    django_app.post_json(reverse("auth:signup"), params=params, status=201)


def test_signup_same_as_password(db, django_app):
    params = {"email": "bobby@example.com", "password": "bobby@example.com"}
    resp = django_app.post_json(reverse("auth:signup"), params=params, status=400)

    assert 'password' in resp.json


def test_signup_invalid_email(db, django_app):
    params = {"email": "bobby", "password": "bobby@example.com"}
    resp = django_app.post_json(reverse("auth:signup"), params=params, status=400)

    assert 'email' in resp.json
