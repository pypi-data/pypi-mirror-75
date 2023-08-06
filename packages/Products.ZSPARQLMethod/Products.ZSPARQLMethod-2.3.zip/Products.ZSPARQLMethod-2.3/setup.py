from setuptools import setup, find_packages
from os.path import join
import sys
import os

NAME = 'Products.ZSPARQLMethod'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(join(*PATH)).read().strip()

install_requires = ['sparql-client', 'eventlet', 'six']
if sys.version_info < (2, 6):
    install_requires += ['simplejson']

TEST_REQUIRES = ['mock', 'cssselect', 'webob']
if sys.version_info[0] == 2:
    TEST_REQUIRES += ['mechanize==0.2.5', 'wsgi_intercept==0.4']
else:
    TEST_REQUIRES += ['mechanize==0.4.5', 'wsgi_intercept==1.9.2']

docs = open('README.rst').read() + "\n" + \
       open(os.path.join("docs", "HISTORY.txt")).read()

setup(
    name=NAME,
    version=VERSION,
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.2",
        "Framework :: Zope",
        "Framework :: Zope :: 2",
        "Framework :: Zope :: 4",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    keywords='EEA Add-ons Plone Zope',
    author='European Environment Agency: IDM2 A-Team',
    author_email="eea-edw-a-team-alerts@googlegroups.com",
    url='https://github.com/eea/Products.ZSPARQLMethod',
    license='GPL',
    description="Zope product for making SPARQL queries, simiar to ZSQLMethod",
    long_description_content_type='text/x-rst',
    long_description=docs,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={"test": TEST_REQUIRES},
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
