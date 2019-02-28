from django.urls import reverse


def test_account(db, django_app, token0):
    headers = {"Authorization": "Bearer {}".format(token0.key)}
    resp = django_app.get(reverse("user-profile"), headers=headers, status=200)

    assert resp.json == {
        "first_name": "Bobby",
        "last_name": "Email",
        "date_joined": "2018-02-15T15:35:02Z",
    }
