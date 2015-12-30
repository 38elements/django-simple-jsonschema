from __future__ import unicode_literals
from django.conf import settings
from django.http import HttpResponse
from jsonschema import Draft4Validator
import json


class SimpleJsonschemaException(Exception):

    def __init__(self, errors):
        self.errors = errors


class SimpleJsonschemaMiddleware(object):

    def __init__(self):
        self.set_schemas(settings.SIMPLE_JSONSCHEMA)

    def set_schemas(self, simple_jsonschema):
        self._schemas = {}
        for key, schema in simple_jsonschema.items():
            methods, view_name = key
            if isinstance(methods, tuple):
                for method in methods:
                    schema_id = method.upper() + ':' + view_name
                    self._schemas[schema_id] = Draft4Validator(schema)
            elif isinstance(methods, unicode):
                schema_id = methods.upper() + ':' + view_name
                self._schemas[schema_id] = Draft4Validator(schema)

    def get_schema(self, request):
        view_name = request.resolver_match.view_name
        method = request.method
        key = method + ':' + view_name
        return self._schemas[key]

    def process_view(self, request, view_func, view_args, view_kwargs):
        schema = self.get_schema(request)
        json_data = json.loads(request.body.decode(request.encoding), encoding=request.encoding)
        errors = list(schema.iter_errors(json_data))
        if len(errors):
            raise SimpleJsonschemaException(errors)
        setattr(request, 'json_data', json_data)
        return None

    def process_exception(self, request, exception):
        if not isinstance(exception, SimpleJsonschemaException):
            return None
        errors = [
            {'message': e.message, 'path': e.path, 'schema_path': e.schema_path}
            for e in exception.errors
        ]
        rv = json.dumps(errors)
        return HttpResponse(rv, content_type='application/json')
