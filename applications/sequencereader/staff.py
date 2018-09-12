from PyQt5 import QtGui, QtCore
from montunolito.core.solfege import SCALE_LENGTH
from montunolito.core.utils import remap_number, past_and_futur
from sequencereader.rules import (
    STAFF_LINES_NUMBERS, POSITIONS_COUNT, FLAT_SCALE, get_matching_line,
    get_note_position)

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


def get_extra_stafflines_path(
        top, height, radius, centers, positions, up=False):

    centers = reversed(centers) if up else centers
    positions = reversed(positions) if up else positions
    reference_line = 18 if up else 13

    path = QtGui.QPainterPath()
    rect = QtCore.QRectF()
    rect.setTop(top)
    rect.setHeight(height)

    previous_center = None
    start_line = None
    use_double_line = False
    need_draw = False
    for center, position in zip(centers, positions):
        if position < 35 if up else position > 23:
            if start_line:
                begin = min([start_line, reference_line])
                end = max([start_line, reference_line])
                path.addPath(get_staff_lines(rect, begin, end))
                need_draw = False
            break

        need_draw = True
        if previous_center is None:
            previous_center = center
            left = center.x() + radius if up else center.x() - radius
            right = center.x() - radius if up else center.x() + radius
            rect.setLeft(left)
            rect.setRight(right)

        if not start_line:
            start_line = get_matching_line(position)

        if center.x() != previous_center.x() and use_double_line is False:
            end_line = get_matching_line(position)
            begin = min([start_line, end_line])
            end = max([start_line, end_line])
            path.addPath(get_staff_lines(rect, begin, end))
            if center.x() > previous_center.x():
                right = center.x() - radius if up else center.x() + radius
                rect.setRight(right)
            else:
                left = center.x() + radius if up else center.x() - radius
                rect.setLeft(left)
            use_double_line = True
            start_line = end_line

    if need_draw:
        path.addPath(get_staff_lines(rect, start_line, 13))
    return path


def get_standard_staff_lines(rect):
    return get_staff_lines(rect, 13, 18)


def get_top_from_position(height, position):
    position = POSITIONS_COUNT - position
    return (height / POSITIONS_COUNT) * (position - 1)


def get_beam_start_end(height, notes, display_scale):
    first_note = get_note_position(notes[0], display_scale)
    last_note = get_note_position(notes[-1], display_scale)
    start = get_top_from_position(height, first_note)
    end = get_top_from_position(height, last_note)
    return start, end


def get_beam_bottom(height, notes, display_scale, up=True):
    start, end = get_beam_start_end(height, notes, display_scale)
    return start if up else end


def get_beam_top(height, notes, display_scale, up=True):
    start, end = get_beam_start_end(height, notes, display_scale)
    offset = height * BEAM_LENGTH_FACTOR
    return end - offset if up else start + offset


def get_beams_tops(height, sequence, directions, display_scale):
    tops = []
    tops_tmp = []
    iterator = zip(past_and_futur(sequence), directions)
    straight = height * STRAIGHT_CONNECTION_FACTOR
    for (_, notes, next_notes), direction in iterator:
        if not notes:
            tops.append(None)
            tops_tmp = []
            continue

        is_up = direction == 'up'
        tops_tmp.append(get_beam_top(height, notes, display_scale, up=is_up))
        if not next_notes:
            if abs(tops_tmp[0] - tops_tmp[-1]) < straight:
                top = min(tops_tmp) if is_up else max(tops_tmp)
                tops.extend([top for _ in range(len(tops_tmp))])
            else:
                tops.extend(get_average_beam_tops(tops_tmp, is_up))
            tops_tmp = []
    return tops


def get_average_beam_tops(tops, is_up):
    if len(tops) == 1:
        return tops

    start = tops[0]
    end = tops[-1]

    if len(tops) == 2:
        spacer = (start - end) / (len(tops) - 1)
        return [tops[0] - (spacer * .3), tops[-1] + (spacer * .3)]

    highest = min(tops) if is_up else max(tops)
    lowest = max(tops) if is_up else min(tops)
    offset = abs(highest - lowest) / 3
    highest = highest + offset if is_up else highest - offset
    lowest = highest - offset if is_up else highest + offset
    spacer = abs(highest - lowest) / (len(tops) - 1)
    tops = [highest + offset - (spacer * i) for i in range(len(tops))]
    return tops


def get_signature_centers(rect, signature):
    centers = []
    offset = rect.width() / (len(signature.positions) + 1)
    x = rect.left() + offset
    for position in signature.positions:
        y = rect.top() + get_top_from_position(rect.height(), position)
        centers.append(QtCore.QPoint(x, y))
        x += offset
    return centers

