from django.test import TestCase
from django_simple_jsonschema import SimpleJsonschemaMiddleware


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


class SimpleJsonschemaMiddlewareTestCase(TestCase):

    def test_init(self):
        with self.settings(SIMPLE_JSONSCHEMA=s1):
            sj = SimpleJsonschemaMiddleware()
            self.assertEqual(sj.ces, 'utf8')
            schema1 = s1[('post', 'foo:bar')]
            schema2 = sj.schemas['POST:foo:bar'].schema
            self.assertEqual(schema1, schema2)
            with self.settings(SIMPLE_JSONSCHEMA_ENCODING='euc-jp'):
                sj = SimpleJsonschemaMiddleware()
                self.assertEqual(sj.ces, 'euc-jp')

        with self.settings(SIMPLE_JSONSCHEMA=s2):
            sj = SimpleJsonschemaMiddleware()
            self.assertEqual(sj.ces, 'utf8')
            schema1 = s2[(('post', 'put'), 'foo:bar')]
            schema2 = sj.schemas['POST:foo:bar'].schema
            self.assertEqual(schema1, schema2)
            schema3 = sj.schemas['PUT:foo:bar'].schema
            self.assertEqual(schema1, schema3)
