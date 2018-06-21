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

from .solfege import (
    FINGERSSTATES, FINGERSSTATE_TYPES, CHORDS, SCALENAME_BY_CHORDNAME, SCALES,
    CHORD_SCALES_REMPLACEMENT_INDEXES, MUTE_EIGHTH, CHORD_INDEXES_PRIORITY_ORDER)

from .utils import (
    remap_array, remap_number, find_closer_number, choose, offset_array,
    count_occurence_continuity, replace_in_array)


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
    This is the main melodic generation method. It receive a reference_note and
    a list of melodic eightmetas. It decide which sort of melody has to be
    generated and generate it.
    """
    melody_length = define_melody_length(eighthmetas)
    eighthmetas = eighthmetas[:melody_length]
    behavior = eighthmetas[0]['behavior']
    fingersstates = [em['fingersstate'] for em in eighthmetas]

    chord_array = generate_notearray_chord(
        chord=eighthmetas[0]['chord'], tonality=tonality)
    chord_array_destination = generate_notearray_chord(
        chord=eighthmetas[-1]['chord'], tonality=tonality)

    melody = None
    if behavior == 'arpegic':
        melody = generate_arpegic_melody(
            chord_array=chord_array[:],
            chord_array_destination=chord_array_destination[:],
            length=melody_length)

    elif behavior == 'static':
        if len(set(fingersstates)) == 1:
            melody = generate_static_melody(
                reference_note=reference_note,
                chord_array=chord_array[:],
                chord_array_destination=chord_array_destination[:],
                length=melody_length)

    if melody is None:
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

    eighthnotes = convert_melody_to_eighthnotes(
            melody=melody, fingersstates=fingersstates)

    return eighthnotes


def convert_melody_to_eighthnotes(melody, fingersstates):
    '''
    this method combine afingersstates array and a melody array to create
    eighthnotes.
    '''
    eighthsnotes = []
    for note, fingersstate in zip(melody, fingersstates):
        eighthsnote = [note if state else None for state in fingersstate]
        eighthsnotes.append(eighthsnote)

    return eighthsnotes


def define_melody_length(eighthmetas):
    '''
    this method check the eighthmetas continuity and return the lenght of the
    generable melody.
    '''
    length = min([
        count_occurence_continuity([d['chord'] for d in eighthmetas]),
        count_occurence_continuity([d['behavior'] for d in eighthmetas])])
    if length < len(eighthmetas):
        length += 1
    return length


def generate_arpegic_melody(
        chord_array, chord_array_destination, length):
    '''
    this method return and number array. The method iter the chord array and 
    select a destination note in the destination chord array.
    There iteration sens (normal or reverted) is random
    '''
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
    '''
    this method generate a static melody. It means, it find a coherent note and
    create an array: [number] * length given.
    '''
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
    '''
    This method generate a chromatical melody. Chromatical mean, melody iterate
    by half tones. An half tone is represented by a difference of 1 between two
    notes.. So the array will look like :  [2, 3, 4, 5] or [10, 9, 8, 7, 6]

    This method analyse the reference note, the chord array and the destination
    array. Firstly it select a melody startnote. It analyse the possible
    destionation notes in the destination array: chord_array_destination[0]&[2]
    (tonic or quint).
    If there's a chromatical transition possible between the startnote and any
    destination respecting the lenght given, it return a number array.
    If there no target possible, it return None.
    '''
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
    '''
    This method is pretty similar as generate_chromatic_melody but it receive a
    scale as arg. Instead of iterate by half tones, it iter on the scale.
    '''
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


def convert_eighthmetas_to_eighthnotes(eighthnotes, eighthmetas, tonality):
    '''
    this is the main conversion meta, it transform meta data to notes array
    by finger pressed.
    The method need the last eighthnotes generated as reference to continue
    a cohenrent melody and chord progession. Firstly, it convert all mute
    eighthmeta to MUTE_EIGHTH because it is not used for melody and chord
    generation. Secondly it generate a melody as notearray. And finally the
    melody is used to convert the chords eighthnotes.
    '''
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

    melodic_eighthnotes = generate_melody_from_eighthmetas(
        reference_note=reference_note,
        eighthmetas=melodic_eighthmetas,
        tonality=tonality)
    lenght = len(melodic_eighthnotes)

    indexes = [
        i for i, em in enumerate(eighthmetas)
        if get_fingersstate_type(em['fingersstate']) == 'melodic'][:lenght]

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