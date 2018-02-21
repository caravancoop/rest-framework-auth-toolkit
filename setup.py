from setuptools import setup

long_description = '''
This libary provides mixins and views to handle signup, login and logout
in an API built with django-rest-framework.  After login, client
applications get a token for the API requests.

Email-based signups and Facebook login are supported.

Contrary to other similar modules, rest-auth-toolkit doess not provide
a set of Django apps to include and configure in your settings, but a
collection of mixins, base classes, base views and simple templates
that you can integrate and customize in your own apps.
'''

setup(
    name='Rest-Framework-Auth-Toolkit',
    version='0.6',
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
    ],
    packages=[
        'rest_auth_toolkit',
    ],
    include_package_data=True,
    install_requires=[
        'django',
        'djangorestframework',
        'facepy',
    ],
)
