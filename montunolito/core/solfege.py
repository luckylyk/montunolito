"""
This module contains all the constants and music rules used during the
musical generation process: Chord, Scales, Fingerstates
And also some utils.
"""

NOTES = ('A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab')

SCALE_LENGTH = 12


SCALES = dict(
    major=[0, 2, 4, 5, 7, 9, 11],
    minor=[0, 2, 3, 5, 7, 8, 10])


CHORDS = dict(
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
    dim =   [0, 3, 6, 10, 12],
    sus4 =  [0, 5, 7, 12, 19],
    aug =   [0, 4, 8, 12, 19],
    qm =    [0, 4, 6, 12, 19])


# this dict contain index usefull for scales creation
# To generate a scale from chord, it use a major or minor as base scale.
# If some scale notes are modified by the chord, the method can use this
# dictionnary to know which note in the scale must be replaced by the chord.
# The sub-dictionnaries contain the array index for the note replacement.
# The key is the index in the scale array, and the value is the index in the
# chord array.
CHORD_SCALES_REMPLACEMENT_INDEXES = dict(
    m6 =    {5: 3}, 
    M7 =    {6: 3},
    m7M =   {6: 3},
    M7b9 =  {6: 3, 1: 4},
    m7b9 =  {1: 4},
    dim =   {4: 2},
    aug =   {4: 2},
    qm =    {4: 2})


CHORD_INDEXES_PRIORITY_ORDER = dict(
    M6 =    [3, 1, 2, 0, 4],
    m6 =    [3, 1, 2, 0, 4],
    M7 =    [1, 3, 0, 2, 4],
    m7 =    [1, 3, 0, 2, 4],
    M7M =   [3, 2, 1, 0, 4],
    m7M =   [3, 2, 1, 0, 4],
    M7b9 =  [1, 3, 2, 4, 0],
    m7b9 =  [1, 3, 2, 4, 0],
    M9 =    [1, 0, 4, 3, 2],
    m9 =    [1, 0, 4, 3, 2],
    M11 =   [1, 2, 3, 4, 0],
    m11 =   [1, 2, 3, 4, 0],
    dim =   [1, 2, 3, 4, 0],
    sus4 =  [1, 2, 3, 0, 4],
    aug =   [1, 2, 3, 4, 0],
    qm =    [1, 2, 3, 4, 0])


SCALENAME_BY_CHORDNAME = dict(
    major = ('Major', 'M6', 'M7', 'M7M', 'M7b9', 'M9', 'M11', 'Sus4', 'aug'),
    minor = ('Minor', 'm6', 'm7', 'm7M', 'm7b9', 'm9', 'm11', 'dim', 'qm'))


# this is a list of hand posing pattern for piano
# it represant thumd, index, middle, ring and pinkie
# 0 mean the finger is not pressing a key
# 1, it's pressing a key.
FINGERSSTATES = (
    (False, False, False, False, False), (True, False, False, False, True),
    (True, False, False, False, False), (False, True, False, False, False),
    (False, False, True, False, False), (False, False, False, True, False),
    (False, True, False, True, False), (True, True, True, True, True))



FINGERSSTATE_TYPES = {
    'mute': [0],
    'melodic': [1, 2, 3, 4, 5],
    'harmonic': [6, 7]}


MUTE_EIGHTH = [None, None, None, None, None]


def get_fingersstate_type(array):

    if array is None:
        return None

    conditions = (
        any([isinstance(v, int) and not isinstance(v, bool) for v in array]) or
        None in array)

    if conditions:
        array = [False if v is None else True for v in array]

    index = FINGERSSTATES.index(tuple(array))
    for fingersstate_type, indexes in FINGERSSTATE_TYPES.items():
        if index in indexes:
            return fingersstate_type
