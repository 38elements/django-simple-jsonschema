# -*- coding: utf-8 -*-
from django.test import TestCase
from django_simple_jsonschema import SimpleJsonschemaMiddleware
from django_simple_jsonschema.management.commands.check_schema import Command
from collections import namedtuple
from jsonschema import Draft4Validator
from django.http import HttpResponse
from django.core.management import call_command
from django.utils.six import StringIO


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

json_str = '{"id": "あああ", "password": "bar"}'.encode('utf-8')
ResolverMatchMock = namedtuple('ResolverMatchMock', ['view_name'])


class HttpRequestMock():

    def __init__(self, method, resolver_match, body, encoding):
        self.method = method
        self.resolver_match = resolver_match
        self.body = body
        self.encoding = encoding
        self.path = '/foo/bar/'


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
                'POST', resolver_match, json_str, 'utf-8')
            schema = sj.get_schema(request).schema
            schema1 = s[('post', 'foo:bar:hoge')]
            self.assertEqual(schema, schema1)
            self.assertIsInstance(sj.get_schema(request), Draft4Validator)
            resolver_match = ResolverMatchMock('foo:bar')
            request = HttpRequestMock(
                'PUT', resolver_match, json_str, 'utf-8')
            schema = sj.get_schema(request).schema
            schema2 = s[('post', 'foo:bar:hoge')]
            self.assertEqual(schema, schema2)
            self.assertIsInstance(sj.get_schema(request), Draft4Validator)

    def test_process_view(self):
        with self.settings(SIMPLE_JSONSCHEMA=s):
            sj = SimpleJsonschemaMiddleware()
            resolver_match = ResolverMatchMock('foo:bar')
            request = HttpRequestMock(
                'POST', resolver_match, json_str, 'utf-8')
            result = sj.process_view(request, None, None, None)
            self.assertIsNone(result)
            resolver_match = ResolverMatchMock('foo:bar')
            request = HttpRequestMock(
                'POST', resolver_match, '{}'.encode('utf-8'), 'utf-8')
            result = sj.process_view(request, None, None, None)
            self.assertIsInstance(result, HttpResponse)

    def test_get_encoding(self):
        with self.settings(SIMPLE_JSONSCHEMA=s):
            sj = SimpleJsonschemaMiddleware()
            resolver_match = ResolverMatchMock('foo:bar')
            request = HttpRequestMock(
                'POST', resolver_match, json_str, 'cp932')
            encoding = sj.get_encoding(request)
            self.assertEqual(encoding, 'cp932')
            request.encoding = None
            encoding = sj.get_encoding(request)
            self.assertEqual(encoding, 'utf-8')


class CheckSchemaTestCase(TestCase):

    def test_success(self):
        out = StringIO()
        call_command('check_schema', stdout=out)
        self.assertIn('ERROR', out.getvalue())
        with self.settings(SIMPLE_JSONSCHEMA=s):
            out = StringIO()
            call_command('check_schema', stdout=out)
            self.assertIn('SUCCESS', out.getvalue())

    def test_jsonschema_exist(self):
        c = Command()
        self.assertFalse(c._jsonschema_exist)
        with self.settings(SIMPLE_JSONSCHEMA=s):
            c = Command()
            self.assertTrue(c._jsonschema_exist)

    def test_jsonschema_errors(self):
        with self.settings(SIMPLE_JSONSCHEMA=s):
            c = Command()
            self.assertEqual([], c._jsonschema_errors)
        e = {
            ('post', 'foo:bar:hoge'): {
                '$schema': 'http://json-schema.org/schema#',
                'type': 1,
                'properties': {
                    'id': {'type': 'string'},
                    'password': {'type': 'string'},
                    },
                'required': ['id']
            },
            (('post', 'put'), 'foo:bar'): {
                '$schema': 'http://json-schema.org/schema#',
                'type': 1,
                'properties': {
                    'id': {'type': 'string'},
                    'password': {'type': 'string'},
                    },
                'required': ['id']
            }
        }
        with self.settings(SIMPLE_JSONSCHEMA=e):
            self.assertEqual(2, len(c._jsonschema_errors))
