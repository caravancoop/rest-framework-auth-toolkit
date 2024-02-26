# Changelog for Rest-Framework-Auth-Toolkit

## v0.13

Tested with Python 3.10, 3.11 and 3.12,
and Django 3.2, 4.1 and 4.2.


## v0.12

Library tested with Python 3.9 and 3.10,
and Django 3.2, 4.0 and 4.1 (#172, #208)

`SignupDeserializer.create` passes all validated data to the
`AUTH_USER.objects.create_user` method, so that data for extra
fields in your serializer subclass gets passed automatically


## v0.11

Tests are run with combinations of Python 3.8 and 3.9
and Django 2.2 and 3.1 (#115)

A number of improvements make it easier to integrate in your
project (#135):

New class `TokenAuthentication` can be directly added to
django-rest-framework settings for API auth.

The `BaseAPIToken` class provides a default `revoke` method
needed by the logout view.

Email addresses can be normalized by serializers using the
new `CustomEmailField` class.  Default behaviour does not
normalize before checking uniqueness or saving data.

Login now sends `user_logged_in` signal.  If you have
`django.contrib.auth` in `INSTALLED_APPS` and your user model
has a `last_login` field, it will be automatically updated.

### Upgrade notes

`BaseUserEmail.natural_key` now returns a 1-element tuple
with the email field value.

Use Python 3.8 or 3.9 and Django 2.2 (LTS release) or 3.1.


## v0.10

Django password validators are now applied during signup #23

Facebook login is fixed (silent error in previous version due
to API change) #36

Partial test coverage #33

API docs for the demo app #48

### Upgrade notes

Python 3 is required!

If you were using `str(apitoken)` or equivalents to get the auth token
in headers, you have to use `apitoken.key` now.


## v0.9

Run tests and demo with Python 3.7 and Django 2.0.

Package library with flit.

### Upgrade notes

The facepy dependency is now optional.  Depend on
`rest-framework-auth-toolkit[facebook]` to have it automatically installed.


## v0.8

Set up internationalization.


## v0.7

Added abstract base user model, with email as username.


## v0.6

It is now possible to use login without signup.


## v0.5

First published version.

Includes views for signup (with email confirmation), login and logout.
A demo app shows how to integrate and configure the library.
