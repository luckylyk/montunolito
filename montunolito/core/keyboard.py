from .utils import remap_number, get_number_multiples, find_closer_number
from .solfege import SCALE_LENGHT, get_fingersstate_type


KEYBOARD_LENGHT = 88
HIGHER_NOTE_USED = 71
LOWER_NOTE_USED = 27


def is_mute_keysstate(keysstate):
    return not sum(keysstate)


def is_melodic_keysstate(keysstate):
    return keysstate_lenght(keysstate) == 1


def is_chord_keysstate(keysstate):
    if is_mute_keysstate(keysstate) or is_melodic_keysstate(keysstate):
        return False
    return True


def keysstate_pressed_fingers_lenght(keysstate):
    return len([s for s in keysstate if s == 1])


def convert_keysstate_to_notearray(keysstate):
    return [
        remap_number(i, value=SCALE_LENGHT)
        for i in keysstate_indexes(keysstate)]


def keysstate_indexes(keysstate):
    return [i for i, s in enumerate(keysstate) if s == 1]


def keysstate_lenght(keysstate):
    return len(set(convert_keysstate_to_notearray(keysstate)))


def convert_eightnotes_to_keysstates(eightnotes, keysstates=None):
    melodic_keysstates = [ks for ks in keysstates if is_melodic_keysstate(ks)]
    chord_keysstates = [ks for ks in keysstates if is_chord_keysstate(ks)]


def convert_keys_to_keystate(keys):
    return [1 if key in keys else 0 for key in range(KEYBOARD_LENGHT)]


def generate_melodic_keys(eightnote, reference_keysstate=None):
    assert get_fingersstate_type(eightnote) == 'melodic', \
        '{} must be melodic'.format(eightnote)
    if reference_keysstate is not None:
        assert is_melodic_keysstate(reference_keysstate)

    notes = [note for note in eightnote if note]
    pressed_fingers_number = len(notes) + 1
    notes = get_number_multiples(
        notes[0], base=SCALE_LENGHT, maximum=KEYBOARD_LENGHT)
    final_notes = []

    if not reference_keysstate:
        for note in sorted(notes, reverse=True):
            if note < HIGHER_NOTE_USED:
                final_notes.append(note)
            if len(final_notes) == pressed_fingers_number:
                return sorted(final_notes)

    reference_pressed_fingers_number = keysstate_pressed_fingers_lenght(
        reference_keysstate)

    if pressed_fingers_number == reference_pressed_fingers_number:
        for index in keysstate_indexes(reference_keysstate):
            final_notes.append(
                find_closer_number(
                    reference=index,
                    array=notes,
                    clamp=KEYBOARD_LENGHT))
        return sorted(final_notes)







