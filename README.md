# Warning Status Developping
  
## django-simple-jsonschema
`django-simple-jsonschema` is middleware for integrating [django](https://github.com/django/django) and [jsonschema](https://github.com/Julian/jsonschema).   
If the request is invalid, such as the following response will be sent.   
```
{
    "errors": [
        {
            "message": "'id' is a required property", 
            "path": [], 
            "schema_path": [
                "required"
            ]
        }, 
        {
            "message": "1 is not of type 'string'", 
            "path": [
                "password"
            ], 
            "schema_path": [
                "properties", 
                "password", 
                "type"
            ]
        }
    ], 
    "url": "/foo/bar/"
}
```
  
## Requirements
* Python 3+
* Django 1.8+
* jsonschema 2.5+

## Installation
```
MIDDLEWARE_CLASSES = [
    # ...
    django_simple_jsonschema.SimpleJsonschemaMiddleware
]
```

## Configuration
You define the following variables in your project’s settings.

##### SIMPLE_JSONSCHEMA
`SIMPLE_JSONSCHEMA` is `dict`.     
`SIMPLE_JSONSCHEMA` has key which is `('<method>', '<view_name>')` or `(('<method1>', '<method2>'), '<view_name>'))`.  
`SIMPLE_JSONSCHEMA` has value  which is schema.   
###### Example 
```
SIMPLE_JSONSCHEMA = {
    ('post', 'namespace1:namespace2:name1'): {
        '$schema': 'http://json-schema.org/schema#',
        'type': 'object',
        'properties': {
            'login_id': {'type': 'string'},
            'password': {'type': 'string'},
        },
        'required': ['id']
    },
    (('post', 'put'), 'namespace3:name2'): {
        '$schema': 'http://json-schema.org/schema#',
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'message': {'type': 'string'},
        }
    }
}
```
