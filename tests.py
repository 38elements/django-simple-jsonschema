from __future__ import unicode_literals
from django.test import TestCase
from django_simple_jsonschema import SimpleJsonschemaMiddleware
from collections import namedtuple
from jsonschema import Draft4Validator


s = {
    ('post', 'foo:bar:hoge'): {
        '$schema': 'http://json-schema.org/schema#',
        'type': 'object',
        'properties': {
            'id': {'type': 'string'},
            'password': {'type': 'string'},
            },
        'required': ['id']
    },
    (('post', 'put'), 'foo:bar'): {
        '$schema': 'http://json-schema.org/schema#',
        'type': 'object',
        'properties': {
            'id': {'type': 'string'},
            'password': {'type': 'string'},
            },
        'required': ['id']
    }
}

json_str = r'{"id": "foo", "password": "bar"}'
ResolverMatchMock = namedtuple('ResolverMatchMock', ['view_name'])


class HttpRequestMock():

    def __init__(self, method, resolver_match, body, encoding):
        self.method = method
        self.resolver_match = resolver_match
        self.body = body
        self.encoding = encoding


class SimpleJsonschemaMiddlewareTestCase(TestCase):

    def test_init(self):
        with self.settings(SIMPLE_JSONSCHEMA=s):
            sj = SimpleJsonschemaMiddleware()
            schema1 = s[('post', 'foo:bar:hoge')]
            schema2 = sj._schemas['POST:foo:bar'].schema
            self.assertEqual(schema1, schema2)
            schema1 = s[(('post', 'put'), 'foo:bar')]
            schema2 = sj._schemas['POST:foo:bar'].schema
            self.assertEqual(schema1, schema2)
            schema3 = sj._schemas['PUT:foo:bar'].schema
            self.assertEqual(schema1, schema3)

    def test_get_schema(self):
        with self.settings(SIMPLE_JSONSCHEMA=s):
            sj = SimpleJsonschemaMiddleware()
            resolver_match = ResolverMatchMock('foo:bar:hoge')
            request = HttpRequestMock(
                'POST', resolver_match, json_str, 'utf8')
            schema = sj.get_schema(request).schema
            schema1 = s[('post', 'foo:bar:hoge')]
            self.assertEqual(schema, schema1)
            self.assertIsInstance(sj.get_schema(request), Draft4Validator)
            resolver_match = ResolverMatchMock('foo:bar')
            request = HttpRequestMock(
                'PUT', resolver_match, json_str, 'utf8')
            schema = sj.get_schema(request).schema
            schema2 = s[('post', 'foo:bar:hoge')]
            self.assertEqual(schema, schema2)
            self.assertIsInstance(sj.get_schema(request), Draft4Validator)

    def test_process_view(self):
        with self.settings(SIMPLE_JSONSCHEMA=s):
            sj = SimpleJsonschemaMiddleware()
            resolver_match = ResolverMatchMock('foo:bar')
            request = HttpRequestMock(
                'POST', resolver_match, json_str, 'utf8')
            result = sj.process_view(request, None, None, None)
            self.assertIsNone(result)

    def test_process_exception(self):
        pass
