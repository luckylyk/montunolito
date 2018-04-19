
##############################################################################
#  CORE / CONSTANTS
##############################################################################

notes = dict(
    A = 0,
    Bb = 1,
    B = 2,
    C = 3,
    Db = 4,
    D = 5,
    Eb = 6,
    E = 7,
    F = 8,
    Gb = 9,
    G = 10,
    Ab = 11)

scales = dict(
    major = [0, 2, 4, 5, 7, 9, 11],
    minor = [0, 2, 3, 5, 7, 8, 10])

chords = dict(
    Major = [0, 4, 7, 12, 19],
    Minor = [0, 3, 7, 12, 19],
    M6 =    [0, 4, 7, 9, 12],
    m6 =    [0, 3, 7, 9, 12],
    M7 =    [0, 4, 7, 10, 12],
    m7 =    [0, 3, 7, 10, 12],
    M7M =   [0, 4, 7, 11, 12],
    m7M =   [0, 3, 7, 11, 12],
    M7b9 =  [0, 4, 7, 10, 13],
    m7b9 =  [0, 3, 7, 10, 13],
    M9 =    [0, 4, 7, 10, 14],
    m9 =    [0, 3, 7, 10, 14],
    M11 =   [0, 4, 10, 14, 17],
    m11 =   [0, 3, 10, 14, 17],
    dim =   [0, 3, 6, 9, 12],
    sus4 =  [0, 5, 7, 12, 19],
    aug =   [0, 4, 8, 12, 19],
    qm =    [0, 4, 6, 12, 19])

pitches = [0, 1, 2, 3, 4, 5]

progression_type = dict(
    static = 1,
    diatonic = 2,
    harpege = 3,
    chromatic = 4)

# this is a list of hand posing pattern for piano
# it represant thumd, index, middle, ring and pinkie
# 0 mean the finger is not pressing a key
# 1, it's pressing a key.
handposes = (
    (0, 0, 0, 0, 0), (1, 0, 0, 0, 1), (1, 0, 0, 0, 0), (0, 1, 0, 0, 0),
    (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 1, 1, 1, 0), (1, 1, 1, 1, 1))


handpose_types = {
    'mute': [0],
    'melodic': [1, 2, 3, 4, 5],
    'chord': [6, 7]}


##############################################################################
#  DATA (must be moved in json files)
##############################################################################


# every pattern contains 5 keys: 1, 2, 3, 4, relationships
# keys 1, 2, 3, 4 contains differents alternative array of hand pattern index.
# the key number correspond the quarter of the pattern (1 = first quarter, etc)
# the 'relationship' key contains a dict. His keys represent the pattern index
# it contain the pattern index of the next quarter and a value
# (between 0 and 5)
# it's for generate random patterns.
# this is data and will be moved in JSON files. Every pattern will be save as
# different json file.
rythmic_patterns = dict(
    basic = {
        1: ((1, 0, 6, 1), (1, 3, 5, 1), (2, 3, 5, 1)),
        2: ((0, 6, 0, 1), (0, 3, 5, 1), (0, 1, 0, 1)),
        3: ((0, 6, 0, 1), (0, 6, 0, 6), (0, 3, 5, 1)),
        4: ((0, 6, 1, 1), (0, 2, 3, 4), (0, 6, 0, 1), (0, 6, 1, 0), (1, 0, 1, 0)),
        'relationships': {
            (1, 0): {(2, 0): 5, (2, 1): 0, (2, 2): 3},
            (1, 1): {(2, 0): 2, (2, 1): 5, (2, 2): 3},
            (1, 2): {(2, 0): 2, (2, 1): 5, (2, 2): 3},
            (2, 0): {(3, 0): 5, (3, 1): 1, (3, 2): 1},
            (2, 1): {(3, 0): 2, (3, 1): 3, (3, 2): 4},
            (2, 2): {(3, 0): 2, (3, 1): 3, (3, 2): 4},
            (3, 0): {(4, 0): 3, (4, 1): 1, (4, 2): 2, (4, 3): 2, (4, 4): 3},
            (3, 1): {(4, 0): 0, (4, 1): 3, (4, 2): 0, (4, 3): 2, (4, 4): 5},
            (3, 2): {(4, 0): 2, (4, 1): 0, (4, 2): 2, (4, 3): 0, (4, 4): 4},
            (4, 0): {(1, 0): 3, (1, 1): 3, (1, 2): 0}, 
            (4, 1): {(1, 0): 2, (1, 1): 0, (1, 2): 5},
            (4, 2): {(1, 0): 4, (1, 1): 2, (1, 2): 0},
            (4, 3): {(1, 0): 4, (1, 1): 0, (1, 2): 0},
            (4, 4): {(1, 0): 2, (1, 1): 4, (1, 2): 0}},
        'progressions': {
            (1, 0): {'static': 3, 'diatonic': 1, 'harpege': 5, 'chromatic': 0},
            (1, 1): {'static': 0, 'diatonic': 0, 'harpege': 5, 'chromatic': 0},
            (1, 2): {'static': 0, 'diatonic': 3, 'harpege': 5, 'chromatic': 0},
            (2, 0): {'static': 5, 'diatonic': 3, 'harpege': 3, 'chromatic': 2},
            (2, 1): {'static': 0, 'diatonic': 0, 'harpege': 5, 'chromatic': 0},
            (2, 2): {'static': 2, 'diatonic': 3, 'harpege': 0, 'chromatic': 3},
            (3, 0): {'static': 5, 'diatonic': 3, 'harpege': 3, 'chromatic': 2},
            (3, 1): {'static': 5, 'diatonic': 0, 'harpege': 0, 'chromatic': 0},
            (3, 2): {'static': 0, 'diatonic': 0, 'harpege': 5, 'chromatic': 0},
            (4, 0): {'static': 5, 'diatonic': 0, 'harpege': 0, 'chromatic': 0},
            (4, 1): {'static': 0, 'diatonic': 3, 'harpege': 1, 'chromatic': 3},
            (4, 2): {'static': 5, 'diatonic': 3, 'harpege': 3, 'chromatic': 2},
            (4, 3): {'static': 3, 'diatonic': 0, 'harpege': 3, 'chromatic': 1},
            (4, 4): {'static': 0, 'diatonic': 3, 'harpege': 0, 'chromatic': 3}}
            },

    chacha = {
        1: ((6, 1, 0, 1)),
        2: ((6, 1, 0, 1)),
        3: ((6, 1, 0, 1)),
        4: ((6, 1, 0, 1)),
        'relationships': {
            (1, 0): {(2, 0): 5},
            (2, 0): {(3, 0): 5},
            (3, 0): {(4, 0): 5},
            (4, 0): {(1, 0): 5}},
        'progressions': {
            (1, 0): {'static': 5, 'diatonic': 0, 'harpege': 0, 'chromatic': 0},
            (2, 0): {'static': 5, 'diatonic': 0, 'harpege': 0, 'chromatic': 0},
            (3, 0): {'static': 5, 'diatonic': 0, 'harpege': 0, 'chromatic': 0},
            (4, 0): {'static': 5, 'diatonic': 0, 'harpege': 0, 'chromatic': 0}
            }
        })


chord_grids = dict(
    example = [
        (1, 'Minor'), None, None, (4, 'Minor'),
        None, None, (5, 'M7'), None,
        None, None, None, (4, 'Minor'),
        None, None, (1, 'Minor'), None])


##############################################################################
#  GENERATORS / ITERATOR / CONVERTOR
##############################################################################


import random
import itertools


def get_handpose_type(handpose):
    index = handposes.index(handpose)
    for handpose_type, indexes in handpose_types.items():
        if index in indexes:
            return handpose_type


def reverse_chord(chord, degree):
    ''' this method offset a chord list '''
    return chord[degree:] + chord[:5-degree]


def remap_note(index):
    ''' this method remap note to force value to be between 0 - 11 '''
    while index > 11:
        index -= 11
    return index


def remap_note_array(note, array):
    ''' this method is usefull to repitch a scale '''
    return [remap_note(index + note) for index in array]


def pattern_iterator(pattern):
    '''
    this iterator loop on a pattern. A parttern is a dict containing four
    key as int representing the the quater of the pattern. A complete parttern
    is during 2 mesures. To selected the pattern, it randomize picking an
    relationship indice between the indexes definied in the sub patter dict:
    'relationship'
    '''
    last_index = (4, random.randint(1, len(pattern[4]) - 1))
    while True:
        qpatterns = pattern['relationships'][last_index]
        index = random.choice(
            [t for k, v in qpatterns.items() for t in tuple([k] * v) if v])
        yield index
        last_index = index


def pick_pattern_prefered_progression_type(pattern, index):
    '''
    this method pick a random comportement in the pattern subdict 'progression'
    using the indice of probabilty defined in the dict.
    '''
    progression_prefs = pattern['progressions'][index]
    return random.choice([
        t for k, v in progression_prefs.items()
        for t in tuple([k] * v) if v])


def pick_progression_type(
        reference_note, prefered_progression_type, previous_zipped_datas,
        zipped_datas, next_zipped_datas):

    zipped = previous_zipped_datas[2:] + zipped_datas + next_zipped_datas[:2]
    indexes_and_chords = [
        (i, chord) for i, (chord, handpose) in enumerate(zipped)
        if get_handpose_type(handpose) == 'melodic']
    indexes = [i for (i, c) in indexes_and_chords]
    chords = [c for (i, c) in indexes_and_chords]

    # if there's no chord evolution return static
    if len(set(chords)) == 1 and len(chords) > 1:
        return ['static'] * 4

    if not 0 in indexes or 1 in indexes:
        reference_note = None

    for index, (i, c) in enumerate(indexes_and_chords):
        if i in [0, 1, 6, 7]:
            continue
        if not index or index >= (len(indexes_and_chords) - 1):
            continue

        """TODO"""

    return [prefered_progression_type] * 4


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


def zip_chords_handposes(pattern_index, pattern, chords):
    '''
    @pattern_index is a tuple containing the parttern index e.g. :(3, 2)
    @pattern is a pattern dict used for the generation
    @chords list of 4 chords to zip
    method return a list e.g.
        ((4, 'Minor'), (0, 0, 0, 0, 0))
        ((4, 'Minor'), (0, 1, 1, 1, 0))
        ((1, 'Minor'), (0, 0, 0, 0, 0))
        ((1, 'Minor'), (1, 0, 0, 0, 1))
    representing 4 eighth notes.
    '''
    handposes_retrived = []
    qpattern = pattern[pattern_index[0]][pattern_index[1]]
    for index in qpattern:
        handposes_retrived.append(handposes[index])
    return [(c, hp) for c, hp in zip(chords, handposes_retrived)]


def zipped_chords_handposes_and_progression_iterator(
        pattern, chord_grid, mandatory_progression_type=None):
    '''
    this iterator iter synchronulsy on the chord grid and the rythmic pattern
    it generate the hand poses and return a zipped list of all eighth and the 
    picked prefered progression e.g.
        (
          [
            ((5, 'M7'), (0, 0, 0, 0, 0)),
            ((5, 'M7'), (0, 1, 1, 1, 0)),
            ((5, 'M7'), (0, 0, 0, 0, 0)),
            ((4, 'Minor'), (1, 0, 0, 0, 1))
          ],
          'chromatic'
        )
    '''
    patterns_it = pattern_iterator(pattern)
    chords_it = chord_iterator(chord_grid)

    while True:
        index_pattern = next(patterns_it)
        chords = next(chords_it)
        prefered_progression_type = (
            mandatory_progression_type or
            pick_pattern_prefered_progression_type(pattern, index_pattern))
        current_zipped_datas = zip_chords_handposes(
            index_pattern, pattern, chords)

        yield current_zipped_datas, prefered_progression_type


def convert_handposes_booleans_to_handposes_notes(
        processed_datas, to_process_datas, tonality, progression_type):
    """ TODO """

    return [None, None, None]


def montuno_generator(  # Find better name
        pattern, chord_grid, tonality, mode, mandatory_progression_type=None):

    data_it = zipped_chords_handposes_and_progression_iterator(
        pattern, chord_grid, mandatory_progression_type)

    processed_datas = [None, None, None, None]
    to_process_datas = next(data_it)

    while True:
        datas = convert_handposes_booleans_to_handposes_notes(
            processed_datas, to_process_datas,
            tonality, mandatory_progression_type)

        for data in datas:
            yield data

        processed_datas = processed_datas[-len(datas)+1:-1] + datas
        to_process_datas = to_process_datas[len(datas):]

        if len(to_process_datas) < 4:
            to_process_datas += next(data_it)


gen = zipped_chords_handposes_and_progression_iterator(
    rythmic_patterns['basic'], chord_grids['example'])


for elt in next(gen):
    print(elt)
