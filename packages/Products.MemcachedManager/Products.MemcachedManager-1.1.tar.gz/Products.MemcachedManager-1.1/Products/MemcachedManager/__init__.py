# -*- coding: utf-8 -*-
"""
$Id$
"""

import logging
logger = logging.getLogger('MemcachedManager')


def initialize(context):
    try:
        from Products.MemcachedManager import MemcachedManager
    except ImportError:
        logger.error('Unable to import MemcachedManager. '
                     'You may need to install the memcache '
                     'client python library. See README.txt '
                     'for instructions.')
        return

    context.registerClass(
        MemcachedManager.MemcachedManager,
        constructors = (
        MemcachedManager.manage_addMemcachedManagerForm,
        MemcachedManager.manage_addMemcachedManager),
        icon='cache.gif'
        )
