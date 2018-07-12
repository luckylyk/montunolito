import sys
import os
import datetime

from montunolito.core.solfege import NOTES, SCALE_LENGTH
from montunolito.core.utils import (
    remap_number, split_array, set_array_lenght_multiple)

from .ressources import RESSOURCES


POSITIONS_X = ("86", "146", "205", "265", "324", "383", "442", "502")
BEAM_Y = {'up': 45, "down": -85}
PIANO_PART = {
    'id': 'P1',
    'partname': 'Piano',
    'instrumentname': 'Piano'}


def convert_to_musicxml(eighthkbnotes, tempo=None):
    header = RESSOURCES['header']
    identification = RESSOURCES['identification'].format(
        encoding_date=datetime.datetime.today().strftime("%Y-%m-%d"))
    default = RESSOURCES['default']
    parts = get_parts([PIANO_PART])
    measures = generate_measures(eighthkbnotes, tempo=tempo)
    score = RESSOURCES['score'].format(
        identification=identification,
        default=default,
        parts=parts,
        measures=measures)

    musicxml = header + score
    return musicxml


def get_parts(parts):
    scoreparts = ''
    for part in parts:
        scoreparts += RESSOURCES['scorepart'].format(**part)
    return RESSOURCES['partlist'].format(measure=scoreparts)


def generate_measures(eighthkbnotes, tempo=None):
    eighthkbnotes = set_array_lenght_multiple(
        array=eighthkbnotes, multiple=8, default=[])
    eighthkbnotes_measures = split_array(eighthkbnotes, lenght=8)

    measures = ''
    for i, eighthkbnotes_measure in enumerate(eighthkbnotes_measures):
        measures += generate_measure(
            eighthkbnotes_measure, measure_number=i+1, tempo=tempo)
        tempo = None
    part = RESSOURCES['part'].format(id=PIANO_PART['id'], content=measures)
    return part


def generate_measure(eighthkbnotes, measure_number=1, tempo=None):
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
            notename = NOTES[remapped_note][0]
            octave = (note - remap_number(note - 3, value=SCALE_LENGTH)) // SCALE_LENGTH + 1
            if i == 0:
                chord = ''
                continuity = get_beam_continuity(index, eighthkbnotes)
                beam = RESSOURCES['beam'].format(continuity=continuity)
                if continuity == 'begin':
                    orientation = 'up' if note > 40 else 'down'
            else:
                chord = RESSOURCES['chord']
                beam = ''
            stem = RESSOURCES['stem'].format(
                posy=BEAM_Y[orientation], orientation=orientation)
            alter = RESSOURCES['alter'] if len(NOTES[remapped_note]) > 1 else ''

            notesxml.append(
                RESSOURCES['note'].format(
                    posx=POSITIONS_X[index],
                    chord=chord,
                    notename=notename,
                    octave=octave,
                    alter=alter,
                    beam=beam,
                    stem=stem))

    notesxml = ''.join(notesxml)
    header = RESSOURCES['measureheader'].format(tempo=tempo) if tempo else ''
    measure = RESSOURCES['measure'].format(
        measureheader=header, number=measure_number, notes=notesxml)

    return measure


def get_beam_continuity(index, eighthkbnotes):
    if index in (0, 4) or not eighthkbnotes[index - 1]:
        return 'begin'
    elif index in (3, 7) or not eighthkbnotes[index + 1]:
        return 'end'
    else:
        return 'continue'


