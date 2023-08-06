.. image:: https://img.shields.io/pypi/v/django-partial-content.svg
  :target: https://pypi.python.org/pypi/django-partial-content/

Support for partial content in Django staticfiles.

After an installation add the following app to your settings.

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django-partial-content',
        ...
    ]

After that Django will respect `Range` header in requests to static files. Note that using `staticfiles` module in production is not recommended. The extension is only for ease of development.

Tested with Django (2.0, 3.0), SRWare Iron and files no larger than 40MB.

Known issues:
 - Multiple ranges aren't supported.
 - Big files aren't supported yet.
