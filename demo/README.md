# Demo application for Rest-Framework-Auth-Toolkit

This is a minimal Django project that shows how to use
the package and helps checking if changes break usage.

This app is also used by the automated tests.


## How to install

Run this command once from the repository root:

```
python setup-develop.py develop
```

This makes the package `rest_auth_toolkit` importable by the demo app,
with local changes immediately seen.

Go in the `demo` directory and install the other dependencies:

```
pip install -r requirements.txt
```

# How to run

Define the environment variables needed by the app:

```
export DEMO_FACEBOOK_APP_ID="..."
export DEMO_FACEBOOK_APP_SECRET_KEY="..."
```

(using a [virtualenvwrapper hook](https://virtualenvwrapper.readthedocs.io/en/latest/scripts.html#postactivate)
or a `.env` file with [direnv](https://direnv.net/) is a good ideae to make this automatic)

You can then run Django commands:

```
python manage.py migrate
python manage.py runserver
```

Then head on to `http://localhost:8000/api/` to see the endpoints available.
