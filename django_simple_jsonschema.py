from django.conf import settings
from django.http import HttpResponse


class SimpleJsonschemaException(Exception):
    pass


class SimpleJsonschemaMiddleware(object):

    def __init__(self):
        self._schema = settings.SIMPLE_JSONSCHEMA

    def get_schema(self, request):
        view_name = request.resolver_match.view_name
        method = request.method
        key = method + ':' + view_name
        return self._schema[key]

    def process_view(self, request, view_func, view_args, view_kwargs):
        # schema = self.get_schema(request)
        pass

    def process_exception(self, request, exception):
        if not isinstance(exception, SimpleJsonschemaException):
            return None
        return HttpResponse('{}', content_type='application/json')
