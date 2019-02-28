# Changelog for Rest-Framework-Auth-Toolkit


## v0.10 (unreleased)

Django password validators are now applied during signup.

Facebook login is fixed (silent error in previous version due to API change).

Partial test coverage.

API docs for the demo app.


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
