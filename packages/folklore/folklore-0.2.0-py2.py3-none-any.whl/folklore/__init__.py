# -*- coding: utf-8 -*-

"""
folklore
~~~~~~~~

Folklore is an elegant thrift service development framework.
"""

from .service import ServiceHandler as Folklore, \
    ServiceModule as FolkloreModule, \
    FolkloreService, Context, thrift_module
from .hook import StopHook, define_hook
from .exc import CloseConnectionError, FolkloreException, TimeoutException


__all__ = ['Folklore', 'FolkloreModule', 'FolkloreService', 'StopHook',
           'define_hook', 'Context', 'CloseConnectionError',
           'FolkloreException', 'TimeoutException', 'thrift_module']
