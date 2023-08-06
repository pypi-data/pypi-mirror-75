"""
Pip.Services Container
----------------------

Pip.Services is an open-source library of basic microservices.
pip_services3_container provides IoC container implementation.

Links
`````

* `website <http://github.com/pip-services/pip-services>`_
* `development version <http://github.com/pip-services3-python/pip-services3-container-python>`

"""

from setuptools import setup
from setuptools import find_packages
 
setup(
    name='pip_services3_container',
    version='3.1.1',
    url='http://github.com/pip-services3-python/pip-services3-container-python',
    license='MIT',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    description='IoC container for Pip.Services in Python',
    long_description=__doc__,
    packages=find_packages(exclude=['config', 'data', 'examples', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'iso8601', 'PyYAML', 'pytest', 'pytz', 'pystache', 'pybars3', 'numpy', 'pip_services3_commons', 'pip_services3_components'
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