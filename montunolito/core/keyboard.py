from .utils import remap_number, get_number_multiples, find_closer_number
from .solfege import SCALE_LENGTH, get_fingersstate_type


KEYBOARD_LENGHT = 88
HIGHER_NOTE_USED = 66
LOWER_NOTE_USED = 25
REFERENCE_STARTNOTE = 35


def is_melodic_keyboard_eighth(keyboard_eighth):
    return keyboard_eighth_length(keyboard_eighth) == 1


def is_harmonic_keyboard_eighth(keyboard_eighth):
    return keyboard_eighth_length(keyboard_eighth) > 1


def is_mute_keyboard_eighth(keyboard_eighth):
    return keyboard_eighth_length(keyboard_eighth) == 0


def keyboard_eighth_length(keyboard_eighth):
    return len(set(
        [remap_number(n, value=SCALE_LENGTH) for n in keyboard_eighth]))


def melodic_gap(note_array_1, note_array_2):
    note_array_1 = [n for n in note_array_1 if n is not None]
    note_array_2 = [n for n in note_array_2 if n is not None]
    if not all([note_array_1, note_array_2]):
        raise ValueError('cannot compare melodic gap with an empty array.')

    note_1 = remap_number(note_array_1[0], value=SCALE_LENGTH)
    note_2 = remap_number(note_array_2[0], value=SCALE_LENGTH)
    note_1, note_2 = max([note_1, note_2]), min([note_1, note_2])
    value_1 = abs(note_1 - note_2)
    value_2 = abs((note_2 + SCALE_LENGTH) - note_1)
    return min([value_1, value_2])


def convert_eighthnote_to_keyboard_eighth(eighthnote, keyboard_sequence=None):
    keyboard_sequence = keyboard_sequence or []
    melodic_keyboard_eighth = [
        kbs for kbs in keyboard_sequence if is_melodic_keyboard_eighth(kbs)]
    harmonic_keyboard_eighth = [
        kbs for kbs in keyboard_sequence if is_harmonic_keyboard_eighth(kbs)]

    keyboard_eighth = [
        e for e in keyboard_sequence if not is_mute_keyboard_eighth(e)]
    keyboard_eighth = keyboard_eighth[-1] if keyboard_eighth else None
    reference_melodic_keyboard_eighth = (
        melodic_keyboard_eighth[-1] if melodic_keyboard_eighth else None)
    reference_harmonic_keyboard_eighth = (
        harmonic_keyboard_eighth[-1] if harmonic_keyboard_eighth else None)

    if get_fingersstate_type(eighthnote) == 'melodic':
        generated_kbnotes = generate_melodic_keyboard_eighth(
            eighthnote=eighthnote,
            reference_keyboard_eighth=reference_melodic_keyboard_eighth)

    elif get_fingersstate_type(eighthnote) == 'harmonic':
        generated_kbnotes = generate_harmonic_keyboard_eighth(
            eighthnote=eighthnote,
            reference_keyboard_eighth=keyboard_eighth,
            reference_melodic_keyboard_eighth=reference_melodic_keyboard_eighth,
            reference_harmonic_keyboard_eighth=reference_harmonic_keyboard_eighth)

    else:
        generated_kbnotes = []
    return sorted(list(set(generated_kbnotes)))


def generate_melodic_keyboard_eighth(
        eighthnote, reference_keyboard_eighth=None):
    notes = [note for note in eighthnote if note is not None]
    pressed_fingers_number = len(notes) + 1
    notes = get_number_multiples(
        notes[0], base=SCALE_LENGTH, maximum=KEYBOARD_LENGHT)
    keys = []

    if not reference_keyboard_eighth:
        for note in sorted(notes, reverse=True):
            if note < HIGHER_NOTE_USED:
                keys.append(note)
            if len(keys) == pressed_fingers_number:
                return sorted(keys)

    if pressed_fingers_number == len(reference_keyboard_eighth):
        for key in reference_keyboard_eighth:
            keys.append(
                find_closer_number(
                    reference=key,
                    array=notes,
                    clamp=KEYBOARD_LENGHT))
        return clamp_keyboard_heighth(sorted(keys), reference_keyboard_eighth)

    startindex = 0
    for note in notes:
        if notes[startindex] < reference_keyboard_eighth[0]:
            startindex += 1
        else:
            break

    if pressed_fingers_number == 2 and len(reference_keyboard_eighth) == 3:
        notes = sorted(notes[startindex:startindex+2])
    else:
        notes = sorted(notes[startindex-1:startindex+2])
    return clamp_keyboard_heighth(notes, reference_keyboard_eighth)


def eighthnote_lenght(eighthnote):
    return len([n for n in eighthnote if n is not None])


def generate_harmonic_keyboard_eighth(
        eighthnote, reference_keyboard_eighth=None,
        reference_melodic_keyboard_eighth=None,
        reference_harmonic_keyboard_eighth=None):

    notes = [note for note in eighthnote if note is not None]

    conditions = (
        reference_melodic_keyboard_eighth or reference_harmonic_keyboard_eighth)
    if not conditions:
        return generate_first_harmonic_keys(notes)

    keys = []
    multiples = sorted([
        number for note in notes for number in get_number_multiples(
            number=note, base=SCALE_LENGTH, maximum=KEYBOARD_LENGHT)])

    conditions = (
        (reference_melodic_keyboard_eighth and
        not reference_harmonic_keyboard_eighth) or
        (reference_keyboard_eighth and
         is_melodic_keyboard_eighth(reference_keyboard_eighth)))

    if conditions:
        for number in sorted(multiples):
            check_notes = [remap_number(k, value=SCALE_LENGTH) for k in keys]
            if number > sorted(reference_melodic_keyboard_eighth)[0]:
                if remap_number(number, value=SCALE_LENGTH) not in check_notes:
                    keys.extend([number, number + SCALE_LENGTH])
        return sorted(keys)

    if reference_melodic_keyboard_eighth is not None:
        multiples = [
            n for n in multiples if n > reference_melodic_keyboard_eighth[0]]

    reference_length = len(set([
        remap_number(n, value=SCALE_LENGTH)
        for n in reference_harmonic_keyboard_eighth]))
    if len(notes) != reference_length:
        return generate_first_harmonic_keys(notes)

    for key in reference_harmonic_keyboard_eighth:
        array = [n for n in multiples if n not in keys]
        keys.append(
            find_closer_number(
                reference=key,
                array=array,
                clamp=KEYBOARD_LENGHT))
        if len(keys) == len(notes):
            break
    return sorted([n for key in keys for n in (key, key + SCALE_LENGTH)])


def generate_first_harmonic_keys(notes):
    keys = []
    for note in notes:
        multiples = get_number_multiples(
            number=note, base=SCALE_LENGTH, maximum=KEYBOARD_LENGHT)
        number = find_closer_number(
            reference=REFERENCE_STARTNOTE,
            array=multiples,
            clamp=KEYBOARD_LENGHT)
        keys.extend([number, number + SCALE_LENGTH])
    return sorted(keys)


def clamp_keyboard_heighth(keyboard_eight, reference_keyboard_eight):
    if not melodic_gap(reference_keyboard_eight, keyboard_eight) >= 4:
        return keyboard_eight

    if keyboard_eight[-1] > HIGHER_NOTE_USED:
        keyboard_eight = [n - SCALE_LENGTH for n in keyboard_eight]
    elif keyboard_eight[0] < LOWER_NOTE_USED:
        keyboard_eight = [n + SCALE_LENGTH for n in keyboard_eight]

    return keyboard_eight