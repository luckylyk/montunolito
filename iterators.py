import sys
import os
import random
import itertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from montunolito.utils import choose
from montunolito.solfege import FINGERSSTATES
from montunolito.melody import convert_eighthmetas_to_eighthnotes
from montunolito.patterns import PATTERNS


def pattern_iterator(pattern):
    '''
    this iterator loop on a pattern. A parttern is a dict containing four
    key as int representing the the quater of the pattern. A complete parttern
    is during 2 mesures. To selected the pattern, it randomize picking an
    relationship indice between the indexes definied in the sub patter dict:
    'relationship'
    '''
    last_pindexes = (4, random.randint(1, len(pattern[4]) - 1))
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
    qpattern = pattern[pattern_index[0]][pattern_index[1]]
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

        yield create_eighthmetas (
            pattern_index, pattern, chords, prefered_behavior)


def montuno_generator(
        pattern, chord_grid, tonality, forced_behavior=None):
    '''
    This iterator is the main iterator
    It create a stream of 64byte array representing a 62 keyboard keys states.
    The method receive a pattern a chord grid and a int between 0 and 11 as tonality.
    TODO: the conversion to eighthnotes to eighth_kbstates
    '''

    eighthtmetas_it = eighthmetas_iterator(
        pattern, chord_grid, forced_behavior)

    previous_eighthnotes = [None, None, None, None]
    eighthmetas = next(eighthtmetas_it) + next(eighthtmetas_it)

    while True:
        eighthnotes = convert_eighthmetas_to_eighthnotes(
            previous_eighthnotes, eighthmetas,
            tonality)

        for eighthnote in eighthnotes:
            yield eighthnote

        previous_eighthnotes = previous_eighthnotes[-len(datas)+1:-1] + datas
        eighthmetas = eighthmetas[len(datas):]

        while len(to_process_datas) < 8:
            eighthmetas += next(eighthtmetas_it)


if __name__ == '__main__':
    CHORDGRIDS = [
        {'degree': 1, 'name': 'Minor'}, None, None, {'degree': 4, 'name': 'Minor'},
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
        None]

    def test():
        import time
        montunos = montuno_generator(
            pattern=PATTERNS['basic'],
            chord_grid=CHORDGRIDS,
            tonality=5)
        print (montunos)

        for _ in range(125):
            time.sleep(.075)
            print(next(montunos))

    test()
