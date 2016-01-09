# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from jsonschema import Draft4Validator
import json


class SimpleJsonschemaMiddleware(object):

    def __init__(self):
        self.set_schemas(settings.SIMPLE_JSONSCHEMA)
        self.default_encoding = 'utf-8'

    def get_encoding(self, request):
        return request.encoding if request.encoding else self.default_encoding

    def set_schemas(self, simple_jsonschema):
        self._schemas = {}
        for key, schema in simple_jsonschema.items():
            methods, view_name = key
            if isinstance(methods, tuple):
                for method in methods:
                    schema_id = method.upper() + ':' + view_name
                    self._schemas[schema_id] = Draft4Validator(schema)
            elif isinstance(methods, str):
                schema_id = methods.upper() + ':' + view_name
                self._schemas[schema_id] = Draft4Validator(schema)

    def get_schema(self, request):
        view_name = request.resolver_match.view_name
        method = request.method
        key = method + ':' + view_name
        return self._schemas[key]

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            schema = self.get_schema(request)
        except KeyError:
            return None
        encoding = self.get_encoding(request)
        json_data = json.loads(request.body.decode(encoding), encoding=encoding)
        errors = list(schema.iter_errors(json_data))
        if len(errors):
            errors_data = {}
            errors_data['url'] = request.path
            errors_data['method'] = request.method
            errors = [
                {'message': e.message, 'path': list(e.path), 'schema_path': list(e.schema_path)}
                for e in errors
            ]
            errors_data['errors'] = errors
            rv = json.dumps(errors_data)
            return HttpResponse(rv, content_type='application/json')
        setattr(request, 'json_data', json_data)
        return None
