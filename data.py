
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
        (1, 'Minor'), None, (4, 'Minor'), None,
        (5, 'M7') , None, (4, 'Minor'), None])


def reverse_chord(chord, degree):
    ''' this method offset a chord list '''
    return chord[degree:] + chord[:5-degree]


def remap_note(index):
    ''' this method remap note to force value to be between 0 - 11 '''
    while index > 11:
        index -= 11
    return index


def remap_note_array(note, array):
    return [remap_note(index + note) for index in array]


import random
import itertools


def pattern_iterator(pattern):
    last_index = (4, random.randint(1, len(pattern[4])))
    while True:
        qpatterns = pattern['relationships'][last_index]
        index = random.choice(
            [t for k, v in qpatterns.items() for t in tuple([k] * v) if v])
        yield index
        last_index = index


def pick_comportment(pattern, index):
    comportment_prefs = pattern['comportments'][index]
    return random.choice([
        t for k, v in comportment_prefs.items()
        for t in tuple([k] * v) if v])


def chord_iterator(chord_grid):
    assert len(chord_grid) % 8 == 0, 'chord grid len must be multiple of 8'
    chords = itertools.cycle(chord_grid)
    beat_1 = next(chords)
    beat_2 = next(chords) or beat_1
    while True:
        yield beat_1, beat_2
        beat_1 = next(chords) or beat_2
        beat_2 = next(chords) or beat_1


def notes_hand_pose_generator(
        pattern, tonality, mode, chord_grid, mandatory_comportment=None):
    patterns = pattern_iterator(pattern)
    chords = chord_iterator(chord_grid)

    last_index_pattern = None
    last_prefered_comportment = None
    last_chords = None

    current_index_pattern = next(patterns)
    current_prefered_comportment = pick_comportment(pattern, current_index_pattern)
    current_chords = next(chords)

    next_index_pattern = next(patterns)
    next_prefered_comportment = pick_comportment(pattern, next_index_pattern)
    next_chords = next(chords)

    last_reference_note = None

    while True:
        last_index_pattern = current_index_pattern
        last_prefered_comportment = current_prefered_comportment
        last_chords = current_chords

        current_index_pattern = next_index_pattern
        current_prefered_comportment = next_prefered_comportment
        current_chords = next_chords

        next_index_pattern = next(patterns)
        next_prefered_comportment = pick_comportment(pattern, next_index_pattern)
        next_chords = next(chords)

        print (current_index_pattern)
        yield "\n".join([
        # hps = [
            str([hand_poses[i], get_handpose_type(hand_poses[i]), next_prefered_comportment, current_chords])
            for i in 
                pattern[current_index_pattern[0]][current_index_pattern[1]]])
        # print (hps)

    # iteration done, do the note selection algorythm


gen = notes_hand_pose_generator(rythmic_patterns['basic'], None, None, chord_grids['example'])