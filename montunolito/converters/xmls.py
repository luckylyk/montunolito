import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from montunolito.core.solfege import NOTES, SCALE_LENGTH
from montunolito.core.utils import remap_number


def read_ressource_xml_file(filename):
    filename = os.path.join(RESSOURCES_PATH, filename)
    with open(filename, "r") as my_xml:
        return my_xml.read()

POSITIONS_X = ("86", "146", "205", "265", "324", "383", "442", "502")
BEAM_Y = {'up': 45, "down": -85}
RESSOURCES_PATH = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), 'xml')
RESSOURCES = {
    str(filename[:-4]) : read_ressource_xml_file(filename)
    for filename in os.listdir(RESSOURCES_PATH)}

print (RESSOURCES.keys())


def generate_measure(eighthkbnotes, tempo=None):
    assert len(eighthkbnotes) == 8

    notesxml = []
    orientation = None
    for index, eighthkbnote in enumerate(eighthkbnotes):
        if not eighthkbnote:
            note = RESSOURCES['emptyeighth'].format(posx=POSITIONS_X[index])
            notesxml.append(note)
            continue

        for i, note in enumerate(eighthkbnote):
            remapped_note = remap_number(note, value=SCALE_LENGTH)
            notename = NOTES[remapped_note]
            octave = (note - remapped_note) / SCALE_LENGTH
            if i == 0:
                continuity = get_beam_continuity(index, eighthkbnotes)
                beam = RESSOURCES['beam'].format(continuity=continuity)
                if continuity == 'begin':
                    orientation = 'up' if note > 40 else 'down'
            else:
                beam = ""
            stem = RESSOURCES['stem'].format(
                posy=BEAM_Y[orientation], orientation=orientation)

            notesxml.append(
                RESSOURCES['note'].format(
                    posx=POSITIONS_X[index],
                    notename=notename,
                    octave=octave,
                    beam=beam,
                    stem=stem))

    notesxml = ''.join(notesxml)
    header = RESSOURCES['measureheader'].format(tempo=tempo) if tempo else ''
    measure = RESSOURCES['measure'].format(measureheader=header, notes=notesxml)

    return measure



def get_beam_continuity(index, eighthkbnotes):
    if index in (0, 4) or not eighthkbnotes[index - 1]:
        return 'begin'
    elif index in (3, 7) or eighthkbnotes[index + 1]:
        return 'end'
    else:
        return 'continue'


if __name__ == "__main__":
    eighthkbnotes = [
        [35, 47, 59],
        [39, 51, 63],
        [41, 53, 65],
        [35, 47, 59],
        [],
        [37, 41, 49, 53],
        [],
        [37, 41, 49, 53]]

    print(generate_measure(eighthkbnotes, tempo=120))