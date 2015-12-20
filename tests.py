from django.test import TestCase
from django_simple_jsonschema import SimpleJsonschemaMiddleware


class SimpleJsonschemaMiddlewareTestCase(TestCase):

    def test_foo(self):
        with self.settings(SIMPLE_JSONSCHEMA='123456789'):
            SimpleJsonschemaMiddleware()
