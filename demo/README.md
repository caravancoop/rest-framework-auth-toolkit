# Demo application for Rest-Framework-Auth-Toolkit

This is a minimal Django project that shows how to use
the package and helps checking if changes break usage.

This app is also used by the automated tests.

Move to the demo directory in your terminal:

```
cd demo
```

## How to install

Install the app dependencies, including `rest_auth_toolkit` from the parent
directory, with this command:

```
pip install -r requirements.txt
```

# How to run

Define the environment variables needed by the app:

```
export DATABASE_URL=postgres://restauth:password@localhost:5432/demo
export DEMO_FACEBOOK_APP_ID="..."
export DEMO_FACEBOOK_APP_SECRET_KEY="..."
```

(using a [virtualenvwrapper hook](https://virtualenvwrapper.readthedocs.io/en/latest/scripts.html#postactivate)
or a `.env` file with [direnv](https://direnv.net/) is a good ideae to make this automatic)

You can then run Django commands (still inside the `demo` directory):

```
python manage.py migrate
python manage.py runserver
```

Then head on to `http://localhost:8000/api/` to see the endpoints available.
