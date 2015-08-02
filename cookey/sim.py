# -*- coding: utf-8 -*-
"""# TODO: docstring"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import traceback
from pprint import pprint

import logging
from collections import Counter, OrderedDict
import numpy as num

import cookey
from . import keyboard
from . import util
from .typist import Typist
from .util import get_logger

LOG = get_logger()

import click as cli

@cli.command()
@cli.option(
    '-v', '--verbose', count=True,
    help='Show more messages during the execution. Can be specified multiple times.'
)
@cli.version_option(cookey.__versionstr__, '-V', '--version')
@cli.help_option('-h', '--help')
def main(verbose):
    verbose = 3 if verbose > 3 else verbose
    level = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG][verbose]

    LOG.setLevel(level)
    chars = [0 for _ in range(256)]
    charcounter = Counter()
    typists = OrderedDict([
        (layout_name, Typist(layout)) for layout_name,layout in [
            ('QWERTY', keyboard.QWERTY),
            ('Simplified Dvorak', keyboard.SDVORAK),
            ('Programmers\' Dvorak', keyboard.PDVORAK),
            ('Drunken Dvorak', keyboard.DDVORAK),
            ('Colemak', keyboard.COLEMAK),
            ('Workman', keyboard.WORKMAN),
            ('Programmers\' Workman', keyboard.PWORKMAN),
            ('Norman', keyboard.NORMAN),
        ]
    ])

    for filename in util.find_files('.', ['*.c', '*.h', '*.py', '*.txt', '*.rst']):
        file = ""
        with open(filename, 'r+b') as f:
            while True:
                bb = f.read(8192*10)
                if not bb:
                    break
                file += bb.decode('ascii', errors='ignore')

        for typist in typists.values():
            typist.type(file)

        for char in file:
            try:
                chars[ord(char)] += 1
            except IndexError:
                print(char)

    charcounter += Counter({
        chr(char):chars[char] for char in range(256)
    })

    total_chars = sum(charcounter.values())
    print((total_chars, charcounter,))

    # curious_letters = [(str(letter), charcounter[letter]) for letter in '9}RrNnVv']
    # curious_count = sum([count for (_,count) in curious_letters])
    # print((curious_letters, curious_count, total_chars, round(curious_count / total_chars * 100, 3),))

    for layout_name,typist in typists.iteritems():
        print("{:20s}:\t {}".format(layout_name, typist.get_stats()))
