Introduction
============

.. image:: http://img.shields.io/pypi/v/Products.MemcachedManager.svg
    :target: https://pypi.python.org/pypi/Products.MemcachedManager

.. image:: https://img.shields.io/travis/collective/Products.MemcachedManager/master.svg
    :target: http://travis-ci.org/collective/Products.MemcachedManager

.. image:: https://img.shields.io/coveralls/collective/Products.MemcachedManager/master.svg
    :target: https://coveralls.io/r/collective/Products.MemcachedManager

MemcachedManager is a cache similar to RAMCacheManager, using `memcached <https://memcached.org/>`_ for storage.

Dependencies
============

`memcached`_

    This needs to be set up on a server Zope can connect to.
    You provide the IP address in the MemcachedManager settings screen.


`pylibmc <https://pypi.python.org/pypi/pylibmc>`_

or...

`python-memcached <https://pypi.python.org/pypi/python-memcached>`_

Credits
=======

Thanks to Mike Solomon <mas63@cornell.edu> for key validation
