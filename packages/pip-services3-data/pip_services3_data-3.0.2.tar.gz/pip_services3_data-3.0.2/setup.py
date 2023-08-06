"""
Pip.Services Data
------------------

Pip.Services is an open-source library of basic microservices.
pip_services3_data provides data processing and persistence components.

Links
`````

* `website <http://github.com/pip-services/pip-services>`_
* `development version <http://github.com/pip-services3-python/pip-services3-data-python>`

"""

from setuptools import setup
from setuptools import find_packages
import json

with open('component.json') as json_file:
    config = json.load(json_file)

setup(
    name='pip_services3_data',
    version=config['version'],
    url='http://github.com/pip-services3-python/pip-services3-data-python',
    license='MIT',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    description='Data processing and persistence components for Pip.Services in Python',
    long_description=__doc__,
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'iso8601', 'PyYAML', 'pip_services3_commons', 'pip_services3_components'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]    
)
