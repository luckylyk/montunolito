
##############################################################################
#  CORE / CONSTANTS
##############################################################################

NOTES = ('A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab')


SCALES = dict(
    major = [0, 2, 4, 5, 7, 9, 11],
    minor = [0, 2, 3, 5, 7, 8, 10])


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


PITCHES = [0, 1, 2, 3, 4, 5]


# this is a list of hand posing pattern for piano
# it represant thumd, index, middle, ring and pinkie
# 0 mean the finger is not pressing a key
# 1, it's pressing a key.
FINGERSSTATES = (
    (0, 0, 0, 0, 0), (1, 0, 0, 0, 1), (1, 0, 0, 0, 0), (0, 1, 0, 0, 0),
    (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 1, 0, 1, 0), (1, 1, 1, 1, 1))


FINGERSSTATE_TYPES = {
    'mute': [0],
    'melodic': [1, 2, 3, 4, 5],
    'chord': [6, 7]}


MUTE_EIGHTH = [None, None, None, None, None]

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
PATTERNS = dict(
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
        'behaviors': {
            (1, 0): {'static': 3, 'diatonic': 1, 'arpegic': 5, 'chromatic': 0},
            (1, 1): {'static': 0, 'diatonic': 0, 'arpegic': 5, 'chromatic': 0},
            (1, 2): {'static': 0, 'diatonic': 3, 'arpegic': 5, 'chromatic': 0},
            (2, 0): {'static': 5, 'diatonic': 3, 'arpegic': 3, 'chromatic': 2},
            (2, 1): {'static': 0, 'diatonic': 0, 'arpegic': 5, 'chromatic': 0},
            (2, 2): {'static': 2, 'diatonic': 3, 'arpegic': 0, 'chromatic': 3},
            (3, 0): {'static': 5, 'diatonic': 3, 'arpegic': 3, 'chromatic': 2},
            (3, 1): {'static': 5, 'diatonic': 0, 'arpegic': 0, 'chromatic': 0},
            (3, 2): {'static': 0, 'diatonic': 0, 'arpegic': 5, 'chromatic': 0},
            (4, 0): {'static': 5, 'diatonic': 0, 'arpegic': 0, 'chromatic': 0},
            (4, 1): {'static': 0, 'diatonic': 3, 'arpegic': 1, 'chromatic': 3},
            (4, 2): {'static': 5, 'diatonic': 3, 'arpegic': 3, 'chromatic': 2},
            (4, 3): {'static': 3, 'diatonic': 0, 'arpegic': 3, 'chromatic': 1},
            (4, 4): {'static': 0, 'diatonic': 3, 'arpegic': 0, 'chromatic': 3}}
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
        'behaviors': {
            (1, 0): {'static': 5, 'diatonic': 0, 'arpegic': 0, 'chromatic': 0},
            (2, 0): {'static': 5, 'diatonic': 0, 'arpegic': 0, 'chromatic': 0},
            (3, 0): {'static': 5, 'diatonic': 0, 'arpegic': 0, 'chromatic': 0},
            (4, 0): {'static': 5, 'diatonic': 0, 'arpegic': 0, 'chromatic': 0}
            }
        })


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

##############################################################################
#  MATH UTILS
##############################################################################

def remap_array(array, offset=0, value=10):
    ''' this method remap an array int between 0 and value '''
    return [remap_number(number + offset, value=value) for number in array]


def find_closer_number(reference, array, clamp=11, return_index=False):
    reference = remap_number(reference, clamp)
    array = remap_array(array=array, value=clamp)
    if reference in array:
        return array.index(reference) if return_index else reference

    closer_difference = None
    for i, number in enumerate(array):
        difference = min(
            abs(reference - number), abs(reference + clamp - number))
        if not closer_difference or closer_difference > difference:
            closer_index = i
            closer_difference = difference
    return closer_index if return_index else array[closer_index]


def count_occurence_continuity(array):
    '''
    utils who count the occurence in a list before a difference
    example :
        ['salut', 'salut', 'salut', 'prout', 'salut'] = 3
        ['salut', 'prout', 'salut', 'salut', 'salut'] = 1
    '''
    result = 0
    for element in array:
        if element != array[0]:
            break
        result += 1
    return result


def remap_number(number, value=10):
    ''' this method remap an int between 0 and value '''
    while number > value - 1:
        number -= value
    while number < 0:
        number += value
    return number


def offset_array(array, offset):
    ''' this method offset a list '''
    return array[offset:] + array[:offset - len(array)]


def choose(items):
    '''
    this method is an utils to choose an element with a coefficient.
    :items: is a dict {'item1': coefficien as int}
    return a random key with a chance coefficient as value
    '''
    return random.choice([
        t for k, v in items.items()
        for t in tuple([k] * v) if v])


def replace_in_array(indexes, items, array):
    '''
    place the give items in the given array at the given indexes.
    '''
    if indexes[-1] > len(array) or len(indexes) != len(items):
        raise IndexError

    array = array[:]
    for index, item in zip(indexes, items):
        array[index] = item
    return array


##############################################################################
#  MELODY
##############################################################################
"""
nomenclature : 
    chord = {'degree': 0, 'name': 'Minor'}
    tonality = int (factor to offset all values)
    fingersstate = (0, 1, 0, 1, 0)
        list representing fingers in action on keyboard:
            0 = released,
            1 = pressed
    eighthnote = [None, 2, 6, 8, None]
        list representing note played by pressed fingers. None is
        for released fingers
    behavior = list of constant for algorythme, represention the melodic behavior
    eighthmeta = 
        {
            'chord': {'degree': 5, 'name': M7'},
            'fingersstate': (0, 0, 0, 0, 0),
            'behavior': 'chromatic'
        }
        dict of meta data representing eighth note, used by the generator
        to be transformed in final_eighth
"""

import random
import itertools


def get_fingersstate_type(fingersstate):
    if fingersstate is None:
        return None
    fingersstate = tuple([0 if v is None else v for v in fingersstate])
    fingersstate = tuple([1 if value > 0 else 0 for value in fingersstate])
    index = FINGERSSTATES.index(fingersstate)
    for fingersstate_type, indexes in FINGERSSTATE_TYPES.items():
        if index in indexes:
            return fingersstate_type


def generate_notearray_chord(chord, tonality):
    '''
    This method returns and number array contain degree.
    give a chord with this structure :
        chord = {'degree': 5, 'name': 'M7'}
        tonality = int >= 0 and int <=11
    '''
    concert_pitch_array = remap_array(
        array=CHORDS[chord['name']], offset=chord['degree'], value=12)
    return remap_array(array=concert_pitch_array, offset=tonality, value=12)


def generate_notearray_scale(chord, tonality):
    '''
    This method returns and number array contain degree as scale.
    '''
    for scalename, chordnames in SCALENAME_BY_CHORDNAME.items():
        if chord['name'] in chordnames:
            scale = SCALES[scalename][:]
            replacements = CHORD_SCALES_REMPLACEMENT_INDEXES.get(chord['name'])
            if replacements:
                for scale_index, chord_index in replacements.items():
                    scale[scale_index] = CHORDS[chord['name']][chord_index]

            offset = chord['degree'] + tonality
            return remap_array(array=scale, offset=offset, value=12)


def generate_melody_from_eighthmetas(reference_note, eighthmetas, tonality):
    """
    This method generate a melody as note array based on eighthmetas.
    """
    melody_length = define_melody_length(eighthmetas)
    eighthmetas = eighthmetas[:melody_length]
    behavior = eighthmetas[0]['behavior']
    fingersstates = [em['fingersstate'] for em in eighthmetas]

    chord_array = generate_notearray_chord(
        chord=eighthmetas[0]['chord'], tonality=tonality)
    chord_array_destination = generate_notearray_chord(
        chord=eighthmetas[-1]['chord'], tonality=tonality)

    if behavior == 'arpegic':
        return generate_arpegic_melody(
            chord_array=chord_array[:],
            chord_array_destination=chord_array_destination[:],
            length=melody_length)

    elif behavior == 'static':
        if len(set(fingersstates)) == 1:
            return generate_static_melody(
                reference_note=reference_note,
                chord_array=chord_array[:],
                chord_array_destination=chord_array_destination[:],
                length=melody_length)

    melody = generate_chromatic_melody(
        reference_note=reference_note,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        length=melody_length)

    if melody is None:
        scale = generate_notearray_scale(
            chord=eighthmetas[0]['chord'], tonality=tonality)

        melody = generate_diatonic_melody(
            reference_note=reference_note,
            chord_array=chord_array[:],
            chord_array_destination=chord_array_destination[:],
            scale=scale[:],
            length=melody_length)

    if melody is None:
        melody = generate_arpegic_melody(
            chord_array=chord_array[:],
            chord_array_destination=chord_array_destination[:],
            length=melody_length)

    return melody


def convert_melody_to_eighthnotes(melody, fingerstates):
    eighthsnotes = []
    for note, fingersstate in zip(melody, fingerstates):
        eighthsnote = [note if state else None for state in fingersstate]
        eighthsnotes.append(eighthsnote)

    return eighthsnotes


def define_melody_length(eighthmetas):
    length = min([
        count_occurence_continuity([d['chord'] for d in eighthmetas]),
        count_occurence_continuity([d['behavior'] for d in eighthmetas])])
    if length < len(eighthmetas):
        length += 1
    return length


def generate_arpegic_melody(
        chord_array, chord_array_destination, length):

    descending = choose({False: 2, True: 1})
    if descending:
        chord_array.reverse()
        # offset to ensure the good start note
        chord_array = offset_array(chord_array, 4)

    original_chord_notes_iterator = itertools.cycle(chord_array)
    notes = [
        next(original_chord_notes_iterator)
        for _ in range(length)]

    if chord_array == chord_array_destination:
        return notes

    last_note = choose({
        chord_array_destination[0]: 3,
        chord_array_destination[2]: 1})
    return notes[:-1] + [last_note]


def generate_static_melody(
        reference_note, chord_array, chord_array_destination, length):

    if reference_note:
        note = find_closer_number(
            reference=reference_note,
            array=(chord_array[0], chord_array[2]),
            clamp=12)
    else:
        note = choose({chord_array[0]: 5, chord_array[0]: 1})

    if chord_array == chord_array_destination:
        return [note] * length
    return [note] * (length - 1)


def generate_chromatic_melody(
        reference_note, chord_array, chord_array_destination, length):

    if reference_note:
        startnote = find_closer_number(
            reference=reference_note,
            array=(chord_array[0], chord_array[2]),
            clamp=12)
    else:
        startnote = choose({chord_array[0]: 5, chord_array[0]: 1})

    destination_notes = chord_array_destination[0], chord_array_destination[2]

    if startnote + (length - 1) in destination_notes:
        return [n for n in range(startnote, startnote + length)]
    elif startnote - (length - 1) in destination_notes:
        return sorted([
            n for n in range(startnote - (length - 1), startnote + 1)],
            reverse=True)
    return None


def generate_diatonic_melody(
        reference_note, chord_array, chord_array_destination, scale, length):

    if reference_note:
        startnote_index = scale.index(
            find_closer_number(
                reference=reference_note, array=chord_array, clamp=12))
    else:
        startnote_index = choose({chord_array[0]: 5, chord_array[0]: 1})

    startnote_index_offsets = [
        remap_number(startnote_index + (length - 1), value=7),
        remap_number(startnote_index - (length - 1), value=7)]

    for startnote_index_offset in startnote_index_offsets:
        if scale[startnote_index_offset] in chord_array_destination:
            return [
                scale[remap_number(startnote_index + index, value=7)]
                for index in range(length)]

    return None


##############################################################################
#  GENERATORS / ITERATOR / CONVERTOR
##############################################################################


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


def convert_eighthmetas_to_eighthnotes(eighthnotes, eighthmetas, tonality):
    """
    this is the main conversion meta, it transform meta data to notes array
    by finger pressed.
    The method need the last eighthnotes generated as reference to continue
    a cohenrent melody and chord progession. Firstly, it convert all mute
    eighthmeta to MUTE_EIGHTH because it is not used for melody and chord
    generation. Secondly it generate a melody as notearray. And finally the
    melody is used to convert the chords eighthnotes.
    """
    # To avoid immutable bad surprises
    eighths = eighthmetas[:]

    if get_fingersstate_type(eighthmetas[0]['fingersstate']) == 'mute':
        return [MUTE_EIGHTH]

    for i, eighth in enumerate(eighthmetas):
        if get_fingersstate_type(eighth['fingersstate']) == 'mute':
            eighths[i] = MUTE_EIGHTH

    melodic_eighthnotes = [
        eighthnote for eighthnote in eighthnotes
        if get_fingersstate_type(eighthnote) == 'melodic']

    if melodic_eighthnotes:
        reference_note = [
            note for note in melodic_eighthnotes[-1] if note is not None][0]
    else:
        reference_note = None

    melodic_eighthmetas = [
            em for em in eighthmetas
            if get_fingersstate_type(em['fingersstate']) == 'melodic']

    melody = generate_melody_from_eighthmetas(
        reference_note=reference_note,
        eighthmetas=melodic_eighthmetas,
        tonality=tonality)
    melodic_fingerstates = [
        me['fingersstate'] for me in melodic_eighthmetas[:len(melody)]]
    melodic_eighthnotes = convert_melody_to_eighthnotes(
        melody=melody, fingerstates=melodic_fingerstates)

    indexes = [
        i for i, em in enumerate(eighthmetas)
        if get_fingersstate_type(em['fingersstate']) == 'melodic'][:len(melody)]

    if indexes:
        eighths = replace_in_array(indexes, melodic_eighthnotes, eighths)
        eighths = eighths[:indexes[-1] + 1]

    chord_fingernotes = [
        eighthnote for eighthnote in eighthnotes
        if get_fingersstate_type(eighthnote) == 'chord']
    reference_chord = chord_fingernotes[-1] if chord_fingernotes else None

    chords = generate_chords_from_eighthmetas(
        reference_chord=reference_chord,
        reference_note=reference_note,
        wip_eighths=eighths,
        tonality=tonality)

    indexes = [
        i for i, em in enumerate(eighthmetas)
        if get_fingersstate_type(em['fingersstate']) == 'chord'][:len(chords)]

    if indexes:
        eighths = replace_in_array(
            indexes, chords, eighths)

    return eighths


def generate_chords_from_eighthmetas(
        reference_chord, reference_note, wip_eighths, tonality):

    chords_eighthnotes = []
    for eighth in wip_eighths:
        if eighth == MUTE_EIGHTH:
            continue
        if not isinstance(eighth, dict):
            reference_note = [n for n in eighth if n is not None][0]
            continue

        chord_array = generate_notearray_chord(eighth['chord'], tonality)
        fingersstate = eighth['fingersstate']
        len_current_chord = len([n for n in fingersstate if n])
        if len_current_chord == 5:
            chords_eighthnotes.append(chord_array)
            reference_chord = chord_array
            continue

        indexes_priority = CHORD_INDEXES_PRIORITY_ORDER.get(
            eighth['chord']['name'], [0, 1, 2, 3, 4])

        chord_notes_used = []
        for i in indexes_priority:
            note = chord_array[i]
            if note != reference_note:
                chord_notes_used.append(note)
            if len(chord_notes_used) == len_current_chord:
                break

        i = 0
        eighthnotes = []
        for finger in fingersstate:
            if not finger:
                eighthnotes.append(None)
            else:
                eighthnotes.append(chord_notes_used[i])
                i += 1

        chords_eighthnotes.append(eighthnotes)
        reference_chord = chord_array
    return chords_eighthnotes


def montuno_generator(
        pattern, chord_grid, tonality, forced_behavior=None):

    data_it = eighthmetas_iterator(
        pattern, chord_grid, forced_behavior)

    processed_datas = [None, None, None, None]
    to_process_datas = next(data_it) + next(data_it)

    while True:
        datas = convert_eighthmetas_to_eighthnotes(
            processed_datas, to_process_datas,
            tonality)

        for data in datas:
            yield data

        processed_datas = processed_datas[-len(datas)+1:-1] + datas
        to_process_datas = to_process_datas[len(datas):]

        while len(to_process_datas) < 8:
            to_process_datas += next(data_it)


if __name__ == '__main__':
    def test():
        import time

        montunos = montuno_generator(
            pattern=PATTERNS['basic'],
            chord_grid=CHORDGRIDS['example'],
            tonality=5)
        print (montunos)

        for _ in range(125):
            time.sleep(.075)
            print(next(montunos))
