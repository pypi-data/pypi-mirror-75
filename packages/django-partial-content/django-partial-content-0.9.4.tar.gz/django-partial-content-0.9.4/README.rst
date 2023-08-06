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

The lowest Django version I could get it work is 1.8. Also works on Python 2.7. Tested on Chrome-like browser and Firefox.

Known issues:
 - Multiple ranges aren't supported.
