from PyQt5 import QtGui, QtCore
import sys
from montunolito.core.solfege import SCALE_LENGTH
from montunolito.core.utils import remap_number, past_and_futur


# poisitons scales
DIESE_SCALE = 0, 0, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6
BEMOLE_SCALE = 0, 1, 1, 2, 3, 3, 4, 4, 5, 6, 6, 7
ALTERED_INDEXES = 1, 4, 6, 9, 11

STAFF_LINES_NUMBERS = 26
POSITIONS_COUNT = 54
MATCHERS = {m: [(m * 2) - i for i in range(1, 3)] for m in range(13)}
MATCHERS.update({m: [(m * 2) - i for i in range(2, 4)] for m in range(18, 28)})
BEAM_LENGTH_FACTOR = .15
STRAIGHT_CONNECTION_FACTOR = .05


def get_staff_lines(rect, start=0, end=STAFF_LINES_NUMBERS + 1):
    path = QtGui.QPainterPath()
    space = rect.height() / (STAFF_LINES_NUMBERS + 1)
    bottom = rect.bottom() - (space * start)
    for _ in range(start, end):
        path.moveTo(rect.left(), bottom)
        path.lineTo(rect.right(), bottom)
        bottom -= space
    return path


def get_standard_staff_lines(rect):
    return get_staff_lines(rect, 13, 18)


def get_additional_staff_lines(rect, position):
    if position > 23 and position < 35:
        return None
    for line, positions in MATCHERS.items():
        if position in positions:
            if position <= 23:
                return get_staff_lines(rect, line, 13)
            return get_staff_lines(rect, 18, line)


def get_top_from_position(rect, position):
    position = POSITIONS_COUNT - position
    return (rect.height() / POSITIONS_COUNT) * (position - 1)


def get_note_position(note, display_scale=None):
    display_scale = display_scale or BEMOLE_SCALE
    offset = (note // SCALE_LENGTH) * 7
    line = display_scale[remap_number(note, SCALE_LENGTH)]
    return offset + line


def get_beams_directions(sequence):
    directions = []
    positions_averages = []
    for _, notes, next_notes in past_and_futur(sequence):
        if not notes:
            directions.append(None)
            positions_averages = []
            continue

        positions_averages.append(
            sum([get_note_position(n) for n in notes]) / len(notes))
        if not next_notes:
            averages_count = len(positions_averages)
            average = sum([a for a in positions_averages]) / averages_count
            for _ in range(averages_count):
                directions.append('up' if average < 29 else 'down')
    return directions


def get_beam_start_end(rect, notes):
    first_note = get_note_position(notes[0])
    last_note = get_note_position(notes[-1])
    start = get_top_from_position(rect, first_note)
    end = get_top_from_position(rect, last_note)
    return start, end


def get_beam_bottom(rect, notes, up=True):
    start, end = get_beam_start_end(rect, notes)
    return start if up else end


def get_beam_top(rect, notes, up=True):
    start, end = get_beam_start_end(rect, notes)
    offset = rect.height() * BEAM_LENGTH_FACTOR
    return end - offset if up else start + offset


def get_beams_tops(rect, sequence, directions):
    tops = []
    tops_tmp = []
    iterator = zip(past_and_futur(sequence), directions)
    straight = rect.height() * STRAIGHT_CONNECTION_FACTOR
    for (_, notes, next_notes), direction in iterator:
        if not notes:
            tops.append(None)
            tops_tmp = []
            continue

        is_up = direction == 'up'
        tops_tmp.append(get_beam_top(rect, notes, up=is_up))
        if not next_notes:
            if abs(tops_tmp[0] - tops_tmp[-1]) < straight:
                top = min(tops_tmp) if is_up else max(tops_tmp)
                tops.extend([top for _ in range(len(tops_tmp))])
            else:
                tops.extend(get_average_beam_tops(tops_tmp))
            tops_tmp = []
    return tops


def get_average_beam_tops(tops):
    if len(tops) == 1:
        return tops

    start = tops[0]
    end = tops[-1]
    spacer = (start - end) / (len(tops) - 1)

    if len(tops) == 2:
        return [tops[0] - (spacer * .3), tops[-1] + (spacer * .3)]

    highest = min(tops)
    tops = [highest - (spacer * i) for i in range(len(tops))]
    return tops


def is_altered(note):
    return remap_number(note, SCALE_LENGTH) in ALTERED_INDEXES
