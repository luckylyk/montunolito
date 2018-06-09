
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


scale_by_chord = dict(
    major = ('Major', 'M6', 'M7', 'M7M', 'M7b9', 'M9', 'M11', 'Sus4'),
    minor = ('Minor', 'm6', 'm7', 'm7M', 'm7b9', 'm9', 'm11', 'dim', 'qm'))


pitches = [0, 1, 2, 3, 4, 5]


# this is a list of hand posing pattern for piano
# it represant thumd, index, middle, ring and pinkie
# 0 mean the finger is not pressing a key
# 1, it's pressing a key.
fingersstates = (
    (0, 0, 0, 0, 0), (1, 0, 0, 0, 1), (1, 0, 0, 0, 0), (0, 1, 0, 0, 0),
    (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 1, 1, 1, 0), (1, 1, 1, 1, 1))


fingersstate_types = {
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
#  GENERATORS / ITERATOR / CONVERTOR
##############################################################################
"""
nomenclature : 
    chord = {'degree': 0, 'name': 'Minor'}
    tonality = int (factor to offset all values)
    fingersstate = (0, 1, 1, 1, 0)
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
    index = fingersstates.index(fingersstate)
    for fingersstate_type, indexes in fingersstate_types.items():
        if index in indexes:
            return fingersstate_type


def reverse_chord(chord, degree):
    ''' this method offset a chord list '''
    return chord[degree:] + chord[:5-degree]


def remap_note(index):
    ''' this method remap note to force value to be between 0 - 11 '''
    while index > 11:
        index -= 11
    return index


def remap_notearray(note, array):
    ''' this method is usefull to repitch a scale '''
    return [remap_note(index + note) for index in array]


def generate_notearray_chord(chord, tonality):
    '''
    this return and number array contain degree.
    give a chord with this structure :
        chord = {'degree': 5, 'name': 'M7'}
        tonality = int >= 0 and int <=11
    '''
    concert_pitch_array = remap_notearray(
        chord['degree'], chords[chord['name']])
    return remap_notearray(tonality, concert_pitch_array)


def generate_notearray_scale(chord, tonality):
    scalename = 'major' if chord['name'] in scale_by_chord['major'] else 'minor'
    chordnotes = generate_notearray_chord(chord, tonality)
    return scales[scalename]


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


def pick_favorite_behavior(pattern, index):
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
        fingersstates_retrieved.append(fingersstates[index])
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
            pick_favorite_behavior(pattern, pattern_index))

        yield create_meta_eighths (
            pattern_index, pattern, chords, prefered_behavior)


def convert_meta_eighths_to_fingersnotes(
        processed_datas, meta_eighths, tonality, behavior):

    if get_fingersstate_type(meta_eighths[0]) == 'mute':
        return [[None, None, None, None, None]]

    melodic_indexes = []
    chord_indexes = []
    mute_indexes = []
    for i, data in enumerate(meta_eighths):
        if get_fingersstate_type(data) == 'melodic':
            melodic_indexes.append(i)
        elif get_fingersstate_type(data) == 'chord':
            chord_indexes.append(i)
        elif get_fingersstate_type(data) == 'mute':
            mute_indexes.append(i)

    melodic_processed_datas = [
        data for data in processed_datas
        if get_fingersstate_type(data) == 'melodic']

    melodic_datas = [
            data for i, data in enumerate(meta_eighths)
            if i in melodic_indexes]

    melody = generate_melody_from_meta_eighths(
        processed_datas=melodic_processed_datas,
        meta_eighths=melodic_datas,
        tonality=tonality)

    chords = generate_chord_from_datas()

    return combine_chord_and_melody(
        melody, chords, melodic_indexes, chord_indexes)

def combine_chord_and_melody(melody, chords, melodic_indexes, chord_indexes):
    pass


def generate_melody_from_meta_eighths(processed_datas, meta_eighths, tonality):
    assert set([get_fingersstate_type(me['fingersstate']) for me in meta_eighths]) == {'melodic'}

    # define the melody length who will be generated
    melody_lenght = min([
        count_continuity([d['chord'] for d in meta_eighths]),
        count_continuity([d['behavior'] for d in meta_eighths])])
    if melody_lenght < len(meta_eighths):
        melody_lenght += 1
    meta_eighths = meta_eighths[:melody_lenght]

    # analyse reference datas
    reference_note = [
        note for note in processed_datas[-1] if note is not None][0]

    behavior = meta_eighths[0]['behavior']
    fingersstates = [d['fingersstate'] for d in meta_eighths]
    original_chord = generate_notearray_chord(
        chord=meta_eighths[0]['chord'], tonality=tonality)
    destination_chord = generate_notearray_chord(
        chord=meta_eighths[-1]['chord'], tonality=tonality)

    if behavior == 'arpegic':
        original_chord_notes_iterator = itertools.cycle(original_chord)
        notes = [
            next(original_chord_notes_iterator)
            for _ in range(melody_lenght)]
        if original_chord == destination_chord:
            return notes
        return notes[:-1] + [random.choice(
            [destination_chord[0]] * 3 + [destination_chord[2]])]

    if behavior == 'static':
        if len(set(fingersstates)) != 1:
            behavior = 'chromatic'

    if behavior == 'static':
        note = find_closer_number(
            number=reference_note,
            array=(original_chord[0], original_chord[2]))

        if original_chord == destination_chord:
            return [note] * melody_lenght
        else:
            return [note] * (melody_lenght - 1)

    if behavior == 'chromatic' or behavior == 'melodic':

        startnote = find_closer_number(
            number=reference_note,
            array=(original_chord[0], original_chord[2]))

        destination_notes = destination_chord[0],  destination_chord[2]
        if startnote + (len(meta_eighths) - 1) in destination_notes:
            return range(startnote, startnote + len(meta_eighths))
        elif startnote - (len(meta_eighths) - 1) in destination_notes:
            return sorted(
                range(startnote - (len(meta_eighths) - 1), startnote + 1), reverse=True)
        else:
            print ('not chromaticable')
            behavior = 'melodic'


    chord_is_reversed = bool(
        find_closer_number(
            number=reference_note,
            array=(original_chord[0], original_chord[2]), index=True))
    if chord_is_reversed:
        original_chord = reverse_chord(chord=original_chord, degree=2)

    elif behavior == 'melodic':
        pass


def generate_chord_from_datas():
    return None


def find_closer_number(number, array, clamp=11, index=False):
    if number in array:
        return array.index(number) if index else number

    closer_difference = None
    for i, num in enumerate(array):
        difference = min(abs(number - num), abs(number + (num - clamp)))
        if not closer_difference or closer_difference > difference:
            closer_index = i
            closer_difference = difference
    return closer_index if index else array[closer_index]


def count_continuity(array):
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
    # gen = meta_eighths_iterator(
    #     rythmic_patterns['basic'], chord_grids['example'])

    # for _ in range(2):
    #     for elt in next(gen):
    #         print (elt)
    # for chord in (
    #     {'degree': 0, 'name': 'Minor'},
    #     {'degree': 1, 'name': 'Minor'},
    #     {'degree': 2, 'name': 'Minor'},
    #     {'degree': 3, 'name': 'Minor'},
    #     {'degree': 4, 'name': 'Minor'},
    #     {'degree': 5, 'name': 'Minor'}):
    #         print(generate_notearray_chord(chord, 0))
    generated_eighth = ([2, 0, 0, 0, 2], [3, 0, 0, 0, 3], [4, 0, 0, 0, 4])
    datas = [
        {'chord': {'degree': 4, 'name': 'M7'}, 'fingersstate': (1, 0, 0, 0, 1), 'behavior': 'chromatic'},
        {'chord': {'degree': 4, 'name': 'M7'}, 'fingersstate': (0, 1, 0, 0, 0), 'behavior': 'chromatic'},
        {'chord': {'degree': 2, 'name': 'M7'}, 'fingersstate': (0, 0, 1, 0, 0), 'behavior': 'chromatic'},
        {'chord': {'degree': 4, 'name': 'M7'}, 'fingersstate': (0, 0, 0, 1, 0), 'behavior': 'chromatic'},
        {'chord': {'degree': 4, 'name': 'M7'}, 'fingersstate': (1, 0, 0, 0, 1), 'behavior': 'chromatic'},
    ]
    for data in generate_melody_from_meta_eighths(generated_eighth, datas, 3):
        print(data)
