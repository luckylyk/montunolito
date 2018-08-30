from PyQt5 import QtGui, QtCore
import sys
from montunolito.core.solfege import SCALE_LENGTH
from montunolito.core.utils import remap_number


# poisitons scales
DIESE_SCALE = 0, 0, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6
BEMOLE_SCALE = 0, 1, 1, 2, 3, 3, 4, 4, 5, 6, 6, 7

STAFF_LINES_NUMBERS = 26
POSITIONS_COUNT = 54
MATCHERS = {m: [(m * 2) - i for i in range(1, 3)] for m in range(13)}
MATCHERS.update({m: [(m * 2) - i for i in range(2, 4)] for m in range(18, 28)})


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
            break
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
