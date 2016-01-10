from django.core.management.base import BaseCommand
from django.utils import termcolors
from jsonschema import Draft4Validator
from jsonschema.exceptions import SchemaError
import json


class Command(BaseCommand):

    can_import_settings = True

    @property
    def _jsonschema_exist(self):
        from django.conf import settings
        if not hasattr(settings, 'SIMPLE_JSONSCHEMA'):
            return False
        return True

    @property
    def _jsonschema_errors(self):
        from django.conf import settings
        errors = []
        schemas = settings.SIMPLE_JSONSCHEMA
        for url, schema in schemas.items():
            try:
                Draft4Validator.check_schema(schema)
            except SchemaError as e:
                errors.append({
                    'url': url,
                    'error': e,
                    'schema': json.dumps(schema, indent=4, sort_keys=True)
                })
        return errors

    def handle(self, *args, **options):
        success = termcolors.make_style(fg='green')
        error = termcolors.make_style(fg='red')
        if not self._jsonschema_exist:
            not_exist = '[' + error('ERROR') + '] SIMPLE_JSONSCHEMA is not exist in settings.'
            self.stdout.write(not_exist)
            return
        errors = self._jsonschema_errors
        if len(errors):
            for e in errors:
                title = '\n[' + error('ERROR') + '] schema of ' + str(e['url']) + ' is invalid.'
                self.stdout.write(title)
                self.stdout.write('path: ' + str(list(e['error'].path)))
                self.stdout.write('message: ' + e['error'].message)
                self.stdout.write('schema:\n' + e['schema'] + '\n')
        else:
            self.stdout.write('[' + success('SUCCESS') + '] All jsonschemas are OK.')
