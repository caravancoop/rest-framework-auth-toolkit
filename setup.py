from setuptools import setup

setup(
    name='Rest-Framework-Auth-Toolkit',
    version='0.5',
    description='Simple, flexible signup and login for APIs',
    long_description=long_description,
    url='https://github.com/caravancoop/rest-framework-auth-toolkit',
    author=u'Éric Araujo',
    author_email='earaujo@caravan.coop',
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
    install_requires=[
        'django',
        'djangorestframework',
        'facepy',
    ],
)
