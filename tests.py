from django.test import TestCase
from django_simple_jsonschema import SimpleJsonschemaMiddleware
from collections import namedtuple
from jsonschema import Draft4Validator


s1 = {
    ('post', 'foo:bar'): {
        '$schema': 'http://json-schema.org/schema#',
        'type': 'object',
        'properties': {
            'id': {'type': 'string'},
            'password': {'type': 'string'},
            },
        'required': ['id']
    }
}

s2 = {
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

HttpRequestMock = namedtuple('HttpRequestMock', ['method', 'resolver_match', 'body', 'json_data'])
ResolverMatchMock = namedtuple('ResolverMatchMock', ['view_name'])


class SimpleJsonschemaMiddlewareTestCase(TestCase):

    def test_init(self):
        with self.settings(SIMPLE_JSONSCHEMA=s1):
            sj = SimpleJsonschemaMiddleware()
            schema1 = s1[('post', 'foo:bar')]
            schema2 = sj._schemas['POST:foo:bar'].schema
            self.assertEqual(schema1, schema2)

        with self.settings(SIMPLE_JSONSCHEMA=s2):
            sj = SimpleJsonschemaMiddleware()
            schema1 = s2[(('post', 'put'), 'foo:bar')]
            schema2 = sj._schemas['POST:foo:bar'].schema
            self.assertEqual(schema1, schema2)
            schema3 = sj._schemas['PUT:foo:bar'].schema
            self.assertEqual(schema1, schema3)

    def test_get_schema(self):
        with self.settings(SIMPLE_JSONSCHEMA=s1):
            sj = SimpleJsonschemaMiddleware()
            resolver_match = ResolverMatchMock('foo:bar')
            request = HttpRequestMock(
                'POST', resolver_match, r'{id: "foo", "password": "bar"}', None)
            schema = sj.get_schema(request).schema
            schema1 = s1[('post', 'foo:bar')]
            self.assertEqual(schema, schema1)
            self.assertIsInstance(sj.get_schema(request), Draft4Validator)
