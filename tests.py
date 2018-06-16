import sys
sys.path.insert(0, r"D:\EclipseWorkspaces\csse120\myPyRessource\GitHub") # put you local repo

from montunolito.data import *


def unit_test_melody():
    print("MELODY UNIT TEST -- > started")

    print("###################")
    print("#scales generation#")
    print("###################")
    def names(notearray):
        return [NOTES[n] for n in notearray]

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
    assert generate_arpegic_melody(chord_array[:], chord_array_destination[:], 8) in ([4, 3, 0, 10, 7, 4, 3, 5], [4, 3, 0, 10, 7, 4, 3, 10], [4, 7, 10, 0, 3, 4, 7, 5], [4, 7, 10, 0, 3, 4, 7, 10])
    assert generate_arpegic_melody(chord_array[:], chord_array_destination[:], 8) in ([4, 3, 0, 10, 7, 4, 3, 5], [4, 3, 0, 10, 7, 4, 3, 10], [4, 7, 10, 0, 3, 4, 7, 5], [4, 7, 10, 0, 3, 4, 7, 10])
    assert generate_arpegic_melody(chord_array[:], chord_array_destination[:], 8) in ([4, 3, 0, 10, 7, 4, 3, 5], [4, 3, 0, 10, 7, 4, 3, 10], [4, 7, 10, 0, 3, 4, 7, 5], [4, 7, 10, 0, 3, 4, 7, 10])
    assert generate_arpegic_melody(chord_array[:], chord_array_destination[:], 8) in ([4, 3, 0, 10, 7, 4, 3, 5], [4, 3, 0, 10, 7, 4, 3, 10], [4, 7, 10, 0, 3, 4, 7, 5], [4, 7, 10, 0, 3, 4, 7, 10])

    # chromatic
    chord_array = [4, 7, 10, 0, 3]
    chord_array_destination = [6, 9, 1, 0, 3]

    melody = generate_chromatic_melody(
        reference_note=5, 
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        length=3)
    assert melody == [4, 5, 6]

    melody = generate_chromatic_melody(
        reference_note=5,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        length=4)
    assert melody == [4, 3, 2, 1]

    melody = generate_chromatic_melody(
        reference_note=7,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        length=4) 
    assert melody == [4, 3, 2, 1]

    melody = generate_chromatic_melody(
        reference_note=11,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        length=4)
    assert melody is None

    # diatonic
    reference_note = 4
    chord_array = [4, 7, 10, 0, 3]
    chord_array_destination = [6, 9, 1, 0, 3]
    scale = [4, 6, 7, 8, 10, 0, 3]
    melody_length = 3
    melody = generate_diatonic_melody(
        reference_note=reference_note,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        scale=scale[:],
        length=melody_length)
    assert melody == [4, 6, 7]

    reference_note = 10
    chord_array = [4, 7, 10, 0, 3]
    chord_array_destination = [6, 9, 1, 0, 3]
    scale = [4, 6, 7, 8, 10, 0, 3]
    melody_length = 3
    melody = generate_diatonic_melody(
        reference_note=reference_note,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        scale=scale[:],
        length=melody_length)
    assert melody == [10, 0, 3]

    reference_note = 10
    chord_array = [4, 7, 10, 0, 3]
    chord_array_destination = [6, 9, 1, 0, 3]
    scale = [4, 6, 7, 8, 10, 0, 3]
    melody_length = 5
    melody = generate_diatonic_melody(
        reference_note=reference_note,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        scale=scale[:],
        length=melody_length)
    assert melody == [10, 0, 3, 4, 6]

    reference_note = 8
    chord_array = [4, 7, 10, 0, 3]
    chord_array_destination = [6, 7, 1, 0, 3]
    scale = [4, 6, 7, 8, 10, 0, 3]
    melody_length = 8
    melody = generate_diatonic_melody(
        reference_note=reference_note,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        scale=scale[:],
        length=melody_length)
    assert melody == [7, 8, 10, 0, 3, 4, 6, 7]

    reference_note = 4
    chord_array = [4, 7, 10, 0, 3]
    chord_array_destination = [6, 7, 1, 0, 3]
    scale = [4, 6, 7, 8, 10, 0, 3]
    melody_length = 4
    melody = generate_diatonic_melody(
        reference_note=reference_note,
        chord_array=chord_array[:],
        chord_array_destination=chord_array_destination[:],
        scale=scale[:],
        length=melody_length)
    assert melody is None

    print("MELODY UNIT TEST -- > finished")


def unit_test_math():
    print("MATH UTILS UNIT TEST -- > started")

    print("########")
    print("#choose#")
    print("########")
    assert choose({True: 3, False: 1}) in (False, True)
    assert choose({True: 3, False: 1}) in (False, True)
    assert choose({True: 3, False: 1}) in (False, True)
    assert choose({True: 3, False: 1}) in (False, True)

    assert choose({"lionel": 0, "chloe": 2, "mani": 0, "nico": 5}) in ("chloe", "nico")
    assert choose({"lionel": 0, "chloe": 2, "mani": 0, "nico": 5}) in ("chloe", "nico")
    assert choose({"lionel": 0, "chloe": 2, "mani": 0, "nico": 5}) in ("chloe", "nico")
    assert choose({"lionel": 0, "chloe": 2, "mani": 0, "nico": 5}) in ("chloe", "nico")
    assert choose({"lionel": 0, "chloe": 2, "mani": 0, "nico": 5}) in ("chloe", "nico")

    assert choose({"lionel": 0, "chloe": 0, "mani": 5, "nico": 0}) is "mani"
    assert choose({"lionel": 0, "chloe": 0, "mani": 5, "nico": 0}) is "mani"
    assert choose({"lionel": 0, "chloe": 0, "mani": 5, "nico": 0}) is "mani"
    assert choose({"lionel": 0, "chloe": 0, "mani": 5, "nico": 0}) is "mani"

    raise_ = False
    try:
        choose({"lionel": 0, "chloe": 0, "mani": 0, "nico": 0})
    except IndexError:
        raise_ = True
    assert raise_ is True
    del raise_
    print()

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

    print("##############")
    print("#offset_array#")
    print("##############")
    assert offset_array([6, 5, 4, 3, 1], 1) == [5, 4, 3, 1, 6]
    assert offset_array([6, 5, 4, 3, 1], 2) == [4, 3, 1, 6, 5]
    print()


    print("MATH UTILS UNIT TEST -- > finished")
if __name__ == '__main__':
    unit_test_math()
    unit_test_melody()