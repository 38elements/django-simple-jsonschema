from django.conf import settings
from django.http import HttpResponse
from jsonschema import Draft4Validator
from jsonschema.exceptions import ValidationError
import json


class SimpleJsonschemaException(Exception):

    def __init__(self, validation_error):
        self.validation_error = validation_error


class SimpleJsonschemaMiddleware(object):
    """
    {
        (('put', 'post'), foo:bar): {},
        ('post', abc:efg): {}
    }
    """

    def __init__(self):
        self.set_schemas(settings.SIMPLE_JSONSCHEMA)

    def set_schemas(self, simple_jsonschema):
        self.schemas = {}
        for key, schema in simple_jsonschema.items():
            methods, view_name = key
            if isinstance(methods, tuple):
                for method in methods:
                    schema_id = method.upper() + ':' + view_name
                    self.schemas[schema_id] = Draft4Validator(schema)
            elif isinstance(methods, str):
                schema_id = methods.upper() + ':' + view_name
                self.schemas[schema_id] = Draft4Validator(schema)

    def get_schema(self, request):
        view_name = request.resolver_match.view_name
        method = request.method
        key = method + ':' + view_name
        return self._schemas[key]

    def process_view(self, request, view_func, view_args, view_kwargs):
        schema = self.get_schema(request)
        json_data = json.dumps(request.body)
        try:
            schema.validate(json_data)
        except ValidationError as e:
            raise SimpleJsonschemaException(e)
        return None

    def process_exception(self, request, exception):
        if not isinstance(exception, SimpleJsonschemaException):
            return None
        return HttpResponse('{}', content_type='application/json')
