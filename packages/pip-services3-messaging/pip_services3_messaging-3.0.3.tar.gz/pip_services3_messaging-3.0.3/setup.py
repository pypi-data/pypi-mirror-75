"""
Pip.Services Net
----------------------

Pip.Services is an open-source library of basic microservices.
pip_services3_messaging provides messaging components.

Links
`````

* `website <http://github.com/pip-services-python/pip-services-python-messaging>`_
* `development version <http://github.com/pip-services3-python/pip-services3-messaging-python>`

"""

from setuptools import setup
from setuptools import find_packages
    
setup(
    name='pip_services3_messaging',
    version='3.0.3',
    url='http://github.com/pip-services3-python/pip-services3-messaging-python',
    license='MIT',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    description='Messaging components for Pip.Services in Python',
    long_description=__doc__,
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'iso8601', 'PyYAML', 'bottle', 'pip-services3-commons', 'pip-services3-components'
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
