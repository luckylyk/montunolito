import sys
import traceback
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from montunolito.converters.musicxml.convert import convert_to_musicxml
from montunolito.core.iterators import montuno_generator
from montunolito.patterns import PATTERNS
from montunolito.core.keyboard import convert_eighthnote_to_eighthkbstate


def get_pre_registered_eighthkbnotes():
    a = [31, 43, 55]
    b = [34, 46]
    c = [38, 50]
    d = [34, 38, 46, 50]

    return [
        a, b, c, a, [], d, [], a,  [], d, [], a, [], d, a, a]


def get_chromatic_eighthkbnotes():
    return [[n] for n in range(35, 75)]


def convert_to_eighthkbnotes(eighthnotes):
    eighthkbstates=[]
    for eighthnote in eighthnotes:
        eighthkbstate = convert_eighthnote_to_eighthkbstate(
            eighthnote=eighthnote, 
            eighthkbstates=eighthkbstates)
        eighthkbstates.append(eighthkbstate)
    return eighthkbstates


def get_generated_eighthkbnotes():
    a = [1, None, None, None, 1]
    b = [None, 4, None, None, None]
    c = [None, None, 8, None , None]
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
        None, None, None, None, None, 
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
        None, None, None, None, None, None, None, None, None],
}



def get_full_generated_eighthkbnotes():

    montunos = montuno_generator(
        pattern=PATTERNS['montuno'],
        chord_grid=CHORDS['lejourdupoisson'],
        tonality=3)

    eighthkbnotes = []
    for _ in range(8*8*4):
        eighthkbnote = next(montunos)
        eighthkbnotes.append(eighthkbnote)
    return eighthkbnotes


if __name__ == "__main__":

    eighthkbnotes = get_full_generated_eighthkbnotes()
    # (
    #     get_pre_registered_eighthkbnotes() +
    #     get_generated_eighthkbnotes() +
    #     get_full_generated_eighthkbnotes())

    xmlcontent = convert_to_musicxml(eighthkbnotes, tempo=600)
    fileoutput = r'C:\Users\zil\Desktop\xmltest\montuno.xml'
    with open(fileoutput, 'w') as myfile:
        myfile.write(xmlcontent)