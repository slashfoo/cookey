#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup.py file for the project."""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import sys
import io
import re
import fnmatch

import setuptools
import os.path

CURDIR = os.path.abspath(os.path.dirname(__file__))
PROJNAME = 'cookey'

SCRIPTS = []

ENTRY_POINTS = {}
ENTRY_POINTS['console_scripts'] = {
    'cookeysim = cookey.sim:main',
}

CLASSIFIERS = [
    'Programming Language :: Python',
    'Natural Language :: English',
    # 'Development Status :: 2 - Pre-Alpha',
    'Development Status :: 3 - Alpha',
    # 'Development Status :: 4 - Beta',
    # 'Development Status :: 5 - Production/Stable',
    # 'Development Status :: 6 - Mature',
    # 'Development Status :: 7 - Inactive',
    'Environment :: Console',
    'License :: Other/Proprietary License',  # TODO: MIT LICENSE
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    # 'Programming Language :: Python :: 3',
    # 'Programming Language :: Python :: 3.4',
]

PKG_NAME = PROJNAME
PACKAGE_DATA = {
    str(PKG_NAME): ['tests/*']
}

def do_nothing(*_args, **_kwargs):
    """The name says it all, do nothing."""
    pass

def read_files(*filenames, **kwargs):
    """Read multiple files and returns their contents in a single string."""
    # adapted from Jeff Knupp's article on open sourcing a project [1]
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for file_path in filenames:
        with io.open(file_path, encoding=encoding) as a_file:
            buf.append(a_file.read())
    return sep.join(buf)

def read_requirements(req_filename):
    """
    Read the requirements file in a format that pip accepts.

    This means that it skips lines that start with # and empty lines.
    """
    requires = []
    url_egg_re = re.compile(r'^(.*?)#egg=(.*?)$')

    with io.open(req_filename) as req_file:
        for line in req_file.readlines():
            if line == '':
                continue
            if line.startswith('#'):
                continue

            if '://' not in line:
                requires.append(line.strip())
            else:
                egg = url_egg_re.search(line).groups()[-1]
                requires.append(egg)

    return requires


class DisabledCommand(setuptools.Command):  # pylint: disable=too-few-public-methods

    """Class to disable a `python setup.py command_here`."""

    description = 'This command has been disabled.'
    user_options = []

    initialize_options = do_nothing
    finalize_options = do_nothing

    def run(self):
        """Announce and error-out."""
        print(self.description)
        sys.exit(1)

def read_metadata(main_pkg, root_directory=None, filename='__init__.py'):
    """
    Read metadata in the main package's __init__.py or other specified file.

    The data is expected to be in the format::

        __key__ = 'value'
    """
    dunder_re = re.compile(r"^__(.*?)__ = '([^']*)'")

    if not root_directory:
        root_directory = os.path.abspath(os.path.dirname(os.path.curdir))

    filepath = os.path.join(root_directory, main_pkg, filename)

    metadata = {}
    with io.open(filepath) as module_file:
        for line in module_file.readlines():
            if dunder_re.match(line):
                key, val = dunder_re.search(line).groups()
                metadata[key] = val
    return metadata

def find_files(directory, patterns):
    """Walk a directory to find files/dirs recursively that match a glob."""
    for root, dirs, files in os.walk(directory):
        for pattern in patterns:
            for a_dir in fnmatch.filter(dirs, pattern):
                yield os.path.join(root, a_dir)
            for a_file in fnmatch.filter(files, pattern):
                yield os.path.join(root, a_file)

class FuncCommand(setuptools.Command):  # pylint: disable=too-few-public-methods
    """Run a specific function on 'run' and nothing else, no preparing or finalizing options."""

    initialize_options = do_nothing
    finalize_options = do_nothing
    user_options = []

    def run(self):  # pylint: disable=missing-docstring
        self.function(self.args)  # pylint: disable=no-member

    def __init__(self, *args, **kwargs):
        setuptools.Command.__init__(self, *args, **kwargs)

def clean_directory(directory, patterns=None):
    """Clean up all generated files from other commands."""
    if not patterns:
        patterns = [
            'dist',
            'build',
            '.tox',
            '*.egg-info',
            '*.egg',
            'wheelhouse',
            '__pycache__',
            '*.pyc',
            '*.pyo',
            'htmlcov',
            '.coverage',
            '_build',
            '.eggs',
            '_api',
        ]

    description = clean_directory.__doc__

    def clobber(self, _arguments):  # pylint: disable=no-self-use
        """Delete all the unwanted files and print a pretty message."""

        for obj_to_delete in find_files(self.directory, self.patterns):
            print('Removing {}...'.format(obj_to_delete), end=' ')
            os.system('rm -rf {}'.format(obj_to_delete))
            print('DONE')

    return type(
        str('ClobberCommand'),
        (FuncCommand, object,),
        {
            'description': description,
            'args': [],
            'function': clobber,
            'patterns': patterns,
            'directory': directory,
        }
    )

def setup_package(projname, directory):
    """Setup the package using setuptools"""
    metadata = read_metadata(projname, directory)

    packages = setuptools.find_packages(
        where=os.path.join(directory),
    )

    setuptools.setup(
        # Package information
        name=PKG_NAME,
        version=metadata['versionstr'],
        description=metadata['shortdoc'],
        long_description=read_files(os.path.join(directory, 'README.rst')),
        url=metadata['url'],
        license=metadata['license'],
        author=metadata['author'],
        author_email=metadata['email'],

        # Package Properties
        namespace_packages=[],
        packages=packages,
        entry_points=ENTRY_POINTS,
        scripts=SCRIPTS,
        package_data=PACKAGE_DATA,

        # Requirements
        setup_requires=[],
        install_requires=read_requirements(
            os.path.join(directory, 'requirements.txt')
        ),
        extras_require={},
        tests_require=[],

        # Other Stuff
        cmdclass={
            'clobber': clean_directory(directory),
            'register': DisabledCommand,
            'upload': DisabledCommand,
            'upload_docs': DisabledCommand,
        },
        command_options={
        },
        platforms=['any'],
        classifiers=CLASSIFIERS,
        zip_safe=False,
    )

if __name__ == '__main__':
    setup_package(PROJNAME, CURDIR)
