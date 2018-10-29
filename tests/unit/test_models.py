def test_baseemailuser_str(user0):
    assert str(user0) == 'bob@example.com'


def test_baseemailuser_get_short_name(user0):
    assert user0.get_short_name() == 'bob@example.com'


def test_baseemailuser_natural_key(user0):
    assert user0.natural_key() == 'bob@example.com'
