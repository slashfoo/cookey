from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import types
import sys as _sys
import logging as _logging

import os
import fnmatch

DEBUG = _logging.DEBUG
INFO = _logging.INFO
WARNING = WARN = _logging.WARNING
ERROR = _logging.ERROR
CRITICAL = CRIT = _logging.CRITICAL

_DEFAULT_FORMAT_STRING = ''.join([
    '%(levelname)-8s',
    ' - %(asctime)10s - ',
    '%(name)s:%(funcName)s - ',
    '%(message)s',
])
_DEFAULT_DATE_FORMAT_STRING = "%Y-%m-%d %H:%M:%S %Z"

_logging.basicConfig(
    level=DEBUG,
    format=_DEFAULT_FORMAT_STRING,
    datefmt=_DEFAULT_DATE_FORMAT_STRING,
)

_FORMATTER = _logging.Formatter(
    _DEFAULT_FORMAT_STRING,
    _DEFAULT_DATE_FORMAT_STRING
)

_LOGGER_CACHE = {}

def find_files(directory, patterns):
    """Walk a directory to find files/dirs recursively that match a glob."""
    for root, dirs, files in os.walk(directory):
        abs_root = os.path.abspath(root)
        for pattern in patterns:
            for a_dir in fnmatch.filter(dirs, pattern):
                yield os.path.join(abs_root, a_dir)
            for a_file in fnmatch.filter(files, pattern):
                yield os.path.join(abs_root, a_file)

def get_logger(logger_namespace=None):
    """
    Get a logger with default configuration applied to it.
    """
    if logger_namespace is None:
        import inspect
        caller_path = inspect.stack()[1][1]
        caller_name = inspect.getmodulename(caller_path)
        logger_namespace = caller_name

    if logger_namespace in _LOGGER_CACHE:
        logger = _LOGGER_CACHE[logger_namespace]
    else:
        logger = _logging.getLogger(logger_namespace)

        if logger_namespace != '':
            null_handler = _logging.NullHandler()
            logger.addHandler(null_handler)

        logger.crit = logger.critical

        _LOGGER_CACHE[logger_namespace] = logger

    return logger

