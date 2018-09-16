import math
import numpy as np
from random import randint
from montunolito.core.utils import remap_number


BIT_RATE = 65025 // 2
TIME = 13780 // 2
BASE = 10
PITCHES = [n for n in reversed([BASE * (2 ** (i / 12.0)) for i in range(88)])]


def get_sound_array(note, time=1):
    pitch = PITCHES[note] / 15
    array = []
    index = 0
    while len(array) <= TIME * time:
        array.append(math.sin(index / pitch) * BIT_RATE)
        index += 1
    return array[:TIME * time]


def mix_sound_arrays(*arrays):
    mixed = []
    diviser = len(arrays)
    for i in range(len(arrays[0])):
        values = [array[i] for array in arrays]
        mixed.append(sum(values) / diviser)
    return mixed


def silt(time=1):
    return [0] * TIME * time


def convert_sequence_to_int16(sequence):
    sound_array = []
    for notes in sequence:
        sound_arrays = []
        sound_arrays = [get_sound_array(note) for note in notes]
        if not sound_arrays:
            sound_array.extend(silt())
            continue
        sound_array.extend(mix_sound_arrays(*sound_arrays))

    return np.int16(sound_array)
