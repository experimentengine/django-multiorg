import os

from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    setup_requires=['setuptools-markdown'],
    name='django-multiorg',
    version='0.1',
    packages=['multiorg',],
    include_package_data=True,
    license='BSD License',
    description='Allow users to view a Django application as a member of different organizations.',
    long_description=README,
    url='http://github.com/experimentengine/django-multiorg/',
    author='Jeremy Boyd',
    author_email='jeremy.boyd@experimentengine.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
