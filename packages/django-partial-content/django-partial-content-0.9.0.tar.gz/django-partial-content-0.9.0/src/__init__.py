from django.http import HttpRequest, HttpResponse

import django.views.static

import re
import io

LIMIT = 1024 ** 2


serve_func = django.views.static.serve


def handler(request, *args, **kwargs):
    return handle(request, serve_func(request, *args, **kwargs))


django.views.static.serve = handler


def handle(request: HttpRequest, response: HttpResponse):
    if 'range' in request.headers and response.status_code == 200:
        header = request.headers['range']
        if header.find('bytes=') == 0:
            splitter = re.compile('[-,]')
            parts = splitter.split(header[6:].strip())
            start = int(parts[0])
            end = int(parts[1]) + 1 if parts[1] else start + LIMIT
            content = response.getvalue()
            if end > len(content):
                end = len(content)
            response._set_streaming_content(io.BufferedReader(io.BytesIO(content[start:end])))
            response._headers['content-length'] = 'Content-Length', str(end - start)
            response._headers['content-range'] = 'Content-Range', 'bytes %d-%d/%d' % (start, end - 1, len(content))
            del response._headers['content-disposition']
            response.status_code = 206

    return response
