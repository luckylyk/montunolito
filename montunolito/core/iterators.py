
import random
import itertools

from .utils import choose
from .solfege import FINGERSSTATES
from .melody import convert_eighthmetas_to_eighthnotes
from .keyboard import convert_eighthnote_to_keyboard_eighth


def pattern_iterator(pattern):
    '''
    this iterator loop on a pattern. A parttern is a dict containing four
    key as int representing the the quater of the pattern. A complete parttern
    is during 2 mesures. To selected the pattern, it randomize picking an
    relationship indice between the indexes definied in the sub patter dict:
    'relationship'
    '''
    last_pindexes = (3, random.randint(1, len(pattern['figures'][-1])) - 1)
    while True:
        qpatterns = pattern['relationships'][last_pindexes]
        pindexes = choose(qpatterns)
        yield pindexes
        last_pindexes = pindexes



def chord_iterator(chord_grid):
    '''
    this iterator cycle on a given chord grid.
    Chord grid len must be multiple of 16.
    Each chord grid element represent an eighth note.
    '''
    assert len(chord_grid) % 16 == 0, 'chord grid len must be multiple of 16'
    assert chord_grid[0] is not None, 'the first chord grid element cannot be None'

    chords = itertools.cycle(chord_grid)
    beat_4 = None
    while True:
        beat_1 = next(chords) or beat_4
        beat_2 = next(chords) or beat_1
        beat_3 = next(chords) or beat_2
        beat_4 = next(chords) or beat_3
        yield beat_1, beat_2, beat_3, beat_4


def create_eighthmetas(
        pattern_index, pattern, chords, prefered_behavior):
    '''
    @pattern_index is a tuple containing the parttern index e.g. :(3, 2)
    @pattern is a pattern dict used for the generation
    @chords list of 4 chords to zip
    method return a list e.g.
    representing 4 eighth notes.
    '''
    fingersstates_retrieved = []
    qpattern = pattern['figures'][pattern_index[0]][pattern_index[1]]
    for index in qpattern:
        fingersstates_retrieved.append(FINGERSSTATES[index])
    return [
        {'chord': c, 'fingersstate': hp, 'behavior': prefered_behavior}
        for c, hp in zip(chords, fingersstates_retrieved)]


def eighthmetas_iterator(
        pattern, chord_grid, mandatory_behavior=None):
    '''
    this iterator iter synchronulsy on the chord grid and the rythmic pattern
    it generate the hand poses and return a zipped list of all eighth and the
    picked prefered behavior.
    '''
    patterns_it = pattern_iterator(pattern)
    chords_it = chord_iterator(chord_grid)

    while True:
        pattern_index = next(patterns_it)
        chords = next(chords_it)
        prefered_behavior = (
            mandatory_behavior or choose(pattern['behaviors'][pattern_index]))

        yield create_eighthmetas(
            pattern_index, pattern, chords, prefered_behavior)


def montuno_generator(pattern, chord_grid, tonality, forced_behavior=None):
    '''
    This iterator is the main iterator
    It create a stream of 64byte array representing a 62 keyboard keys states.
    The method receive a pattern a chord grid and a int between
    0 and 11 as tonality.
    '''

    eighthtmetas_it = eighthmetas_iterator(
        pattern, chord_grid, forced_behavior)

    previous_eighthnotes = [None, None, None, None]
    eighthmetas = next(eighthtmetas_it) + next(eighthtmetas_it)
    keyboard_sequence = []

    while True:
        eighthnotes = convert_eighthmetas_to_eighthnotes(
            previous_eighthnotes, eighthmetas,
            tonality)

        for i, eighthnote in enumerate(eighthnotes):
            keyboard_eighth = convert_eighthnote_to_keyboard_eighth(
                eighthnote=eighthnote, 
                keyboard_sequence=keyboard_sequence)
            keyboard_sequence.append(keyboard_eighth)
            ## print for debug
            # print(eighthmetas[i])
            # print(eighthnote)
            # print(keyboard_eighth)
            yield keyboard_eighth

        offset = -len(eighthnotes) + 1
        previous_eighthnotes = previous_eighthnotes[offset:-1] + eighthnotes
        eighthmetas = eighthmetas[len(eighthnotes):]

        if len(keyboard_sequence) > 8:
            keyboard_sequence = keyboard_sequence[-8:]

        while len(eighthmetas) < 8:
            eighthmetas += next(eighthtmetas_it)
