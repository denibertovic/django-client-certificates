from distutils.core import setup

import os
import sys

VERSION = '0.1dev'


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
    install_requires=['pyOpenSSL>=0.13', 'django>=1.4'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
