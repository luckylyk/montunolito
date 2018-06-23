import sys
import traceback
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), 'montunolito'))

from montunolito.core.iterators import *
from montunolito.core.melody import *
from montunolito.core.solfege import *
from montunolito.core.utils import *
from montunolito.core.keyboard import *


###############################################################################
################################# MELODY TESTS ################################
###############################################################################

def test_generate_scale():
    def names(notearray):
        return [NOTES[n] for n in notearray]

    # Major
    assert names(generate_notearray_scale({'degree': 0, 'name': 'Major'}, 3)) == ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    assert names(generate_notearray_scale({'degree': 0, 'name': 'M7'}, 3)) == ['C', 'D', 'E', 'F', 'G', 'A', 'Bb']
    assert names(generate_notearray_scale({'degree': 0, 'name': 'M7b9'}, 3)) == ['C', 'Db', 'E', 'F', 'G', 'A', 'Bb']
    assert names(generate_notearray_scale({'degree': 0, 'name': 'aug'}, 3)) == ['C', 'D', 'E', 'F', 'Ab', 'A', 'B']

    # Minor
    assert names(generate_notearray_scale({'degree': 0, 'name': 'Minor'}, 3)) == ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb']
    assert names(generate_notearray_scale({'degree': 0, 'name': 'm6'}, 3)) == ['C', 'D', 'Eb', 'F', 'G', 'A', 'Bb'] 
    assert names(generate_notearray_scale({'degree': 0, 'name': 'm7M'}, 3)) == ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'B'] 
    assert names(generate_notearray_scale({'degree': 0, 'name': 'm7b9'}, 3)) == ['C', 'Db', 'Eb', 'F', 'G', 'Ab', 'Bb']
    assert names(generate_notearray_scale({'degree': 0, 'name': 'dim'}, 3)) == ['C', 'D', 'Eb', 'F', 'Gb', 'Ab', 'Bb']
    assert names(generate_notearray_scale({'degree': 0, 'name': 'qm'}, 3)) == ['C', 'D', 'Eb', 'F', 'Gb', 'Ab', 'Bb']

    # same scale remaped
    assert names(generate_notearray_scale({'degree': 0, 'name': 'M7'}, 3)) == ['C', 'D', 'E', 'F', 'G', 'A', 'Bb']
    assert names(generate_notearray_scale({'degree': 0, 'name': 'M7'}, 4)) == ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'B']
    assert names(generate_notearray_scale({'degree': 0, 'name': 'M7'}, 5)) == ['D', 'E', 'Gb', 'G', 'A', 'B', 'C']
    assert names(generate_notearray_scale({'degree': 0, 'name': 'M7'}, 6)) == ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'Db']
    assert names(generate_notearray_scale({'degree': 0, 'name': 'M7'}, 7)) == ['E', 'Gb', 'Ab', 'A', 'B', 'Db', 'D']
    assert names(generate_notearray_scale({'degree': 0, 'name': 'M7'}, 8)) == ['F', 'G', 'A', 'Bb', 'C', 'D', 'Eb']

    # same scale remaped with chord degree
    assert names(generate_notearray_scale({'degree': 1, 'name': 'M7'}, 2)) == ['C', 'D', 'E', 'F', 'G', 'A', 'Bb']
    assert names(generate_notearray_scale({'degree': 1, 'name': 'M7'}, 3)) == ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'B']
    assert names(generate_notearray_scale({'degree': 1, 'name': 'M7'}, 4)) == ['D', 'E', 'Gb', 'G', 'A', 'B', 'C']
    assert names(generate_notearray_scale({'degree': 1, 'name': 'M7'}, 5)) == ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'Db']
    assert names(generate_notearray_scale({'degree': 1, 'name': 'M7'}, 6)) == ['E', 'Gb', 'Ab', 'A', 'B', 'Db', 'D']
    assert names(generate_notearray_scale({'degree': 1, 'name': 'M7'}, 7)) == ['F', 'G', 'A', 'Bb', 'C', 'D', 'Eb']


def test_generate_static_melody():
    reference_note = 4
    chord_array = [4, 7, 10, 0, 3]
    chord_array_destination = [4, 7, 10, 0, 3]
    assert generate_static_melody(reference_note, chord_array[:], chord_array_destination[:], 3) == [4, 4, 4]
    assert generate_static_melody(reference_note, chord_array[:], chord_array_destination[:], 4) == [4, 4, 4, 4]
    assert generate_static_melody(reference_note, chord_array[:], chord_array_destination[:], 7) == [4, 4, 4, 4, 4, 4, 4]

    reference_note = 4
    chord_array = [4, 7, 10, 0, 3]
    chord_array_destination = [5, 7, 10, 0, 3]
    assert generate_static_melody(reference_note, chord_array[:], chord_array_destination[:], 3) == [4, 4]
    assert generate_static_melody(reference_note, chord_array[:], chord_array_destination[:], 4) == [4, 4, 4]
    assert generate_static_melody(reference_note, chord_array[:], chord_array_destination[:], 7) == [4, 4, 4, 4, 4, 4]

    reference_note = 4
    chord_array = [2, 7, 10, 0, 3]
    chord_array_destination = [5, 7, 10, 0, 3]
    assert generate_static_melody(reference_note, chord_array[:], chord_array_destination[:], 3) == [2, 2]
    assert generate_static_melody(reference_note, chord_array[:], chord_array_destination[:], 4) == [2, 2, 2]
    assert generate_static_melody(reference_note, chord_array[:], chord_array_destination[:], 7) == [2, 2, 2, 2, 2, 2]


def test_generate_arpegic_melody():
    chord_array = [4, 7, 10, 0, 3]
    chord_array_destination = [5, 7, 10, 0, 3]
    assert generate_arpegic_melody(chord_array[:], chord_array_destination[:], 8) in ([4, 3, 0, 10, 7, 4, 3, 5], [4, 3, 0, 10, 7, 4, 3, 10], [4, 7, 10, 0, 3, 4, 7, 5], [4, 7, 10, 0, 3, 4, 7, 10])
    assert generate_arpegic_melody(chord_array[:], chord_array_destination[:], 8) in ([4, 3, 0, 10, 7, 4, 3, 5], [4, 3, 0, 10, 7, 4, 3, 10], [4, 7, 10, 0, 3, 4, 7, 5], [4, 7, 10, 0, 3, 4, 7, 10])
    assert generate_arpegic_melody(chord_array[:], chord_array_destination[:], 8) in ([4, 3, 0, 10, 7, 4, 3, 5], [4, 3, 0, 10, 7, 4, 3, 10], [4, 7, 10, 0, 3, 4, 7, 5], [4, 7, 10, 0, 3, 4, 7, 10])
    assert generate_arpegic_melody(chord_array[:], chord_array_destination[:], 8) in ([4, 3, 0, 10, 7, 4, 3, 5], [4, 3, 0, 10, 7, 4, 3, 10], [4, 7, 10, 0, 3, 4, 7, 5], [4, 7, 10, 0, 3, 4, 7, 10])


def test_generate_chromatic_melody():
    chord_array = [4, 7, 10, 0, 3]
    chord_array_destination = [6, 9, 1, 0, 3]

    melody = generate_chromatic_melody(
        reference_note=5, 
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        length=3)
    assert melody == [4, 5, 6]

    melody = generate_chromatic_melody(
        reference_note=5,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        length=4)
    assert melody == [4, 3, 2, 1]

    melody = generate_chromatic_melody(
        reference_note=7,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        length=4) 
    assert melody == [4, 3, 2, 1]

    melody = generate_chromatic_melody(
        reference_note=11,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        length=4)
    assert melody is None


def test_generate_diatonic_melody():
    reference_note = 4
    chord_array = [4, 7, 10, 0, 3]
    chord_array_destination = [6, 9, 1, 0, 3]
    scale = [4, 6, 7, 8, 10, 0, 3]
    melody_length = 3
    melody = generate_diatonic_melody(
        reference_note=reference_note,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        scale=scale[:],
        length=melody_length)
    assert melody == [4, 6, 7]

    reference_note = 10
    chord_array = [4, 7, 10, 0, 3]
    chord_array_destination = [6, 9, 1, 0, 3]
    scale = [4, 6, 7, 8, 10, 0, 3]
    melody_length = 3
    melody = generate_diatonic_melody(
        reference_note=reference_note,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        scale=scale[:],
        length=melody_length)
    assert melody == [10, 0, 3]

    reference_note = 10
    chord_array = [4, 7, 10, 0, 3]
    chord_array_destination = [6, 9, 1, 0, 3]
    scale = [4, 6, 7, 8, 10, 0, 3]
    melody_length = 5
    melody = generate_diatonic_melody(
        reference_note=reference_note,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        scale=scale[:],
        length=melody_length)
    assert melody == [10, 0, 3, 4, 6]

    reference_note = 8
    chord_array = [4, 7, 10, 0, 3]
    chord_array_destination = [6, 7, 1, 0, 3]
    scale = [4, 6, 7, 8, 10, 0, 3]
    melody_length = 8
    melody = generate_diatonic_melody(
        reference_note=reference_note,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        scale=scale[:],
        length=melody_length)
    assert melody == [7, 8, 10, 0, 3, 4, 6, 7]

    reference_note = 4
    chord_array = [4, 7, 10, 0, 3]
    chord_array_destination = [6, 7, 1, 0, 3]
    scale = [4, 6, 7, 8, 10, 0, 3]
    melody_length = 4
    melody = generate_diatonic_melody(
        reference_note=reference_note,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        scale=scale[:],
        length=melody_length)
    assert melody is None


def test_define_melody_lenghth():
    eighthmetas = [
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (0, 1, 0, 1, 0)},
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (0, 1, 0, 1, 0)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'arpegic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'chromatic', 'fingersstate': (0, 0, 0, 0, 0)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'chromatic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'M7', 'degree': 5}, 'behavior': 'chromatic', 'fingersstate': (0, 0, 0, 0, 0)},
        {'chord': {'name': 'M7', 'degree': 5}, 'behavior': 'chromatic', 'fingersstate': (1, 0, 0, 0, 1)}]
    assert define_melody_length(eighthmetas) == 4

    eighthmetas = [
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (0, 1, 0, 1, 0)},
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'chromatic', 'fingersstate': (0, 1, 0, 1, 0)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'chromatic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'chromatic', 'fingersstate': (0, 0, 0, 0, 0)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'chromatic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'M7', 'degree': 5}, 'behavior': 'chromatic', 'fingersstate': (0, 0, 0, 0, 0)},
        {'chord': {'name': 'M7', 'degree': 5}, 'behavior': 'chromatic', 'fingersstate': (1, 0, 0, 0, 1)}]
    assert define_melody_length(eighthmetas) == 3

    eighthmetas = [
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (0, 1, 0, 1, 0)},
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (0, 1, 0, 1, 0)},
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (0, 0, 0, 0, 0)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'chromatic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'M7', 'degree': 5}, 'behavior': 'chromatic', 'fingersstate': (0, 0, 0, 0, 0)},
        {'chord': {'name': 'M7', 'degree': 5}, 'behavior': 'chromatic', 'fingersstate': (1, 0, 0, 0, 1)}]
    assert define_melody_length(eighthmetas) == 6


def test_generate_melody_from_eighthmetas():
    reference_note = 4
    tonality = 3
    eighthmetas = [
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (0, 1, 0, 1, 0)},
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (0, 1, 0, 1, 0)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'arpegic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'chromatic', 'fingersstate': (0, 0, 0, 0, 0)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'chromatic', 'fingersstate': (1, 0, 0, 0, 1)}]
    # result = generate_melody_from_eighthmetas(reference_note, eighthmetas, tonality)
    # assert result in ([4, 7, 11, 7], [4, 11, 4, 7], [4, 7, 11, 2], [4, 11, 4, 2])

    reference_note = 4
    tonality = 3
    eighthmetas = [
        {'chord': {'name': 'Major', 'degree': 2}, 'behavior': 'diatonic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Major', 'degree': 2}, 'behavior': 'diatonic', 'fingersstate': (0, 1, 0, 1, 0)},
        {'chord': {'name': 'Major', 'degree': 2}, 'behavior': 'diatonic', 'fingersstate': (0, 1, 0, 1, 0)},
        {'chord': {'name': 'Major', 'degree': 2}, 'behavior': 'diatonic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'static', 'fingersstate': (1, 0, 0, 0, 1)}]
    result = generate_melody_from_eighthmetas(reference_note, eighthmetas, tonality)
    mustbe = [[5, None, None, None, 5], [None, 7, None, 7, None], [None, 9, None, 9, None], [10, None, None, None, 10], [0, None, None, None, 0]]
    assert result == mustbe # diatonic solution goes up

    reference_note = 4
    tonality = 3
    eighthmetas = [
        {'chord': {'name': 'Major', 'degree': 5}, 'behavior': 'diatonic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Major', 'degree': 5}, 'behavior': 'diatonic', 'fingersstate': (0, 1, 0, 1, 0)},
        {'chord': {'name': 'Major', 'degree': 5}, 'behavior': 'diatonic', 'fingersstate': (0, 1, 0, 1, 0)},
        {'chord': {'name': 'Major', 'degree': 5}, 'behavior': 'diatonic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'static', 'fingersstate': (1, 0, 0, 0, 1)}]
    result = generate_melody_from_eighthmetas(reference_note, eighthmetas, tonality)
    mustbe = [[3, None, None, None, 3], [None, 4, None, 4, None], [None, 5, None, 5, None], [6, None, None, None, 6], [7, None, None, None, 7]]
    assert result == mustbe # chomatic solution goes up

    reference_note = 0
    tonality = 8
    eighthmetas = [
        {'chord': {'name': 'Major', 'degree': 5}, 'behavior': 'static', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Major', 'degree': 5}, 'behavior': 'static', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Major', 'degree': 5}, 'behavior': 'static', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Major', 'degree': 5}, 'behavior': 'diatonic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'static', 'fingersstate': (1, 0, 0, 0, 1)}]
    result = generate_melody_from_eighthmetas(reference_note, eighthmetas, tonality)
    mustbe = [[1, None, None, None, 1], [1, None, None, None, 1], [1, None, None, None, 1], [1, None, None, None, 1]]
    assert result == mustbe  # static solution

    reference_note = None
    tonality = 8
    eighthmetas = [
        {'chord': {'name': 'Major', 'degree': 5}, 'behavior': 'static', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Major', 'degree': 5}, 'behavior': 'static', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Major', 'degree': 5}, 'behavior': 'static', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Major', 'degree': 5}, 'behavior': 'diatonic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'static', 'fingersstate': (1, 0, 0, 0, 1)}]
    result = generate_melody_from_eighthmetas(reference_note, eighthmetas, tonality)
    mustbe = [[1, None, None, None, 1], [1, None, None, None, 1], [1, None, None, None, 1], [1, None, None, None, 1]]
    assert result == mustbe  # static solution


###############################################################################
################################# MELODY KEYBOARD #############################
###############################################################################


def test_is_melodic_keysstate():
    keysstate = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0]
    assert is_melodic_keysstate(keysstate) is False

    keysstate = [
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
        1, 0, 0, 1]
    assert is_melodic_keysstate(keysstate) is False

    keysstate = [
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0]
    assert is_melodic_keysstate(keysstate) is True


def test_is_mute_keysstate():
    keysstate = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0]
    assert is_mute_keysstate(keysstate) is True

    keysstate = [
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
        1, 0, 0, 1]
    assert is_mute_keysstate(keysstate) is False

    keysstate = [
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0]
    assert is_mute_keysstate(keysstate) is False


def test_is_chord_keysstate():
    keysstate = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0]
    assert is_chord_keysstate(keysstate) is False

    keysstate = [
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
        1, 0, 0, 1]
    assert is_chord_keysstate(keysstate) is True

    keysstate = [
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0]
    assert is_chord_keysstate(keysstate) is False


def test_convert_keysstate_to_notearray():
    keysstate = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert convert_keysstate_to_notearray(keysstate) == []

    keysstate = [
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
        1, 0, 0, 1]
    assert convert_keysstate_to_notearray(keysstate) == [0, 6, 0, 4, 7, 0, 3]

    keysstate = [
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0]
    assert convert_keysstate_to_notearray(keysstate) == [0, 0, 0, 0, 0, 0]

###############################################################################
################################# UTILS TESTS #################################
###############################################################################


def test_choose():
    assert choose({True: 3, False: 1}) in (False, True)
    assert choose({True: 3, False: 1}) in (False, True)
    assert choose({True: 3, False: 1}) in (False, True)
    assert choose({True: 3, False: 1}) in (False, True)

    assert choose({"lionel": 0, "chloe": 2, "mani": 0, "nico": 5}) in ("chloe", "nico")
    assert choose({"lionel": 0, "chloe": 2, "mani": 0, "nico": 5}) in ("chloe", "nico")
    assert choose({"lionel": 0, "chloe": 2, "mani": 0, "nico": 5}) in ("chloe", "nico")
    assert choose({"lionel": 0, "chloe": 2, "mani": 0, "nico": 5}) in ("chloe", "nico")
    assert choose({"lionel": 0, "chloe": 2, "mani": 0, "nico": 5}) in ("chloe", "nico")

    assert choose({"lionel": 0, "chloe": 0, "mani": 5, "nico": 0}) is "mani"
    assert choose({"lionel": 0, "chloe": 0, "mani": 5, "nico": 0}) is "mani"
    assert choose({"lionel": 0, "chloe": 0, "mani": 5, "nico": 0}) is "mani"
    assert choose({"lionel": 0, "chloe": 0, "mani": 5, "nico": 0}) is "mani"

    raise_ = False
    try:
        choose({"lionel": 0, "chloe": 0, "mani": 0, "nico": 0})
    except IndexError:
        raise_ = True
    assert raise_ is True
    del raise_


def test_find_closer_number():
    assert find_closer_number(reference=8, array=(3, 6, 7, 8), clamp=12) == 8
    assert find_closer_number(reference=4, array=(3, 6, 7, 8), clamp=12) == 3
    assert find_closer_number(reference=14, array=(3, 6, 7, 8), clamp=12) == 3
    assert find_closer_number(reference=4, array=(3, 6, 7, 8), return_index=True) == 0


def test_count_occurence_continuity():
    assert count_occurence_continuity(['salut', 'salut', 'salut', 'prout', 'salut']) == 3
    assert count_occurence_continuity(['salut', 'prout', 'salut', 'salut', 'salut']) == 1
    assert count_occurence_continuity([5, 4, 3, 2, 1]) == 1
    assert count_occurence_continuity(['a', 'a', 'a', 'a', 'a', 'a']) == 6
    assert count_occurence_continuity(['salut', 'salut', 'salut', 'salut', 'prout']) == 4


def test_remap_number():
    assert remap_number(-1, value=12) == 11
    assert remap_number(10, value=12) == 10
    assert remap_number(14, value=12) == 2
    assert remap_number(0, value=12) == 0
    assert remap_number(62, value=12) == 2


def test_offset_array():
    assert offset_array([6, 5, 4, 3, 1], 1) == [5, 4, 3, 1, 6]
    assert offset_array([6, 5, 4, 3, 1], 2) == [4, 3, 1, 6, 5]


def test_replace_in_array():
    eighthnotes = [None, 5, None, 9, None], [7, None, None, None, 7], [9, None, None, None, 9]
    indexes = (2, 3, 5)
    eighthmetas = [
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (0, 1, 0, 1, 0)},
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (0, 1, 0, 1, 0)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'arpegic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'chromatic', 'fingersstate': (0, 0, 0, 0, 0)},
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'chromatic', 'fingersstate': (1, 0, 0, 0, 1)}]
    finalarray = replace_in_array(indexes, eighthnotes, eighthmetas)
    mustbe = [
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (1, 0, 0, 0, 1)},
        {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (0, 1, 0, 1, 0)},
        [None, 5, None, 9, None],
        [7, None, None, None, 7],
        {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'chromatic', 'fingersstate': (0, 0, 0, 0, 0)},
        [9, None, None, None, 9]]
    assert finalarray == mustbe


def test_iteration():
    CHORDGRIDS = dict(
        example = [
            {'degree': 1, 'name': 'Minor'},
            None,
            None,
            {'degree': 4, 'name': 'Minor'},
            None,
            None,
            {'degree': 5, 'name': 'M7'},
            None,
            None,
            None,
            None,
            {'degree': 4, 'name': 'Minor'},
            None,
            None, 
            {'degree': 1, 'name': 'Minor'},
            None])
    import time
    montunos = montuno_generator(
        pattern=PATTERNS['basic'],
        chord_grid=CHORDGRIDS['example'],
        tonality=5)
    print (montunos)

    for _ in range(125):
        time.sleep(.075)
        print(next(montunos))


if __name__ == '__main__':
    tests = [
        test_choose,
        test_find_closer_number,
        test_count_occurence_continuity,
        test_remap_number,
        test_offset_array,
        test_replace_in_array,
        test_generate_scale,
        test_generate_static_melody,
        test_generate_arpegic_melody,
        test_generate_chromatic_melody,
        test_generate_diatonic_melody,
        test_define_melody_lenghth,
        test_generate_melody_from_eighthmetas,
        test_is_melodic_keysstate,
        test_is_mute_keysstate,
        test_is_chord_keysstate,
        test_convert_keysstate_to_notearray
    ]

    test_failed = 0
    test_succesful = 0
    tracebacks = {}
    for test in tests:
        try:
            test()
            test_succesful += 1
        except:
            test_failed += 1
            tracebacks[test.__name__] = traceback.format_exc()

    print()
    print('{} / {} methods tested succesfully.'.format(
        test_succesful, test_failed + test_succesful))

    if tracebacks:
        print ("\nFailed test(s):")
        for m, tb in tracebacks.items():
            print(m + " :")
            print(tb)


    print (get_corresponding_keyboard_indexes(18))