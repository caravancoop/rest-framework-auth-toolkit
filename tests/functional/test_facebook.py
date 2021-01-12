from datetime import datetime

from django.urls import reverse

from pretend import stub


def fake_signed_request(signed_request=None, application_secret_key=None,
                        application_id=None, api_version=None):
    token_object = stub(token="fb oauth token")
    user_object = stub(oauth_token=token_object)
    return stub(user=user_object)


def fake_graph_api_get(self, path="", page=False, retry=3, **options):
    return {
        "email": "alex@example.com",
        "first_name": "Alex",
        "last_name": "Facebook",
        "third_party_id": "1234dddd",
    }


def fake_get_access_token(access_token, application_id, application_secret_key,
                          api_version=None):
    return "oauth token extended", "other setting"


def test_facebook_login(django_app, monkeypatch, userfb0, token1):
    monkeypatch.setattr("facepy.GraphAPI.get", fake_graph_api_get)
    monkeypatch.setattr("facepy.SignedRequest", fake_signed_request)
    monkeypatch.setattr("facepy.get_extended_access_token", fake_get_access_token)
    assert userfb0.last_login is None

    params = {"signed_request": "abcd_signed_request"}
    resp = django_app.post_json(reverse("auth:fb-login"), params=params, status=200)

    assert resp.json.keys() == {"token"}
    assert resp.json["token"] != token1.key
    userfb0.refresh_from_db()
    assert isinstance(userfb0.last_login, datetime)
