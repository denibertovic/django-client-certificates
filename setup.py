from distutils.core import setup

VERSION = '0.1dev'

setup(
    name='django-client-certificates',
    version=VERSION,
    author='Deni Bertovic',
    author_email='deni@kset.org',
    description='Django auth using client certificates',
    packages=['client_certs'],
    license='BSD',
    long_description=open('README.md').read(),
    install_requires='pyOpenSSL>=0.13',
)
