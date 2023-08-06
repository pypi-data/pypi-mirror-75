from django.http import HttpRequest, HttpResponse

import django.views.static

import re
import io
import os

LIMIT = 10 * 1024 ** 2


serve_func = django.views.static.serve


def handler(request, *args, **kwargs):
    return handle(request, serve_func(request, *args, **kwargs))


django.views.static.serve = handler


def handle(request: HttpRequest, response: HttpResponse):
    if request.META.get('HTTP_RANGE') and response.status_code == 200:
        header = request.META['HTTP_RANGE']
        if header.find('bytes=') == 0:
            splitter = re.compile('[-,]')
            parts = splitter.split(header[6:].strip())
            start = int(parts[0])
            end = int(parts[1]) + 1 if parts[1] else start + LIMIT
            content_reader = response.file_to_stream
            content_reader.seek(0, os.SEEK_END)
            total_size = content_reader.tell()
            if end > total_size:
                end = total_size
            content_reader.seek(start)
            content_length = end - start
            content = content_reader.read(content_length)
            response._set_streaming_content(io.BufferedReader(io.BytesIO(content)))
            response._headers['content-length'] = 'Content-Length', str(content_length)
            response._headers['content-range'] = 'Content-Range', 'bytes %d-%d/%d' % (start, end - 1, total_size)
            response.status_code = 206

    return response
