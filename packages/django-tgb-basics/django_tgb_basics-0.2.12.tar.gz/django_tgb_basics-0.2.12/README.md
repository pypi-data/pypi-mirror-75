# django_tgb_basics

This is a collection of useful (basic) features that I usually use in my
Django Projects. I realize that I never use every feature in other libraries,
so I decide to put together the most important ones to easilly reuse.

# Installation and setup

Install with your python package manager as usually you do.
To install with pip:

```
pip install django_tgb_basics
```

Once the package is installed you should edit your `settings.py` file
and add (or modify) the `AUTHENTICATION_BACKENDS` to use the `EmailAuthBackend`.
It's not necessary add to installed apps if you only need the auth backend.

```
AUTHENTICATION_BACKENDS = [
    'django_tgb_basics.backends.EmailAuthBackend',
    # Other authentications backends
]
```

But if you need another features like `MultiSerializerViewSet`, you need to
add `django_tgb_basics` to `INSTALLED_APPS` in the `settings.py` file of your
project.

```
INSTALLED_APPS = [
    ...
    'django_tgb_basics',
    ...
]
```
