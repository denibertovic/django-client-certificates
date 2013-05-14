import os
import sys

from setuptools import setup

VERSION = '0.1'


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='django-client-certificates',
    version=VERSION,
    author='Deni Bertovic',
    author_email='deni@kset.org',
    description='Django auth using client certificates',
    url='github.com/denibertovic/django-client-certificates',
    packages=['client_certs'],
    license='BSD',
    install_requires=['pyOpenSSL>=0.13', 'django>=1.5'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
