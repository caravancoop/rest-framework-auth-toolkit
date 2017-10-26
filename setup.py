from setuptools import setup

setup(
    name='Rest-Framework-Auth-Toolkit',
    version='0.4',
    url='https://github.com/caravancoop/configstore',
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
