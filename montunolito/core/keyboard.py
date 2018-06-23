from .utils import remap_number


def is_mute_keysstate(keysstate):
    return not sum(keysstate)


def is_melodic_keysstate(keysstate):
    notes = set(convert_keysstate_to_notearray(keysstate))
    return len(notes) == 1


def is_chord_keysstate(keysstate):
    if is_mute_keysstate(keysstate) or is_melodic_keysstate(keysstate):
        return False
    return True


def convert_keysstate_to_notearray(keysstate):
    return [remap_number(i, value=12) for i, ks in enumerate(keysstate) if ks]


def get_corresponding_keyboard_indexes(number): # write tests
    number = remap_number(number, value=12)
    indexes = []
    while number <= 64:
        indexes.append(number)
        number += 12
    return indexes


def convert_eightnotes_to_keysstates(eightnotes, keysstates=None):
    keysstates = keysstates or []
    melodic_keysstates = [ks for ks in keysstates if is_melodic_keysstate(ks)]
    chord_keysstates = [ks for ks in keysstates if is_chord_keysstate(ks)]

