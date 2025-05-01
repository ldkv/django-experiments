import json

from django.http import HttpRequest, HttpResponse


def non_html_debug_toolbar(get_response):
    """
    The Django Debug Toolbar usually only works for views that return HTML.
    This middleware wraps any JSON response in HTML if the request
    has a 'debug' query parameter (e.g. http://localhost/foo?debug)

    Docs: https://docs.djangoproject.com/en/5.0/topics/http/middleware/
    Adapted from: https://gist.github.com/fabiosussetto/c534d84cbbf7ab60b025
    """

    def middleware(request: HttpRequest):
        response: HttpResponse = get_response(request)
        if request.GET.get("debug", None) is not None:
            content = json.dumps(json.loads(response.content), sort_keys=True, indent=2)
            response = HttpResponse("<html><body><pre>{}</pre></body></html>".format(content))

        return response

    return middleware
