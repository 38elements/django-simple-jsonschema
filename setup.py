from setuptools import setup

setup(
    name='django-simple-jsonschema',
    version='0.0.3',
    author='38elements',
    description='django-simple-jsonschema is middleware for integrating django and jsonschema. ',
    license='MIT License',
    url='https://github.com/38elements/django-simple-jsonschema',
    install_requires=[
        'django>=1.8',
        'jsonschema>=2.5'
    ],
    py_modules=['django_simple_jsonschema'],
    keywords=['django', 'jsonschema'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers'
    ]
)
