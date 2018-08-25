import sys
import traceback
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from montunolito.converters.musicxml.convert import convert_to_musicxml
from montunolito.converters.midi.convert import convert_to_midi
from montunolito.core.iterators import montuno_generator
from montunolito.patterns import PATTERNS
from montunolito.core.keyboard import convert_eighthnote_to_keyboard_eighth
from montunolito.libs.jsonutils import json_to_pattern


def get_pre_registered_eighthkbnotes():
    a = [31, 43, 55]
    b = [34, 46]
    c = [38, 50]
    d = [34, 38, 46, 50]

    return [
        a, b, c, a, [], d, [], a, [], d, [], a, [], d, a, a]


def get_chromatic_eighthkbnotes():
    return [[n] for n in range(35, 75)]


def convert_to_eighthkbnotes(eighthnotes):
    keyboard_sequence = []
    for eighthnote in eighthnotes:
        keyboard_eighth = convert_eighthnote_to_keyboard_eighth(
            eighthnote=eighthnote,
            keyboard_sequence=keyboard_sequence)
        keyboard_sequence.append(keyboard_eighth)
    return keyboard_sequence


def get_generated_eighthkbnotes():
    a = [1, None, None, None, 1]
    b = [None, 4, None, None, None]
    c = [None, None, 8, None, None]
    d = [None, 4, None, 8, None]
    e = [None, None, None, None, None]

    eighthnotes = [a, b, c, a, e, d, e, a, e, d, e, a, e, d, a, a]
    converted = convert_to_eighthkbnotes(eighthnotes)
    print(converted)
    return converted


CHORDS = {
    'chacha': [
        {'degree': 0, 'name': 'Major'},
        None,
        None,
        None,
        {'degree': 5, 'name': 'Major'},
        None,
        None,
        None,
        {'degree': 7, 'name': 'M7'},
        None,
        None,
        None,
        {'degree': 5, 'name': 'Major'},
        None,
        None,
        None],

    '14541': [
        {'degree': 0, 'name': 'Minor'},
        None,
        None,
        {'degree': 5, 'name': 'Minor'},
        None,
        None,
        {'degree': 7, 'name': 'M7'},
        None,
        None,
        None,
        None,
        {'degree': 5, 'name': 'Minor'},
        None,
        None,
        {'degree': 0, 'name': 'Minor'},
        None],

    'lejourdupoisson': [
        {'degree': 0, 'name': 'm6'},
        None, None, None, None, None, None,
        {'degree': 10, 'name': 'M6'},
        None, None, None, None, None, None, None, 
        {'degree': 8, 'name': 'M6'},
        None, None, None, None, None, None, None,
        {'degree': 7, 'name': 'M7'},
        None, None, None, None, None, None, None,
        {'degree': 5, 'name': 'm6'},
        None, None, None, None, None, None, None,
        {'degree': 0, 'name': 'm7'},
        None, None, None, None, None, None, None,
        {'degree': 2, 'name': 'M7'},
        None, None, None, None, None, None, None,
        {'degree': 7, 'name': 'M7'},
        None, None, None, None, None, None, None, None],
}


def get_full_generated_eighthkbnotes():

    montunos = montuno_generator(
        pattern=load_pattern_json(),
        chord_grid=load_chord_json(),
        tonality=3)

    eighthkbnotes = []
    for _ in range(8*8*4):
        eighthkbnote = next(montunos)
        eighthkbnotes.append(eighthkbnote)
    return eighthkbnotes


def get_extreme_eighth_notes():
    return [[15, 88]] * 8


def load_chord_json():
    chord_file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'ressources', 'chord_30defebrero.json')
    with open(chord_file_path, 'r') as chord_file:
        return json.load(chord_file)


def load_pattern_json():
    chord_file_path = r"C:\Users\zil\calypso.json"
    with open(chord_file_path, 'r') as chord_file:
        return json_to_pattern(json.load(chord_file))


if __name__ == "__main__":

    eighthkbnotes = get_full_generated_eighthkbnotes()
    # (
    #     get_pre_registered_eighthkbnotes() +
    #     get_generated_eighthkbnotes() +
    #     get_full_generated_eighthkbnotes())

    fileoutput = r'C:\Users\zil\Desktop\xmltest\''
    xmlcontent = convert_to_musicxml(eighthkbnotes, tempo=600)
    midicontent = convert_to_midi(eighthkbnotes, tempo=100)

    with open(fileoutput + 'extreme.xml', 'w') as myfile:
        myfile.write(xmlcontent)

    with open(fileoutput + 'anatole2.mid', "wb") as output_file:
        midicontent.writeFile(output_file)


