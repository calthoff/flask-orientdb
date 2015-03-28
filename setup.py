import sys
from setuptools import setup

install_requires = [
    "Flask",
    "pyorient"
]

if sys.version_info < (2, 6):
    install_requires.append('simplejson')

setup(
    name='Flask-OrientDB',
    version='0.1',
    url='http://github.com/calthoff/flask-orientdb',
    license='BSD',
    author='Cory Althoff',
    author_email='coryedwardalthoff@gmail.com',
    description='A Flask extension for using OrientDB with Flask',
    long_description=__doc__,
    #py_modules=['flask_mongokit'],
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    test_suite='tests.suite',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)