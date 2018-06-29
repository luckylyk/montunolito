from .utils import remap_number, get_number_multiples, find_closer_number
from .solfege import SCALE_LENGHT, get_fingersstate_type


KEYBOARD_LENGHT = 88
HIGHER_NOTE_USED = 71
LOWER_NOTE_USED = 27
REFERENCE_STARTNOTE = 35


def is_melodic_eighthkbstate(eighthkbstate):
    return eighthkbstate_lenght(eighthkbstate) == 1


def is_harmonic_eighthkbstate(eighthkbstate):
    return eighthkbstate_lenght(eighthkbstate) > 1


def eighthkbstate_lenght(eighthkbstate):
    return len(set(
        [remap_number(n, value=SCALE_LENGHT) for n in eighthkbstate]))


def convert_eighthnote_to_eighthkbstate(eighthnote, eighthkbstates=None):
    eighthkbstates = eighthkbstates or []
    melodic_eighthkbstate = [
        kbs for kbs in eighthkbstates if is_melodic_eighthkbstate(kbs)]
    harmonic_eighthkbstate = [
        kbs for kbs in eighthkbstates if is_harmonic_eighthkbstate(kbs)]

    reference_melodic_eighthkbstate = (
        melodic_eighthkbstate[0] if melodic_eighthkbstate else None)
    reference_harmonic_eighthkbstate = (
        harmonic_eighthkbstate[0] if harmonic_eighthkbstate else None)

    if get_fingersstate_type(eighthnote) == 'melodic':
        return generate_melodic_eighthkbstate(
            eighthnote=eighthnote,
            reference_eighthkbstate=reference_melodic_eighthkbstate)

    elif get_fingersstate_type(eighthnote) == 'harmonic':
        return generate_harmonic_eighthkbstate(
            eighthnote=eighthnote,
            reference_melodic_eighthkbstate=reference_melodic_eighthkbstate,
            reference_harmonic_eighthkbstate=reference_harmonic_eighthkbstate)

    else: # is mute
        return []


def generate_melodic_eighthkbstate(eighthnote, reference_eighthkbstate=None):
    notes = [note for note in eighthnote if note is not None]
    pressed_fingers_number = len(notes) + 1
    notes = get_number_multiples(
        notes[0], base=SCALE_LENGHT, maximum=KEYBOARD_LENGHT)
    keys = []

    if not reference_eighthkbstate:
        for note in sorted(notes, reverse=True):
            if note < HIGHER_NOTE_USED:
                keys.append(note)
            if len(keys) == pressed_fingers_number:
                return sorted(keys)

    if pressed_fingers_number == len(reference_eighthkbstate):
        for key in reference_eighthkbstate:
            keys.append(
                find_closer_number(
                    reference=key,
                    array=notes,
                    clamp=KEYBOARD_LENGHT))
        return sorted(keys)

    startindex = 0
    for note in notes:
        if notes[startindex] < reference_eighthkbstate[0]:
            startindex += 1
        else:
            break

    if pressed_fingers_number == 2 and len(reference_eighthkbstate) == 3:
        return notes[startindex:startindex+2]
    else:
        return notes[startindex-1:startindex+2]


def eighthnote_lenght(eighthnote):
    return len([n for n in eighthnote if n is not None])


def generate_harmonic_eighthkbstate(
        eighthnote, reference_melodic_eighthkbstate=None,
        reference_harmonic_eighthkbstate=None):

    notes = [note for note in eighthnote if note is not None]

    conditions = (
        reference_melodic_eighthkbstate or reference_harmonic_eighthkbstate)
    if not conditions:
        return generate_first_harmonic_keys(notes)

    keys = []
    multiples = sorted([
        number for note in notes for number in get_number_multiples(
            number=note, base=SCALE_LENGHT, maximum=KEYBOARD_LENGHT)])

    conditions = (
        reference_melodic_eighthkbstate and
        not reference_harmonic_eighthkbstate)
    if conditions:
        for number in multiples:
            check_notes = [remap_number(k, value=12) for k in keys]
            if number > reference_melodic_eighthkbstate[0]:
                if remap_number(number, value=12) not in check_notes:
                    keys.extend([number, number + 12])
        return sorted(keys)

    if reference_melodic_eighthkbstate:
        multiples = [
            n for n in multiples if n > reference_melodic_eighthkbstate[0]]

    reference_lenght = len(set([
        remap_number(n, value=12) for n in reference_harmonic_eighthkbstate]))
    if len(notes) != reference_lenght:
        return generate_first_harmonic_keys(notes)

    for key in reference_harmonic_eighthkbstate:
        array = [n for n in multiples if n not in keys]
        keys.append(
            find_closer_number(
                reference=key,
                array=array,
                clamp=KEYBOARD_LENGHT))
        if len(keys) == len(notes):
            break
    return sorted([n for key in keys for n in (key, key + 12)])


def generate_first_harmonic_keys(notes):
    keys = []
    for note in notes:
        multiples = get_number_multiples(
            number=note, base=SCALE_LENGHT, maximum=KEYBOARD_LENGHT)
        number = find_closer_number(
            reference=REFERENCE_STARTNOTE,
            array=multiples,
            clamp=KEYBOARD_LENGHT)
        keys.extend([number, number + 12])
    return sorted(keys)