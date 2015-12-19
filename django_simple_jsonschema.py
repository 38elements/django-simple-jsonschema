from django.conf import settings


class SimpleJsonschemaMiddleware(object):

    def __init__(self):
        self.schema = settings.SIMPLE_JSONSCHEMA

    def process_request(self, request):
        pass

    def process_exception(self, request, exception):
        pass
