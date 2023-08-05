# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.1'
description = 'Memcached cache manager for Zope.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CHANGES.rst').read()
)


setup(name='Products.MemcachedManager',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Zope2',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Zope Public License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='memcached Zope cache cachemanager',
      author='Sidnei da Silva',
      author_email='plone-developers@lists.sourceforge.net',
      url='https://github.com/collective/Products.MemcachedManager',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      extras_require={
          'pylibmc': 'pylibmc',
          'python-memcached': 'python-memcached',
      },
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
