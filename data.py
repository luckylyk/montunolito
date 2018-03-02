
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

comportments = dict(
    static = 1,
    melodic = 2,
    harpege = 3,
    chromatic = 4)

# this is a list of hand posing pattern for piano
# it represant thumd, index, middle, ring and pinkie
# 0 mean the finger is not pressing a key
# 1, it's pressing a key.
hand_poses = (
    (0, 0, 0, 0, 0), (1, 0, 0, 0, 1), (1, 0, 0, 0, 0), (0, 1, 0, 0, 0),
    (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 1, 1, 1, 0), (1, 1, 1, 1, 1))


hand_pose_types = {
    'mute': [0],
    'melodic': [1, 2, 3, 4, 5],
    'rythmic': [6, 7]}


def get_handpose_type(hand_pose):
    index = hand_poses.index(hand_pose)
    for hand_pose_type, indexes in hand_pose_types.items():
        if index in indexes:
            return hand_pose_type


# every pattern contains 5 keys: 1, 2, 3, 4, relationships
# keys 1, 2, 3, 4 contains differents alternative array of hand pattern index.
# the key number correspond the quarter of the pattern (1 = first quarter, etc)
# the 'relationship' key contains a dict. His keys represent the pattern index
# it contain the pattern index of the next quarter and a value (between 0 and 5)
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
        'comportments': {
            (1, 0): {'static': 3, 'melodic': 1, 'harpege': 5, 'chromatic': 0},
            (1, 1): {'static': 0, 'melodic': 0, 'harpege': 5, 'chromatic': 0},
            (1, 2): {'static': 0, 'melodic': 3, 'harpege': 5, 'chromatic': 0},
            (2, 0): {'static': 5, 'melodic': 3, 'harpege': 3, 'chromatic': 2},
            (2, 1): {'static': 0, 'melodic': 0, 'harpege': 5, 'chromatic': 0},
            (2, 2): {'static': 2, 'melodic': 3, 'harpege': 0, 'chromatic': 3},
            (3, 0): {'static': 5, 'melodic': 3, 'harpege': 3, 'chromatic': 2},
            (3, 1): {'static': 5, 'melodic': 0, 'harpege': 0, 'chromatic': 0},
            (3, 2): {'static': 0, 'melodic': 0, 'harpege': 5, 'chromatic': 0},
            (4, 0): {'static': 5, 'melodic': 0, 'harpege': 0, 'chromatic': 0},
            (4, 1): {'static': 0, 'melodic': 3, 'harpege': 1, 'chromatic': 3},
            (4, 2): {'static': 5, 'melodic': 3, 'harpege': 3, 'chromatic': 2},
            (4, 3): {'static': 3, 'melodic': 0, 'harpege': 3, 'chromatic': 1},
            (4, 4): {'static': 0, 'melodic': 3, 'harpege': 0, 'chromatic': 3}}
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
        'comportments': {
            (1, 0): {'static': 5, 'melodic': 0, 'harpege': 0, 'chromatic': 0},
            (2, 0): {'static': 5, 'melodic': 0, 'harpege': 0, 'chromatic': 0},
            (3, 0): {'static': 5, 'melodic': 0, 'harpege': 0, 'chromatic': 0},
            (4, 0): {'static': 5, 'melodic': 0, 'harpege': 0, 'chromatic': 0}
            }
        })


chord_grids = dict(
    example = [
        (1, 'Minor'), None, None, (4, 'Minor'),
        None, None, (5, 'M7'), None,
        None, None, None, (4, 'Minor'),
        None, None, (1, 'Minor'), None])


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


import random
import itertools


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


def pick_comportment(pattern, index):
    '''
    this method pick a random comportement in the pattern subdict 'comportment'
    using the indice of probabilty defined in the dict.
    '''
    comportment_prefs = pattern['comportments'][index]
    return random.choice([
        t for k, v in comportment_prefs.items()
        for t in tuple([k] * v) if v])


def chord_iterator(chord_grid):
    """
    this iterator cycle on a given chord grid.
    Chord grid len must be multiple of 16.
    Each chord grid element represent an eighth note. 
    """
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


def zip_chords_hand_poses(pattern_index, pattern, chords):
    """
    @pattern_index is a tuple containing the parttern index e.g. :(3, 2)
    @pattern is a pattern dict used for the generation
    @chords list of 4 chords to zip 
    method return a list e.g.
        ((4, 'Minor'), (0, 0, 0, 0, 0))
        ((4, 'Minor'), (0, 1, 1, 1, 0))
        ((1, 'Minor'), (0, 0, 0, 0, 0))
        ((1, 'Minor'), (1, 0, 0, 0, 1))
    representing 4 eighth notes.
    """
    hand_poses_retrived = []
    qpattern = pattern[pattern_index[0]][pattern_index[1]]
    for index in qpattern:
        hand_poses_retrived.append(hand_poses[index])
    return [(c, hp) for c, hp in zip(chords, hand_poses_retrived)]


def zipped_chords_hand_poses_and_comportment_iterator(
        pattern, chord_grid, mandatory_comportment=None):
    patterns_it = pattern_iterator(pattern)
    chords_it = chord_iterator(chord_grid)

    while True:
        index_pattern = next(patterns_it)
        chords = next(chords_it)
        prefered_comportment = (
            mandatory_comportment or pick_comportment(
                pattern, index_pattern))
        current_zipped_datas = zip_chords_hand_poses(
            index_pattern, pattern, chords)

        yield current_zipped_datas, prefered_comportment


gen = zipped_chords_hand_poses_and_comportment_iterator(
    rythmic_patterns['basic'], chord_grids['example'])