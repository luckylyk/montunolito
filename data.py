
##############################################################################
#  CORE / CONSTANTS
##############################################################################

NOTES = dict(
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


chord_grids = dict(
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


def unit_test_math():
    print("MATH UTILS UNIT TEST -- > started")

    print("####################")
    print("#find_closer_number#")
    print("####################")
    assert find_closer_number(reference=8, array=(3, 6, 7, 8), clamp=12) == 8
    assert find_closer_number(reference=4, array=(3, 6, 7, 8), clamp=12) == 3
    assert find_closer_number(reference=14, array=(3, 6, 7, 8), clamp=12) == 3
    assert find_closer_number(reference=4, array=(3, 6, 7, 8), return_index=True) == 0
    print()


    print("############################")
    print("#count_occurence_continuity#")
    print("############################")
    assert count_occurence_continuity(['salut', 'salut', 'salut', 'prout', 'salut']) == 3
    assert count_occurence_continuity(['salut', 'prout', 'salut', 'salut', 'salut']) == 1
    assert count_occurence_continuity([5, 4, 3, 2, 1]) == 1
    assert count_occurence_continuity(['a', 'a', 'a', 'a', 'a', 'a']) == 6
    assert count_occurence_continuity(['salut', 'salut', 'salut', 'salut', 'prout']) == 4
    print()

    print("##############")
    print("#remap_number#")
    print("##############")
    assert remap_number(-1, value=12) == 11
    assert remap_number(10, value=12) == 10
    assert remap_number(14, value=12) == 2
    assert remap_number(0, value=12) == 0
    assert remap_number(62, value=12) == 2
    print()
    print("MATH UTILS UNIT TEST -- > finished")


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
    fingersnote = [None, 2, 6, 8, None]
        list representing note played by pressed fingers. None is
        for released fingers
    behavior = list of constant for algorythme, represention the melodic behavior
    meta_eighth = 
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
    fingersstate = tuple([1 if value > 0 else 0 for value in fingersstate])
    index = FINGERSSTATES.index(fingersstate)
    for fingersstate_type, indexes in FINGERSSTATE_TYPES.items():
        if index in indexes:
            return fingersstate_type


def reverse_chord(chord, degree):
    ''' this method offset a chord list '''
    return chord[degree:] + chord[:5-degree]


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

            return remap_array(array=scale, offset=tonality, value=12)


def generate_melody_from_meta_eighths(reference_note, meta_eighths, tonality):
    """
    This method generate a melody as note array based on meta_eighths.
    """
    melody_lenght = define_melody_lenght(meta_eighths)
    meta_eighths = meta_eighths[:melody_lenght]
    behavior = meta_eighths[0]['behavior']
    fingersstates = [me['fingersstate'] for me in meta_eighths]

    chord_array = generate_notearray_chord(
        chord=meta_eighths[0]['chord'], tonality=tonality)
    chord_array_destination = generate_notearray_chord(
        chord=meta_eighths[-1]['chord'], tonality=tonality)

    if behavior == 'arpegic':
        return generate_arpegic_melody(
            chord_array, chord_array_destination, melody_lenght)

    elif behavior == 'static':
        if len(set(fingersstates)) == 1:
            return generate_static_melody(
                reference_note, chord_array,
                chord_array_destination, melody_lenght)

    melody = generate_chromatic_melody(
        reference_note, chord_array, chord_array_destination, meta_eighths)

    melody = melody or generate_diatonic_melody(
        reference_note, chord_array, chord_array_destination,
        meta_eighths, tonality)

    melody = melody or generate_arpegic_melody(
        chord_array, chord_array_destination, melody_lenght)
    
    return melody


def define_melody_lenght(meta_eighths):
    lenght = min([
        count_occurence_continuity([d['chord'] for d in meta_eighths]),
        count_occurence_continuity([d['behavior'] for d in meta_eighths])])
    if lenght < len(meta_eighths):
        lenght += 1
    return lenght


def generate_arpegic_melody(
        chord_array, chord_array_destination, melody_lenght):

    descending = random.choice([False] * 2 + [True])
    if descending:
        chord_array.reverse()
        # offset to ensure the good start note
        chord_array = reverse_chord(chord_array, 4)

    original_chord_notes_iterator = itertools.cycle(chord_array)
    notes = [
        next(original_chord_notes_iterator)
        for _ in range(melody_lenght)]

    if chord_array == chord_array_destination:
        return notes

    return notes[:-1] + [random.choice(
        [chord_array_destination[0]] * 3 + [chord_array_destination[2]])]


def generate_static_melody(
        reference_note, chord_array, chord_array_destination, melody_lenght):

    note = find_closer_number(
        reference=reference_note,
        array=(chord_array[0], chord_array[2]),
        clamp=12)

    if chord_array == chord_array_destination:
        return [note] * melody_lenght
    else:
        return [note] * (melody_lenght - 1)

    return None


def generate_chromatic_melody(
        reference_note, chord_array, chord_array_destination, meta_eighths):

    startnote = find_closer_number(
        reference=reference_note,
        array=(chord_array[0], chord_array[2]),
        clamp=12)

    destination_notes = chord_array_destination[0], chord_array_destination[2]

    if startnote + (len(meta_eighths) - 1) in destination_notes:
        return range(startnote, startnote + len(meta_eighths))
    elif startnote - (len(meta_eighths) - 1) in destination_notes:
        return sorted(
            range(startnote - (len(meta_eighths) - 1), startnote + 1),
            reverse=True)
    return None


def generate_diatonic_melody(
        reference_note, chord_array, chord_array_destination,
        meta_eighths, tonality):

    scale = generate_notearray_scale(
        chord=meta_eighths[0]['chord'], tonality=tonality)

    startnote_index = scale.index(
        find_closer_number(
            reference=reference_note, array=chord_array, clamp=12))

    startnote_index_offsets = [
        remap_number(startnote_index + (len(meta_eighths) - 1), value=7),
        remap_number(startnote_index - (len(meta_eighths) - 1), value=7)]

    for startnote_index_offset in startnote_index_offsets:
        if scale[startnote_index_offset] in chord_array_destination:
            return [
                scale[remap_number(startnote_index + index, value=7)]
                for index in range(len(meta_eighths))]

    return None


def unti_test_melody():
    print("MELODY UNIT TEST -- > started")

    print("###################")
    print("#scales generation#")
    print("###################")
    def names(notearray):
        ns = {v: k for k, v in NOTES.items()}
        return [ns[n] for n in notearray]

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
    print()

    print("###################")
    print("#Melody generation#")
    print("###################")
    # static
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

    # arpegic

    chord_array = [4, 7, 10, 0, 3]
    chord_array_destination = [5, 7, 10, 0, 3]
    assert generate_arpegic_melody(chord_array[:], chord_array_destination[:], 8) in ([4, 3, 4, 3, 4, 3, 4, 5], [4, 3, 4, 3, 4, 3, 4, 10], [4, 7, 10, 0, 3, 4, 7, 5], [4, 7, 10, 0, 3, 4, 7, 10])
    assert generate_arpegic_melody(chord_array[:], chord_array_destination[:], 8) in ([4, 3, 4, 3, 4, 3, 4, 5], [4, 3, 4, 3, 4, 3, 4, 10], [4, 7, 10, 0, 3, 4, 7, 5], [4, 7, 10, 0, 3, 4, 7, 10])
    assert generate_arpegic_melody(chord_array[:], chord_array_destination[:], 8) in ([4, 3, 4, 3, 4, 3, 4, 5], [4, 3, 4, 3, 4, 3, 4, 10], [4, 7, 10, 0, 3, 4, 7, 5], [4, 7, 10, 0, 3, 4, 7, 10])
    assert generate_arpegic_melody(chord_array[:], chord_array_destination[:], 8) in ([4, 3, 4, 3, 4, 3, 4, 5], [4, 3, 4, 3, 4, 3, 4, 10], [4, 7, 10, 0, 3, 4, 7, 5], [4, 7, 10, 0, 3, 4, 7, 10])


    print("MELODY UNIT TEST -- > finished")
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
    last_index = (4, random.randint(1, len(pattern[4]) - 1))
    while True:
        qpatterns = pattern['relationships'][last_index]
        index = random.choice(
            [t for k, v in qpatterns.items() for t in tuple([k] * v) if v])
        yield index
        last_index = index


def choose_favorite_behavior(pattern, index):
    '''
    this method pick a random comportement in the pattern subdict 'behavior'
    using the indice of probabilty defined in the dict.
    '''
    behavior_prefs = pattern['behaviors'][index]
    return random.choice([
        t for k, v in behavior_prefs.items()
        for t in tuple([k] * v) if v])


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


def create_meta_eighths(
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


def meta_eighths_iterator(
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
            mandatory_behavior or
            choose_favorite_behavior(pattern, pattern_index))

        yield create_meta_eighths (
            pattern_index, pattern, chords, prefered_behavior)


def convert_meta_eighths_to_fingersnotes(fingersnotes, meta_eighths, tonality):
    """
    this is the main conversion meta, it transform meta data to notes array
    by finger pressed.
    The method need the last fingersnotes generated as reference to continue
    a cohenrent melody and chord progession. Firstly, it convert all mute
    meta_eighth to MUTE_EIGHTH because it is not used for melody and chord
    generation. Secondly it generate a melody as notearray. And finally the
    melody is used to convert the chords fingersnotes.
    """
    meta_eighths = meta_eighths[:]

    if get_fingersstate_type(meta_eighths[0]['fingersstate']) == 'mute':
        return MUTE_EIGHTH

    for i, eighth in enumerate(meta_eighths):
        if get_fingersstate_type(eighth['fingersstate']) == 'mute':
            meta_eighths[i] = MUTE_EIGHTH

    melodic_fingersnotes = [
        fingersnote for fingersnote in fingersnotes
        if get_fingersstate_type(fingersnote) == 'melodic']
    reference_note = [
        note for note in melodic_fingersnotes[-1] if note is not None][0]

    melodic_meta_eighths = [
            me for me in meta_eighths
            if get_fingersstate_type(me['fingersstate']) == 'melodic']

    print ("reference note:", reference_note)
    melody = generate_melody_from_meta_eighths(
        reference_note=reference_note,
        meta_eighths=melodic_meta_eighths,
        tonality=tonality)

    indexes = [
        i for i, me in enumerate(meta_eighths)
        if get_fingersstate_type(me['fingersstate']) == 'melodic']

    wip_eighths = combine_eight_and_meta_eighths(
        indexes, melody, meta_eighths)

    chord_fingernotes = [
        fingersnote for fingersnote in fingersnotes
        if get_fingersstate_type(fingersnote) == 'chord']
    reference_chord = chord_fingernotes[-1] if chord_fingernotes else None

    chord = generate_chords_from_meta_eights(
        reference_chord=reference_chord,
        reference_note=reference_note,
        fingernotes=chord_fingernotes,
        wip_eighths=wip_eighths,
        tonality=tonality)

    eighths = combine_eight_and_meta_eighths(
        melody, chords, melodic_indexes, chord_indexes, mute_indexes)

    return meta_eighths


def combine_eight_and_meta_eighths(indexes, eights, meta_eighths):

    wip_meta_eighths = list(meta_eighths[:indexes[len(eights)] - 1][:])
    for i, eighth in enumerate(eights):
        # Combined with chord
        if isinstance(eighth, int):
            wip_meta_eighths[indexes[i]] = eighth
            continue
        # Combined with melody
        wip_meta_eighths[indexes[i]] = [
            eighth if state else None for state in
            wip_meta_eighths[indexes[i]]['fingersstate']]
    return wip_meta_eighths


def generate_chords_from_meta_eights(
        reference_chord, reference_note, wip_eighths, tonality):

    chords_fingersnotes = []
    for eighth in wip_eighths:
        if eighth == MUTE_EIGHTH:
            continue
        if not isinstance(eighth, dict):
            reference_note = [n for n in eighth[-1] if n is not None][0]
            continue

        chord_notearray = generate_notearray_chord(eighth['chord'], tonality)
        len_current_chord = len([n for n in eighth['fingersstate']])
        if len_current_chord == 5:
            chords_fingersnotes.append(chord_notearray)
            reference_chord = chord_notearray
            continue

        indexes_priority = CHORD_INDEXES_PRIORITY_ORDER.get(
            eighth['chord']['name'], [0, 1, 2, 3, 4])

        if reference_chord:
            pass #'TODO'

        chords_fingersnotes.append(chord_notearray)
        reference_chord = chord_notearray
    return None


def montuno_generator(  # Find better name
        pattern, chord_grid, tonality, mode, forced_behavior=None):

    data_it = meta_eighths_iterator(
        pattern, chord_grid, forced_behavior)

    processed_datas = [None, None, None, None]
    to_process_datas = next(data_it) + next(data_it)

    while True:
        datas = convert_meta_eighths_to_fingersnotes(
            processed_datas, to_process_datas,
            tonality, forced_behavior)

        for data in datas:
            yield data

        processed_datas = processed_datas[-len(datas)+1:-1] + datas
        to_process_datas = to_process_datas[len(datas):]

        while len(to_process_datas) < 8:
            to_process_datas += next(data_it)


if __name__ == '__main__':
    unit_test_math()

    print("\n##############\n### TEST 1 ###\n##############\nMeta Eighths Generation")
    gen = meta_eighths_iterator(
        rythmic_patterns['basic'], chord_grids['example'])

    for _ in range(10):
        for elt in next(gen):
            print (elt)

    print("\n##############\n### TEST 2 ###\n##############\nChord array generation")
    for chord in (
        {'degree': 0, 'name': 'Minor'},
        {'degree': 1, 'name': 'Minor'},
        {'degree': 2, 'name': 'Minor'},
        {'degree': 3, 'name': 'Minor'},
        {'degree': 4, 'name': 'Minor'},
        {'degree': 5, 'name': 'Minor'}):
            print(generate_notearray_chord(chord, 0))

    unti_test_melody()


    # print("\n##############\n### TEST 5 ###\n##############\nMelody Generation")
    # reference_note = 4
    # meta_eighths = [
    #     {'chord': {'degree': 4, 'name': 'Major'}, 'fingersstate': (1, 0, 0, 0, 1), 'behavior': 'melodic'},
    #     {'chord': {'degree': 4, 'name': 'Major'}, 'fingersstate': (0, 1, 0, 0, 0), 'behavior': 'melodic'},
    #     {'chord': {'degree': 4, 'name': 'Major'}, 'fingersstate': (0, 0, 1, 0, 0), 'behavior': 'melodic'},
    #     {'chord': {'degree': 4, 'name': 'Major'}, 'fingersstate': (0, 0, 0, 1, 0), 'behavior': 'melodic'},
    #     {'chord': {'degree': 4, 'name': 'Major'}, 'fingersstate': (1, 0, 0, 0, 1), 'behavior': 'melodic'},
    # ]
    # print((generate_melody_from_meta_eighths(reference_note, meta_eighths, tonality=3)))


    # print("\n##############\n### TEST 6 ###\n##############\nRecompile Melody")

    # fingernotes=(
    #     [0, 3, 0, 0, 0],
    #     [0, 0, 6, 0, 0],
    #     [0, 0, 0, 0, 0],
    #     [0, 5, 3, 8, 0],
    #     [0, 0, 0, 9, 0],
    #     [1, 0, 0, 0, 1])

    # meta_eighths=[
    #     {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (1, 0, 0, 0, 1)},
    #     {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (0, 1, 0, 1, 0)},
    #     {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (0, 1, 0, 1, 0)},
    #     {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'arpegic', 'fingersstate': (1, 0, 0, 0, 1)},
    #     {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'chromatic', 'fingersstate': (0, 0, 0, 0, 0)},
    #     {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'chromatic', 'fingersstate': (1, 0, 0, 0, 1)},
    #     {'chord': {'name': 'M7', 'degree': 5}, 'behavior': 'chromatic', 'fingersstate': (0, 0, 0, 0, 0)},
    #     {'chord': {'name': 'M7', 'degree': 5}, 'behavior': 'chromatic', 'fingersstate': (1, 0, 0, 0, 1)},
    #     {'chord': {'name': 'M7', 'degree': 5}, 'behavior': 'static', 'fingersstate': (0, 0, 0, 0, 0)},
    #     {'chord': {'name': 'M7', 'degree': 5}, 'behavior': 'static', 'fingersstate': (0, 1, 0, 1, 0)},
    #     {'chord': {'name': 'M7', 'degree': 5}, 'behavior': 'static', 'fingersstate': (0, 0, 0, 0, 0)},
    #     {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'static', 'fingersstate': (0, 1, 0, 1, 0)},
    #     {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'diatonic', 'fingersstate': (0, 0, 0, 0, 0)},
    #     {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'diatonic', 'fingersstate': (1, 0, 0, 0, 0)},
    #     {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'diatonic', 'fingersstate': (0, 1, 0, 0, 0)},
    #     {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'diatonic', 'fingersstate': (0, 0, 1, 0, 0)},
    #     {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (1, 0, 0, 0, 0)},
    #     {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (0, 1, 0, 0, 0)},
    #     {'chord': {'name': 'Minor', 'degree': 1}, 'behavior': 'arpegic', 'fingersstate': (0, 0, 0, 1, 0)},
    #     {'chord': {'name': 'Minor', 'degree': 4}, 'behavior': 'arpegic', 'fingersstate': (1, 0, 0, 0, 1)}]
    # convert_meta_eighths_to_fingersnotes(fingernotes, meta_eighths, 0)
