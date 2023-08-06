import src
import django.views.static
from django.test import RequestFactory
from django.conf import settings

settings.configure()


def test_normal_file():
    factory = RequestFactory()
    request = factory.get('/test/file', HTTP_RANGE='bytes=0-5')
    response = django.views.static.serve(request, '/test/file', '.')
    assert response.status_code == 206
    assert len(response.getvalue()) == 6
    assert response.get('Content-Range') == 'bytes 0-5/724'


def test_big_file():
    factory = RequestFactory()
    request = factory.get('/test/big', HTTP_RANGE='bytes=4-')
    response = django.views.static.serve(request, '/test/big', '.')
    assert response.status_code == 206
    value = response.getvalue()
    assert len(value) == src.LIMIT
    assert value[335397] == 98
    assert response.get('Content-Range') == 'bytes 4-' + str(src.LIMIT + 3) + '/15920290'


def test_other_request():
    factory = RequestFactory()
    request = factory.get('/test/file')
    response = django.views.static.serve(request, '/test/file', '.')
    assert response.status_code == 200
    assert len(response.getvalue()) == 724
    assert response.get('Content-Range') is None
