# -*- coding: utf-8 -*-
"""# TODO: docstring"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import traceback
from collections import Mapping

from .util import get_logger

LOG = get_logger()

LEFT_PINKY = 0
LEFT_RING = 1
LEFT_MIDDLE = 2
LEFT_INDEX = 3
LEFT_THUMB = 4

RIGHT_PINKY = 5
RIGHT_RING = 6
RIGHT_MIDDLE = 7
RIGHT_INDEX = 8
RIGHT_THUMB = 9

LEFT_HAND = [LEFT_PINKY, LEFT_RING, LEFT_MIDDLE, LEFT_INDEX, LEFT_THUMB]
RIGHT_HAND = [RIGHT_THUMB, RIGHT_INDEX, RIGHT_MIDDLE, RIGHT_RING, RIGHT_PINKY]

NUM_ROW = 0
TOP_ROW = 1
HOME_ROW = 2
BOTTOM_ROW = 3

def flatten(listOfLists):
    "Flatten one level of nesting"
    from itertools import chain
    return chain.from_iterable(listOfLists)

def mapping_dict(keys, value):
    return {key:value for key in keys}

class Layout(Mapping):
    """
    Class that defines a keyboard layout, can be called as a dictionary with
    a character and it'll return a tuple list of the form [(finger,row,hand,dx,dy,lfinger,rfinger)],
    if passed a string, it'll return the list for sequence of key presses
    """
    def __init__(self, unshifted_layer, shifted_layer):
        self._corresponding_row = {}
        self._corresponding_finger = {}
        self._relative_coordinates = {}

        # Add the "Enter" key to home row of left thumb, this is to reduce
        # noise on right pinky, this can be seen as just temporary, on my
        # keyboard, "Enter" key is on the right thumb
        del shifted_layer[2][-1][-1]
        del unshifted_layer[2][-1][-1]
        shifted_layer[-2][4].append('\n')
        unshifted_layer[-2][4].append('\n')

        row_num = BOTTOM_ROW + 1
        dy = -2
        for row in shifted_layer:
            lp, lr, lm, li, lt, rt, ri, rm, rr, rp = row
            self._corresponding_finger.update(mapping_dict(lp, LEFT_PINKY))
            self._corresponding_finger.update(mapping_dict(lr, LEFT_RING))
            self._corresponding_finger.update(mapping_dict(lm, LEFT_MIDDLE))
            self._corresponding_finger.update(mapping_dict(li, LEFT_INDEX))
            self._corresponding_finger.update(mapping_dict(lt, LEFT_THUMB))
            self._corresponding_finger.update(mapping_dict(rt, RIGHT_THUMB))
            self._corresponding_finger.update(mapping_dict(ri, RIGHT_INDEX))
            self._corresponding_finger.update(mapping_dict(rm, RIGHT_MIDDLE))
            self._corresponding_finger.update(mapping_dict(rr, RIGHT_RING))
            self._corresponding_finger.update(mapping_dict(rp, RIGHT_PINKY))

            self._corresponding_row.update(mapping_dict(lp, row_num))
            self._corresponding_row.update(mapping_dict(lr, row_num))
            self._corresponding_row.update(mapping_dict(lm, row_num))
            self._corresponding_row.update(mapping_dict(li, row_num))
            self._corresponding_row.update(mapping_dict(lt, row_num))
            self._corresponding_row.update(mapping_dict(rt, row_num))
            self._corresponding_row.update(mapping_dict(ri, row_num))
            self._corresponding_row.update(mapping_dict(rm, row_num))
            self._corresponding_row.update(mapping_dict(rr, row_num))
            self._corresponding_row.update(mapping_dict(rp, row_num))

            rlp = reversed(lp)
            rri = reversed(ri)
            for finger in [rlp, lr, lm, li, lt, rt, rri, rm, rr, rp]:
                dx = 0
                for char in finger:
                    self._relative_coordinates.update({char: (dx, dy)})
                    dx += 1

            row_num += 1
            dy += 1

        row_num = 0
        dy = -2
        for row in unshifted_layer:
            lp, lr, lm, li, lt, rt, ri, rm, rr, rp = row

            self._corresponding_finger.update(mapping_dict(lp, LEFT_PINKY))
            self._corresponding_finger.update(mapping_dict(lr, LEFT_RING))
            self._corresponding_finger.update(mapping_dict(lm, LEFT_MIDDLE))
            self._corresponding_finger.update(mapping_dict(li, LEFT_INDEX))
            self._corresponding_finger.update(mapping_dict(lt, LEFT_THUMB))
            self._corresponding_finger.update(mapping_dict(rt, RIGHT_THUMB))
            self._corresponding_finger.update(mapping_dict(ri, RIGHT_INDEX))
            self._corresponding_finger.update(mapping_dict(rm, RIGHT_MIDDLE))
            self._corresponding_finger.update(mapping_dict(rr, RIGHT_RING))
            self._corresponding_finger.update(mapping_dict(rp, RIGHT_PINKY))

            self._corresponding_row.update(mapping_dict(lp, row_num))
            self._corresponding_row.update(mapping_dict(lr, row_num))
            self._corresponding_row.update(mapping_dict(lm, row_num))
            self._corresponding_row.update(mapping_dict(li, row_num))
            self._corresponding_row.update(mapping_dict(lt, row_num))
            self._corresponding_row.update(mapping_dict(rt, row_num))
            self._corresponding_row.update(mapping_dict(ri, row_num))
            self._corresponding_row.update(mapping_dict(rm, row_num))
            self._corresponding_row.update(mapping_dict(rr, row_num))
            self._corresponding_row.update(mapping_dict(rp, row_num))

            rlp = reversed(lp)
            rri = reversed(ri)
            for finger in [rlp, lr, lm, li, lt, rt, rri, rm, rr, rp]:
                dx = 0
                for char in finger:
                    self._relative_coordinates.update({char: (dx, dy)})
                    dx += 1

            row_num += 1
            dy += 1


    def __getitem__(self, key):
        assignments = []
        if isinstance(key, basestring):
            for char in key:
                try:
                    finger = self._corresponding_finger[char]
                    row = self._corresponding_row[char]
                    dx, dy = self._relative_coordinates[char]
                    lfinger, rfinger = 0, 0
                    lpfinger, rpfinger = 0, 0
                    if finger in LEFT_HAND:
                        lfinger = finger
                        hand = 0
                        opposite_pinky = RIGHT_PINKY
                        rpfinger = finger
                    elif finger in RIGHT_HAND:
                        rfinger = finger
                        hand = 1
                        opposite_pinky = LEFT_PINKY
                        lpfinger = finger
                    if row > BOTTOM_ROW:
                        assignments.append(
                            (opposite_pinky, BOTTOM_ROW, hand, -1, 1, lpfinger, rpfinger)
                        )
                        row = row - BOTTOM_ROW - 1
                    assignments.append(
                        (finger, row, hand, dx, dy, lfinger, rfinger)
                    )
                except Exception, e:
                    LOG.error("Exception in announce: %s", traceback.format_exc())

        return assignments

    def __iter__(self):
        pass

    def __len__(self):
        return 0

QWERTY = Layout(
    #   L.Pinky      L.Rin  L.Mid  L.Index     L.Thu  R.Thu  R.Index     R.Mid  R.Rin  R.Pinky
    [
        [['`', '1'], ['2'], ['3'], ['4', '5'], [   ], [   ], ['6', '7'], ['8'], ['9'], ['0', '-', '='     ]],
        [['	', 'q'], ['w'], ['e'], ['r', 't'], [   ], [   ], ['y', 'u'], ['i'], ['o'], ['p', '[', ']', '\\']],
        [[     'a'], ['s'], ['d'], ['f', 'g'], [   ], [' '], ['h', 'j'], ['k'], ['l'], [';', "'", '\n']],
        [[     'z'], ['x'], ['c'], ['v', 'b'], [   ], [   ], ['n', 'm'], [','], ['.'], ['/']],
    ],
    [
        [['~', '!'], ['@'], ['#'], ['$', '%'], [   ], [   ], ['^', '&'], ['*'], ['('], [')', '_', '+'     ]],
        [['	', 'Q'], ['W'], ['E'], ['R', 'T'], [   ], [   ], ['Y', 'U'], ['I'], ['O'], ['P', '{', '}', '|']],
        [[     'A'], ['S'], ['D'], ['F', 'G'], [   ], [' '], ['H', 'J'], ['K'], ['L'], [':', '"', '\n']],
        [[     'Z'], ['X'], ['C'], ['V', 'B'], [   ], [   ], ['N', 'M'], ['<'], ['>'], ['?']],
    ]
)

SDVORAK = Layout(
    #   L.Pinky      L.Rin  L.Mid  L.Index     L.Thu  R.Thu  R.Index     R.Mid  R.Rin  R.Pinky
    [
        [['`', '1'], ['2'], ['3'], ['4', '5'], [   ], [   ], ['6', '7'], ['8'], ['9'], ['0', '[', ']'     ]],
        [['	', "'"], [','], ['.'], ['p', 'y'], [   ], [   ], ['f', 'g'], ['c'], ['r'], ['l', '/', '=', '\\']],
        [[     'a'], ['o'], ['e'], ['u', 'i'], [   ], [' '], ['d', 'h'], ['t'], ['n'], ['s', '-', '\n']],
        [[     ';'], ['q'], ['j'], ['k', 'x'], [   ], [   ], ['b', 'm'], ['w'], ['v'], ['z']],
    ],
    [
        [['~', '!'], ['@'], ['#'], ['$', '%'], [   ], [   ], ['^', '&'], ['*'], ['('], [')', '{', '}'     ]],
        [['	', '"'], ['<'], ['>'], ['P', 'Y'], [   ], [   ], ['F', 'G'], ['C'], ['R'], ['L', '?', '+', '|']],
        [[     'A'], ['O'], ['E'], ['U', 'I'], [   ], [' '], ['D', 'H'], ['T'], ['N'], ['S', '_', '\n']],
        [[     ':'], ['Q'], ['J'], ['K', 'X'], [   ], [   ], ['B', 'M'], ['W'], ['V'], ['Z']],
    ]
)

PDVORAK = Layout(
    #   L.Pinky      L.Rin  L.Mid  L.Index     L.Thu  R.Thu  R.Index     R.Mid  R.Rin  R.Pinky
    [
        [['$', '&'], ['['], ['{'], ['}', '('], [   ], [   ], ['=', '*'], [')'], ['+'], [']', '!', '#'     ]],
        [['	', ';'], [','], ['.'], ['p', 'y'], [   ], [   ], ['f', 'g'], ['c'], ['r'], ['l', '/', '^', '\\']],
        [[     'a'], ['o'], ['e'], ['u', 'i'], [   ], [' '], ['d', 'h'], ['t'], ['n'], ['s', '-', '\n']],
        [[     "'"], ['q'], ['j'], ['k', 'x'], [   ], [   ], ['b', 'm'], ['w'], ['v'], ['z']],
    ],
    [
        [['~', '%'], ['7'], ['5'], ['3', '1'], [   ], [   ], ['9', '0'], ['2'], ['4'], ['6', '8', '`'     ]],
        [['	', ':'], ['<'], ['>'], ['P', 'Y'], [   ], [   ], ['F', 'G'], ['C'], ['R'], ['L', '?', '@', '|']],
        [[     'A'], ['O'], ['E'], ['U', 'I'], [   ], [' '], ['D', 'H'], ['T'], ['N'], ['S', '_', '\n']],
        [[     '"'], ['Q'], ['J'], ['K', 'X'], [   ], [   ], ['B', 'M'], ['W'], ['V'], ['Z']],
    ]
)

DDVORAK = Layout(
    #   L.Pinky      L.Rin  L.Mid  L.Index     L.Thu  R.Thu  R.Index     R.Mid  R.Rin  R.Pinky
    [
        [['^', '['], ['{'], ['&'], ['(', '='], [   ], [   ], ['+', ')'], ['*'], ['}'], [']', '#', '!'     ]],
        [['	', ';'], [','], ['.'], ['p', 'y'], [   ], [   ], ['f', 'g'], ['c'], ['r'], ['l', '/', '\\', '$']],
        [[     'a'], ['o'], ['e'], ['u', 'i'], [   ], [' '], ['d', 'h'], ['t'], ['n'], ['s', '-', '\n']],
        [[     "'"], ['q'], ['j'], ['k', 'x'], [   ], [   ], ['b', 'm'], ['w'], ['v'], ['z']],
    ],
    [
        [['@', '1'], ['2'], ['3'], ['4', '5'], [   ], [   ], ['6', '7'], ['8'], ['9'], ['0', '`', '%'     ]],
        [['	', ':'], ['<'], ['>'], ['P', 'Y'], [   ], [   ], ['F', 'G'], ['C'], ['R'], ['L', '?', '|', '~']],
        [[     'A'], ['O'], ['E'], ['U', 'I'], [   ], [' '], ['D', 'H'], ['T'], ['N'], ['S', '_', '\n']],
        [[     '"'], ['Q'], ['J'], ['K', 'X'], [   ], [   ], ['B', 'M'], ['W'], ['V'], ['Z']],
    ]
)

COLEMAK = Layout(
    #   L.Pinky      L.Rin  L.Mid  L.Index     L.Thu  R.Thu  R.Index     R.Mid  R.Rin  R.Pinky
    [
        [['`', '1'], ['2'], ['3'], ['4', '5'], [   ], [   ], ['6', '7'], ['8'], ['9'], ['0', '-', '='     ]],
        [['	', 'q'], ['w'], ['f'], ['p', 'g'], [   ], [   ], ['j', 'l'], ['u'], ['y'], [';', '[', ']', '\\']],
        [[     'a'], ['r'], ['s'], ['t', 'd'], [   ], [' '], ['h', 'n'], ['e'], ['i'], ['o', "'", '\n']],
        [[     'z'], ['x'], ['c'], ['v', 'b'], [   ], [   ], ['k', 'm'], [','], ['.'], ['/']],
    ],
    [
        [['~', '!'], ['@'], ['#'], ['$', '%'], [   ], [   ], ['^', '&'], ['*'], ['('], [')', '_', '+'     ]],
        [['	', 'Q'], ['W'], ['F'], ['P', 'G'], [   ], [   ], ['J', 'L'], ['U'], ['Y'], [':', '{', '}', '|']],
        [[     'A'], ['R'], ['S'], ['T', 'D'], [   ], [' '], ['H', 'N'], ['E'], ['I'], ['O', '"', '\n']],
        [[     'Z'], ['X'], ['C'], ['V', 'B'], [   ], [   ], ['K', 'M'], ['<'], ['>'], ['?']],
    ]
)

WORKMAN = Layout(
    #   L.Pinky      L.Rin  L.Mid  L.Index     L.Thu  R.Thu  R.Index     R.Mid  R.Rin  R.Pinky
    [
        [['`', '1'], ['2'], ['3'], ['4', '5'], [   ], [   ], ['6', '7'], ['8'], ['9'], ['0', '-', '='     ]],
        [['	', 'q'], ['d'], ['r'], ['w', 'b'], [   ], [   ], ['j', 'f'], ['u'], ['p'], [';', '[', ']', '\\']],
        [[     'a'], ['s'], ['h'], ['t', 'g'], [   ], [' '], ['y', 'n'], ['e'], ['o'], ['i', "'", '\n']],
        [[     'z'], ['x'], ['m'], ['c', 'v'], [   ], [   ], ['k', 'l'], [','], ['.'], ['/']],
    ],
    [
        [['~', '!'], ['@'], ['#'], ['$', '%'], [   ], [   ], ['^', '&'], ['*'], ['('], [')', '_', '+'     ]],
        [['	', 'Q'], ['D'], ['R'], ['W', 'B'], [   ], [   ], ['J', 'F'], ['U'], ['P'], [':', '{', '}', '|']],
        [[     'A'], ['S'], ['H'], ['T', 'G'], [   ], [' '], ['Y', 'N'], ['E'], ['O'], ['I', '"', '\n']],
        [[     'Z'], ['X'], ['M'], ['C', 'V'], [   ], [   ], ['K', 'L'], ['<'], ['>'], ['?']],
    ]
)

PWORKMAN = Layout(
    #   L.Pinky      L.Rin  L.Mid  L.Index     L.Thu  R.Thu  R.Index     R.Mid  R.Rin  R.Pinky
    [
        [['`', '!'], ['@'], ['#'], ['$', '%'], [   ], [   ], ['^', '&'], ['*'], ['('], [')', '-', '='     ]],
        [['	', 'q'], ['d'], ['r'], ['w', 'b'], [   ], [   ], ['j', 'f'], ['u'], ['p'], [';', '[', ']', '\\']],
        [[     'a'], ['s'], ['h'], ['t', 'g'], [   ], [' '], ['y', 'n'], ['e'], ['o'], ['i', "'", '\n']],
        [[     'z'], ['x'], ['m'], ['c', 'v'], [   ], [   ], ['k', 'l'], [','], ['.'], ['/']],
    ],
    [
        [['~', '1'], ['2'], ['3'], ['4', '5'], [   ], [   ], ['6', '7'], ['8'], ['9'], ['0', '_', '+'     ]],
        [['	', 'Q'], ['D'], ['R'], ['W', 'B'], [   ], [   ], ['J', 'F'], ['U'], ['P'], [':', '{', '}', '|']],
        [[     'A'], ['S'], ['H'], ['T', 'G'], [   ], [' '], ['Y', 'N'], ['E'], ['O'], ['I', '"', '\n']],
        [[     'Z'], ['X'], ['M'], ['C', 'V'], [   ], [   ], ['K', 'L'], ['<'], ['>'], ['?']],
    ]
)

NORMAN = Layout(
    #   L.Pinky      L.Rin  L.Mid  L.Index     L.Thu  R.Thu  R.Index     R.Mid  R.Rin  R.Pinky
    [
        [['`', '1'], ['2'], ['3'], ['4', '5'], [   ], [   ], ['6', '7'], ['8'], ['9'], ['0', '-', '='     ]],
        [['	', 'q'], ['w'], ['d'], ['f', 'k'], [   ], [   ], ['j', 'u'], ['r'], ['l'], [';', '[', ']', '\\']],
        [[     'a'], ['s'], ['e'], ['t', 'g'], [   ], [' '], ['y', 'n'], ['i'], ['o'], ['h', "'", '\n']],
        [[     'z'], ['x'], ['c'], ['v', 'b'], [   ], [   ], ['p', 'm'], [','], ['.'], ['/']],
    ],
    [
        [['~', '!'], ['@'], ['#'], ['$', '%'], [   ], [   ], ['^', '&'], ['*'], ['('], [')', '_', '+'     ]],
        [['	', 'Q'], ['W'], ['D'], ['F', 'K'], [   ], [   ], ['J', 'U'], ['R'], ['L'], [':', '{', '}', '|']],
        [[     'A'], ['S'], ['E'], ['T', 'G'], [   ], [' '], ['Y', 'N'], ['I'], ['O'], ['H', '"', '\n']],
        [[     'Z'], ['X'], ['C'], ['V', 'B'], [   ], [   ], ['P', 'M'], ['<'], ['>'], ['?']],
    ]
)
