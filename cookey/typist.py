# -*- coding: utf-8 -*-
"""# TODO: docstring"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from .keyboard import flatten
from .util import get_logger

LOG = get_logger()

import numpy as num

class Typist(object):
    def __init__(self, layout):
        self._layout = layout
        self._keypresses = 0
        self._finger_counter = [0 for _ in range(10)]
        self._row_counter = [0 for _ in range(4)]
        self._hand_counter = [0,0]
        self._finger_travel_x_vectors = [[] for _ in range(10)]
        self._finger_travel_y_vectors = [[] for _ in range(10)]
        self._hand_vector = []
        self._same_finger_vector = [[],[]]

    def type(self, words):
        keypresses = self._layout[words]
        self._keypresses += len(keypresses)
        for keypress in keypresses:
            finger,row,hand,dx,dy,lfinger,rfinger = keypress
            self._finger_counter[finger] += 1
            self._row_counter[row] += 1
            self._hand_counter[hand] += 1
            self._hand_vector.append(hand)
            self._same_finger_vector[hand].append(finger)
            self._finger_travel_x_vectors[finger].append(dx)
            self._finger_travel_y_vectors[finger].append(dy)

    def get_stats(self):
        finger_travel = [0 for _ in range(10)]
        finger_percents = [0.0 for _ in range(10)]
        row_percents = [0.0 for _ in range(4)]

        for finger in range(10):
            finger_percents[finger] = round(self._finger_counter[finger]/sum(self._finger_counter)*100,3)
            finger_travel[finger] = num.sum(
                num.sqrt(
                    num.square(num.diff(self._finger_travel_x_vectors[finger])) +
                    num.square(num.diff(self._finger_travel_y_vectors[finger]))
                )
            )

        for row in range(4):
            row_percents[row] = round(self._row_counter[row] / self._keypresses * 100, 3)

        hand_percents = [
            round(count / self._keypresses * 100, 3)
            for count in self._hand_counter
        ]

        hand_vector = num.array(self._hand_vector)
        hand_pedalling = (
            num.count_nonzero(
                hand_vector - num.roll(hand_vector, -1)
            )
        )

        hand_pedalling /= self._keypresses
        hand_pedalling *= 100

        hand_pedalling = round(hand_pedalling, 3)

        same_finger = []
        lsfv = num.array(self._same_finger_vector[0])
        rsfv = num.array(self._same_finger_vector[1])

        same_finger = [
            num.count_nonzero(
                hand_same_finger_vector - num.roll(hand_same_finger_vector, -1)
            )
            for hand_same_finger_vector in [lsfv,rsfv]
        ]

        same_finger[0] /= self._hand_counter[0]
        same_finger[1] /= self._hand_counter[1]
        same_finger[0] *= hand_percents[0]
        same_finger[1] *= hand_percents[1]
        same_finger = [round(k,3) for k in same_finger]
        same_finger = sum(same_finger)

        return (self._keypresses, [finger_percents[finger] for finger in [0,1,2,3,4,9,8,7,6,5]], row_percents, hand_percents, [int(ft) for ft in finger_travel], hand_pedalling, same_finger,)
