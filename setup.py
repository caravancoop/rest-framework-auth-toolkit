# encoding: utf-8
from setuptools import setup

long_description = '''
This libary provides mixins and views to handle signup, login and logout
in an API built with django-rest-framework.  After login, client
applications get a token for the API requests.

Email-based signups are supported out of the box.
Other methods require you to specify an extra in your requirements;
for example, to use Facebook login you need to depend on
`rest-framework-auth-toolkit[facebook]`.

Contrary to other similar modules, rest-auth-toolkit doess not provide
a set of Django apps to include and configure in your settings, but a
collection of mixins, base classes, base views and simple templates
that you can integrate and customize in your own apps.

⚠️ This library is not stable yet, make sure to pin your dependencies.
Recommended form: rest-framework-auth-toolkit == 0.9.*
'''

setup(
    name='Rest-Framework-Auth-Toolkit',
    version='0.9.dev',
    description='Simple, flexible signup and login for APIs',
    long_description=long_description,
    url='https://github.com/caravancoop/rest-framework-auth-toolkit',
    author='Caravan Coop',
    author_email='hi@caravan.coop',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
    ],
    packages=[
        'rest_auth_toolkit',
    ],
    include_package_data=True,
    install_requires=[
        'django >= 1.11',
    ],
    extras_require={
        'facebook': ['facepy'],
    },
)
