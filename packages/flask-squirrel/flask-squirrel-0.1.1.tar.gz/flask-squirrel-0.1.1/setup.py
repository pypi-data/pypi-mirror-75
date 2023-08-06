#!/usr/bin/env python

import re
import sys
from os import path
from setuptools import setup, find_packages

requirements = [
    'Flask>=1.1.0',
    'Flask-Cors>=3.0.0',
    'Flask-HTTPAuth>=3.3.0',
    'Flask-RESTful>=0.3.7',
    'Flask-SQLAlchemy>=2.4.0',
    'passlib'
]

version_file = path.join(
    path.dirname(__file__),
    'flask_squirrel',
    '__version__.py'
)
with open(version_file, 'r') as fp:
    m = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        fp.read(),
        re.M
    )
    version = m.groups(1)[0]

setup(
   name='flask-squirrel',
   version=version,
   license='MIT',
   description='Database REST API provider based on Flask/Flask-RESTful',
   url='https://github.com/ClNo/flask-squirrel',
   keywords='flask SQL REST datatables JSON',
   author='Claudio Nold',
   author_email='claudio.nold@gmx.net',
   packages=find_packages(exclude=['docs', 'tests']),
   classifiers=[
       'Development Status :: 3 - Alpha',
       'Environment :: Web Environment',
       'Intended Audience :: Developers',
       'Framework :: Flask',
       'Programming Language :: Python :: 3',
       'Programming Language :: Python :: 3.6',
       'Programming Language :: Python :: 3.7',
       'Programming Language :: Python :: 3.8',
       'License :: OSI Approved :: MIT License',
       'Operating System :: OS Independent',
       'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
       'Topic :: Software Development :: Libraries :: Python Modules'
   ],
   python_requires='>=3.6',
   zip_safe=False,
   include_package_data=True,
   platforms='any',
   test_suite='pytest',
   install_requires=requirements,
   tests_require=['pytest-flask'],
   # Install these with "pip install -e '.[docs]'
   extras_require={
       'docs': 'sphinx',
   }
)
