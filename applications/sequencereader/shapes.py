from PyQt5 import QtGui, QtCore
import sys
from montunolito.core.solfege import SCALE_LENGTH
from montunolito.core.utils import remap_number


DIESE_SCALE = 0, 0, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6
BEMOLE_SCALE = 0, 1, 1, 2, 3, 3, 4, 4, 5, 6, 6, 7
NOTE_ELLIPSE_RADIUS = 4


def get_staff_lines(rect):
    path = QtGui.QPainterPath()
    space = rect.height() / 36
    top = rect.top() + (11 * space)
    for _ in range(5):
        path.moveTo(rect.left(), top)
        path.lineTo(rect.right(), top)
        top += space * 2
    return path


def get_measure_separator(rect, left=False):
    left = rect.left() if left else rect.right()
    space = rect.height() / 36
    top = rect.top() + (11 * space)
    bottom = rect.top() + (19 * space)
    path = QtGui.QPainterPath(QtCore.QPointF(rect.right(), top))
    path.lineTo(rect.right(), bottom)
    return path


def get_notes_paths(noterects, sequence):
    paths = []
    beam_bottoms = []
    for rect, notes in zip(noterects, sequence):
        if not notes:
            paths.append(get_eighth_rest(rect))
            continue
        points = get_notes_centers(rect, notes)
        for point in points:
            radius = rect.height() / 36
            paths.append(get_note_path(point, radius))
        beam_bottoms.append(QtCore.QPointF(rect.center().x(), points[0].y()))
    beam_path = QtGui.QPainterPath()
    beam_top = beam_bottoms[0].y() - 100
    for bottom in beam_bottoms:
        beam_path.moveTo(bottom)
        beam_path.lineTo(QtCore.QPointF(bottom.x(), beam_top))
    paths.append(beam_path)
    return paths


def get_note_path(point, radius):
    path = QtGui.QPainterPath()
    path.addEllipse(point, radius, radius * .8)
    return path


# 43 is firts line as Eb
# 56 is first line as F#
def get_space_multiplier(note, display_scale=None):
    display_scale = display_scale or BEMOLE_SCALE
    multiplier = (note // SCALE_LENGTH) - 1
    line = display_scale[remap_number(note, SCALE_LENGTH)]
    return (line + (multiplier * 6)) + 1


def get_notes_centers(noterect, notes, display_scale=None):
    space = noterect.height() / 36
    points = []
    previous_top = None
    for note in notes:
        multiplier = get_space_multiplier(note, display_scale)
        top = noterect.bottom() - (space * multiplier)
        difference = abs(top - previous_top) if previous_top else sys.maxsize
        left = noterect.left() if difference > space else noterect.right()
        previous_top = top
        points.append(QtCore.QPointF(left, top))
    return points


def get_eighth_rest(noterect):
    vpadding = noterect.height() * .35
    hpadding = noterect.width() * .1
    noterect = QtCore.QRectF(
        noterect.left() + hpadding,
        noterect.top() + (vpadding * .8),
        noterect.width() - (hpadding * 2),
        noterect.height() - (vpadding * 2))

    start_point = QtCore.QPointF(
        noterect.left() - round(noterect.width() / 2),
        noterect.top() + round(noterect.height() / 3))
    path = QtGui.QPainterPath(start_point)
    control_point = QtCore.QPointF(
        start_point.x() + (noterect.width() / 5),
        start_point.y() + round(noterect.height() / 8))
    control_point_2 = QtCore.QPointF(
        start_point.x() + noterect.width(),
        start_point.y() + round(noterect.height() / 10))
    end_point = QtCore.QPointF(
        noterect.right() + round(noterect.width() / 2),
        noterect.top() + round(noterect.height() / 4))
    path.cubicTo(control_point, control_point_2, end_point)
    path.lineTo(QtCore.QPointF(
        noterect.left(), noterect.bottom() - round(noterect.height() / 3)))
    path.lineTo(QtCore.QPointF(
        start_point.x() + round(noterect.width() / 3),
        noterect.bottom() - round(noterect.height() / 3)))
    path.lineTo(end_point)
    control_point = QtCore.QPointF(
        control_point.x() + (noterect.width() / 2),
        control_point.y() + round(noterect.height() / 20))
    control_point_2 = QtCore.QPointF(
        control_point.x() - ((noterect.width() / 3) * 2),
        control_point_2.y() + round(noterect.height() / 30))
    path.cubicTo(control_point, control_point_2, start_point)
    path.addEllipse(
        QtCore.QPointF(
            start_point.x() + round(noterect.width() / 2.5),
            start_point.y()),
        noterect.width() / 2.7, noterect.width() / 2.7)
    return path
