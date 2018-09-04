from PyQt5 import QtGui, QtCore
import sys
from montunolito.core.utils import past_and_futur
from sequencereader.staff import (
    get_note_position, get_top_from_position, POSITIONS_COUNT,
    get_additional_staff_lines, get_beam_bottom, get_beams_tops,
    get_beams_directions, is_altered)


BEAMCONNECTION_WIDTH_FACTOR = .025
TAILS_HEIGHT_FACTOR = .33


BEMOL = {
    'center': (16, 76),
    'start': (0, 0),
    'points': (
        [(0, 100)],
        [(0, 100), (33, 76), (33, 66)],
        [(33, 66), (33, 50), (0, 66)],
        [(0, 68)],
        [(15, 60), (30, 66), (30, 60)],
        [(25, 70), (25, 80), (0, 98)],
        [(25, 70), (25, 80), (0, 98)])}

DIESE = {
    'center': (50, 50),
    'start': (33, 39),
    'points': (
        [(33, 48)], [(66, 39)], [(66, 30)], [(33, 39)], [None, (33, 66)],
        [(33, 75)], [(66, 66)], [(66, 57)], [(33, 66)], [None, (42, 20)],
        [(42, 88)], [(44, 88)], [(44, 20)], [(42, 20)], [None, (56, 17)],
        [(56, 85)], [(58, 85)], [(58, 17)], [(56, 17)])}

TAIL = {
    'start': (0, 0),
    'points': (
        [(0, 50), (33, 27), (33, 100)],
        [(33, 55), (0, 80), (0, 0)])}

EIGHTH_REST = {
    'center': (50, 135),
    'start': (31, 100),
    'points': (
        [(25, 100)],
        [(100, 0)],
        [(75, 25), (50, 33), (25, 33)],
        [(0, 33), (0, 0), (25, 0)],
        [(45, 0), (45, 27), (25, 27)],
        [(33, 27), (75, 27), (100, 0)],
        [(31, 100)])}

G_KEY = {
    'center': (50, 63),
    'start': (50, 65),
    'points': (
        [(47, 65), (43, 60), (43, 57)],
        [(43, 43), (67, 43), (67, 60)],
        [(67, 76), (33, 76), (33, 55)],
        [(33, 38), (61, 28), (61, 12)],
        [(61, 10), (60, 7), (58, 7)],
        [(53, 7), (50, 16), (51, 22)],
        [(59, 90)],
        [(59, 100), (38, 100), (38, 90)],
        [(38, 84), (47, 84), (47, 90)],
        [(47, 92), (45, 94), (43, 94)],
        [(43, 98), (59, 98), (58, 90)],
        [(50, 22)],
        [(48, 12), (52, 0), (58, 0)],
        [(61, 0), (62, 8), (62, 12)],
        [(62, 39), (35, 39), (35, 58)],
        [(35, 75), (65, 75), (65, 60)],
        [(63, 44), (45, 44), (45, 59)],
        [(45, 59), (47, 65), (50, 65)]
    )
}


def get_left_note(x, radius, difference, direction):
    if direction == 'up':
        return x - radius if difference > 1 else x + radius
    else:
        return x + radius if difference > 1 else x - radius


def get_left_alteration(x, radius, difference, direction):
    left = x - (radius * 3.5) if difference > 2 else x - (radius * 6)
    if direction != 'up':
        left += radius * 1.25
    return left


def get_notes_path(noterect, notes, direction='down'):
    if not notes:
        ratio = noterect.height() / 15
        point = noterect.center()
        return get_path(EIGHTH_REST, ratio=ratio, position=point)

    radius = noterect.height() / POSITIONS_COUNT
    x = noterect.center().x()
    previous_position = sys.maxsize
    previous_alteration_position = sys.maxsize
    notes_points = []
    alterations_points = []
    for note in notes:
        position = get_note_position(note)
        top = get_top_from_position(noterect, position)
        difference = abs(position - previous_position)
        left = get_left_note(x, radius, difference, direction)
        notes_points.append(QtCore.QPointF(left, top))
        previous_position = position

        if is_altered(note):
            difference = abs(position - previous_alteration_position)
            left = get_left_alteration(x, radius, difference, direction)
            alterations_points.append(QtCore.QPointF(left, top))
            previous_alteration_position = position

    path = QtGui.QPainterPath()
    for point in notes_points:
        path.addPath(get_note_path(point, radius))

    for point in alterations_points:
        ratio = noterect.height() / 10
        path.addPath(get_path(DIESE, ratio=ratio, position=point))

    rect = QtCore.QRectF(
        x - (radius * 2) - (radius / 2),
        noterect.top(),
        radius * 2 + radius,
        noterect.height())

    down = get_additional_staff_lines(rect, get_note_position(notes[0]))
    if down:
        path.addPath(down)
    up = get_additional_staff_lines(rect, get_note_position(notes[-1]))
    if up:
        path.addPath(up)
    return path


def get_notes_connections_path(noterects, sequence):
    path = QtGui.QPainterPath()
    directions = get_beams_directions(sequence)
    bottoms = [
        get_beam_bottom(noterects[0], notes, d == 'up') if notes else None
        for d, notes in zip(directions, sequence)]
    tops = get_beams_tops(noterects[0], sequence, directions)
    iterator = past_and_futur(
        [a for a in zip(noterects, tops, bottoms, directions)])
    start_point = None
    for _, current, futur in iterator:
        noterect = current[0]
        top = current[1]
        bottom = current[2]
        direction = current[3]
        next_top = futur[1] if futur else None
        if not top:
            start_point = None
            continue

        x = noterect.center().x()
        beam = QtGui.QPainterPath(QtCore.QPointF(x, top))
        beam.lineTo(QtCore.QPointF(x, bottom))
        path.addPath(beam)

        end_point = QtCore.QPointF(noterect.center().x(), top)
        if next_top is not None:
            if start_point is None:
                start_point = QtCore.QPointF(noterect.center().x(), top)
            continue
        if start_point is None:
            path.addPath(
                get_path(
                    TAIL,
                    rotation=-180 if direction == 'down' else None,
                    ratio=noterect.height() / 8,
                    position=end_point,
                    mirrorh=direction == 'down'))
            continue
        height = noterect.height()
        path.addPath(get_beam_connection_path(start_point, end_point, height))
    return path


def get_path(
        array, ratio=100, rotation=None, position=None, mirrorh=False):
    ratio /= 100

    path = QtGui.QPainterPath(QtCore.QPointF(*array['start']))
    points_arrays = array['points']
    for points in points_arrays:
        if len(points) == 1:
            path.lineTo(*[float(x) for x in points[0]])
        elif len(points) == 2:
            path.moveTo(*[float(x) for x in points[1]])
        else:
            path.cubicTo(*[float(x) for coords in points for x in coords])

    transform = QtGui.QTransform()
    if position:
        transform.translate(position.x(), position.y())
    center = array.get('center')
    if center:
        transform.translate(-center[0] * ratio, -center[1] * ratio)
    if rotation:
        transform.rotate(rotation)
    scalex = - ratio if mirrorh else ratio
    transform.scale(scalex, ratio)
    path.setFillRule(QtCore.Qt.WindingFill)
    return transform.map(path)


def get_note_path(point, radius):
    transform = QtGui.QTransform()
    transform.translate(point.x(), point.y())
    transform.rotate(-25)
    transform.translate(-point.x(), -point.y())
    path = QtGui.QPainterPath()
    path.addEllipse(point, radius, radius * .75)
    path = transform.map(path)
    return path


def get_beam_connection_path(startpoint, endpoint, height=150):
    connection_width = height * BEAMCONNECTION_WIDTH_FACTOR
    path = QtGui.QPainterPath(startpoint)
    path.lineTo(endpoint)
    path.lineTo(
        QtCore.QPointF(endpoint.x(), endpoint.y() - connection_width))
    path.lineTo(
        QtCore.QPointF(startpoint.x(), startpoint.y() - connection_width))
    path.lineTo(QtCore.QPointF(startpoint))
    return path
