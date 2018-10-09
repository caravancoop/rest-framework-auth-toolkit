```
                       __                   __  __         __              ____   _ __
       ________  _____/ /_     ____ ___  __/ /_/ /_       / /_____  ____  / / /__(_) /_
      / ___/ _ \/ ___/ __/ ___/ __ `/ / / / __/ __ \  ___/ __/ __ \/ __ \/ / //_/ / __/
     / /  /  __(__  ) /_  /__/ /_/ / /_/ / /_/ / / / /__/ /_/ /_/ / /_/ / / ,< / / /_
    /_/   \___/____/\__/     \__,_/\__,_/\__/_/ /_/     \__/\____/\____/_/_/|_/_/\__/

```

This libary provides mixins and views to handle signup, login and
logout in an API built with django-rest-framework.  After login,
client applications get a token for the API requests.

Email-based signups are supported out of the box.
Other methods require you to specify an extra in your requirements;
for example, to use Facebook login you need to depend on
`rest-framework-auth-toolkit[facebook]`.

Contrary to other similar modules, rest-auth-toolkit doess not provide
a set of Django apps to include and configure in your settings, but a
collection of mixins, base classes, base views and simple templates
that you can integrate and customize in your own apps.

⚠️ This library is not stable yet, make sure to pin your dependencies.
Recommended form: `rest-framework-auth-toolkit == 0.9.*`
