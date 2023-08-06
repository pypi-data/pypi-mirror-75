import os
import stat
import mimetypes
import posixpath

from urllib.parse import unquote

from django.conf import settings
from django.http import Http404, HttpResponse, FileResponse, \
    HttpResponseNotModified
from django.views import static
from django.utils.http import http_date
from django.views.static import was_modified_since
from django.contrib.staticfiles import finders
from django.utils.encoding import force_bytes

from . import app_settings
from .utils import render


def serve(request, path, insecure=False, **kwargs):
    """
    Serve static files below a given point in the directory structure or
    from locations inferred from the staticfiles finders.

    To use, put a URL pattern such as::

        from django.contrib.staticfiles import views

        url(r'^(?P<path>.*)$', views.serve)

    in your URLconf.

    It uses the django.views.static.serve() view to serve the found files.
    """
    if not settings.DEBUG and not insecure:
        raise Http404
    normalized_path = posixpath.normpath(unquote(path)).lstrip('/')
    if '{}/'.format(app_settings.DIRECTORY_SUFFIX) \
            in '{}/'.format(normalized_path):
        raise Http404("Refusing access to nested '{}' as it would not be "
                      "accessible in production".format(path))
    absolute_path = finders.find(normalized_path)
    if os.path.isdir('%s%s' % (absolute_path, app_settings.DIRECTORY_SUFFIX)):
        return served(request, absolute_path)
    if not absolute_path:
        if path.endswith('/') or path == '':
            raise Http404("Directory indexes are not allowed here.")
        raise Http404("'%s' could not be found" % path)
    document_root, path = os.path.split(absolute_path)
    response = static.serve(
        request,
        path,
        document_root=document_root,
        **kwargs
    )

    if isinstance(response, FileResponse):
        contents = render(absolute_path)
        response.streaming_content = [contents]
        response['Content-Length'] = len(contents)

    return response


def served(request, absolute_path):
    top = '%s%s' % (absolute_path, app_settings.DIRECTORY_SUFFIX)
    latest = -1
    filenames = []

    for root, _, files in os.walk(top, followlinks=True):
        for filename in [os.path.join(root, x) for x in files]:
            if filename.endswith('~'):
                continue
            filenames.append(filename)
            latest = max(latest, os.stat(filename)[stat.ST_MTIME])

    mimetype = mimetypes.guess_type(absolute_path)[0] \
        or 'application/octet-stream'

    if not was_modified_since(
        request.META.get('HTTP_IF_MODIFIED_SINCE'),
        latest,
    ):
        return HttpResponseNotModified(content_type=mimetype)

    contents = b''.join(render(x) for x in sorted(filenames))

    # Ensure bytes otherwise our len(contents) can be short!
    contents = force_bytes(contents)

    response = HttpResponse(contents, content_type=mimetype)
    response['Last-Modified'] = http_date(latest)
    response['Content-Length'] = len(contents)

    return response
