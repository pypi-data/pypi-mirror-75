# Django Email Tools

[![CircleCI](https://circleci.com/gh/pennlabs/django-email-tools.svg?style=shield)](https://circleci.com/gh/pennlabs/django-email-tools)
[![Coverage Status](https://codecov.io/gh/pennlabs/django-email-tools/branch/master/graph/badge.svg)](https://codecov.io/gh/pennlabs/django-email-tools)
[![PyPi Package](https://img.shields.io/pypi/v/django-email-tools.svg)](https://pypi.org/project/django-email-tools/)

## Requirements

* Python 3.6+
* Django 2.2+

## Installation

Install with pip `pip install django-email-tools`

Add `email_tools` to `INSTALLED_APPS`

```python
INSTALLED_APPS = (
    ...
    'email_tools.apps.EmailToolsConfig',
    ...
)
```

Add something like the following to `urls.py`

```python
if settings.DEBUG:
    urlpatterns = [
        path("emailpreview/", include("email_tools.urls", namespace="email_tools")),
    ] + urlpatterns
```

## Documentation

All settings are handled within a `EMAIL_TOOLS` dictionary.

Example:

```python
PLATFORM_ACCOUNTS = {
    'FROM_EMAIL': 'example@example.com',
    'TEMPLATE_DIRECTORY': os.path.join(settings.BASE_DIR, "templates", "emails"),
}
```

The available settings are:

`FROM_EMAIL` the email to send from.

`TEMPLATE_DIRECTORY` the path to a directory containing `.html` files used in emails.

## Usage

Django Email Tools contains two main parts.

First, is `email_tools.emails.send_email` a utility to send html emails given a django template and context.

The second is a debugging page that allows you to see what the rendered result of an email template would look like. This page also allows you to get a list of variables used by the template and modify those variables and see results in real-time.

## Changelog

See [CHANGELOG.md](https://github.com/pennlabs/django-email-tools/blob/master/CHANGELOG.md)

## License

See [LICENSE](https://github.com/pennlabs/django-email-tools/blob/master/LICENSE)
