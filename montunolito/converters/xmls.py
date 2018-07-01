
import os
from montunolito.core.solfege import NOTES, SCALE_LENGTH
from montunolito.core.utils import remap_number


def read_ressource_xml_file(filename):
    filename = os.path.join(RESSOURCES_PATH, filename)
    with open(filename, "r") as my_xml:
        return my_xml.read()

RESSOURCES_PATH = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), 'xml')
RESSOURCES = {
    filename.strip(".xml") : read_ressource_xml_file(filename)
    for filename in os.listdir(RESSOURCES_PATH)}

POSITIONS_X = ("86", "146", "205", "265", "324", "383", "442", "502")

def generate_measure(eighthkbnotes):
    assert len(eighthkbnotes) == 8

    xml_notes = []
    for index, eighthkbnote in enumerate(eighthkbnotes):
        if not eighthkbnote:
            note = RESSOURCES['emptyeighth'].format(posx=POSITIONS_X[index])
            xml_notes.append(note)
            continue

        for i, note in index(eighthkbnote):
            remapped_note = remap_number(note, value=SCALE_LENGTH)
            notename = NOTES[remapped_note]
            pitch = (note - remapped_note) / SCALE_LENGTH


def get_beam_continuity(index, eighthkbnotes):
    if index in (0, 4) or not eighthkbnotes[index - 1]:
        return 'begin'
    elif index in (3, 7) or eighthkbnotes[index + 1]:
        return 'end'
    else:
        return 'continue'
