# -*- coding: utf-8 -*-

"""
folklore.exc
~~~~~~~~~~~~

Folklore related Exceptin definitions.
"""


class FolkloreException(Exception):
    """Base class for all Folklore exceptions
    """


class CloseConnectionError(FolkloreException):
    """Exception for closing client connection
    """


class TimeoutException(FolkloreException):
    """Raised when api call timeout
    """
    def __init__(self, timeout):
        self.timeout = timeout

    def __str__(self):
        return 'Timeout after {} seconds'.format(self.timeout)

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, str(self))
