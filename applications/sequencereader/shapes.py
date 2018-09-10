from PyQt5 import QtGui, QtCore
import sys
from montunolito.core.utils import past_and_futur
from sequencereader.staff import get_top_from_position, POSITIONS_COUNT


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

SHARP = {
    'center': (50, 50),
    'start': (33, 39),
    'points': (
        [(33, 48)], [(66, 39)], [(66, 30)], [(33, 39)], [None, (33, 66)],
        [(33, 75)], [(66, 66)], [(66, 57)], [(33, 66)], [None, (42, 20)],
        [(42, 88)], [(44, 88)], [(44, 20)], [(42, 20)], [None, (56, 17)],
        [(56, 85)], [(58, 85)], [(58, 17)], [(56, 17)])}

NATURAL = {
    'center': (50, 50),
    'start': (42, 0),
    'points': (
        [(42, 73)], [(44, 73)], [(44, 0)], [(44, 0)], [None, (42, 77)],
        [(66, 68)], [(66, 59)], [(42, 68)], [(42, 77)], [None, (42, 43)],
        [(66, 34)], [(66, 25)], [(42, 34)], [(42, 43)], [None, (66, 100)],
        [(64, 100)], [(64, 33)], [(66, 33)], [(66, 100)])}

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
        [(75, 0)],
        [(66, 25), (50, 33), (25, 33)],
        [(0, 33), (0, 0), (25, 0)],
        [(45, 0), (45, 27), (25, 27)],
        [(33, 27), (66, 27), (75, 0)],
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
        [(63, 48), (45, 48), (45, 59)],
        [(45, 59), (47, 65), (50, 65)]
    )
}


def get_path(
        array, ratio=100, rotation=None, position=None, mirrorh=False):
    '''
    This method transform a dict to a QPainterPath().
    The path will be transformed with the given ratio(in%), rotation(degree),
    position(QPoint) and have an horizontal mirror.
    The dict must contains 2 keys
        'start': (x, y)
        'points': (
            [(x, y)], # will be interpreted as lineTo
            [None, (x, y)], # will be interpreted as moveTo
            [(x, y), (x, y), (x, y)]]) # will be interpreted as cubicTo
    a third key can be used to set a shape center (default is (0, 0)):
        'center': (x, y)
    '''
    ratio /= 100

    path = QtGui.QPainterPath(QtCore.QPointF(*array['start']))
    path.setFillRule(QtCore.Qt.WindingFill)

    for points in array['points']:
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
    scaleh = - ratio if mirrorh else ratio
    transform.scale(scaleh, ratio)
    return transform.map(path)


def get_notes_bodies_path(centers, height):
    path = QtGui.QPainterPath()
    radius = height / POSITIONS_COUNT
    for center in centers:
        path.addPath(get_note_path(center, radius))
    return path


def get_notes_alterations_path(centers, height, shape=BEMOL):
    path = QtGui.QPainterPath()
    ratio = height / 10
    for center in centers:
        path.addPath(get_path(shape, ratio=ratio, position=center))
    return path


def get_beam_path(x, top, bottom):
    path = QtGui.QPainterPath(QtCore.QPointF(x, top))
    path.lineTo(QtCore.QPointF(x, bottom))
    return path


def get_notes_connections_path(lefts, height, tops, bottoms, dirs):
    path = QtGui.QPainterPath()
    start_point = None
    iterator = past_and_futur([a for a in zip(lefts, tops, bottoms, dirs)])

    for i, (_, (x, top, bottom, direction), futur) in enumerate(iterator):
        next_top = futur[1] if futur else None
        if not top:
            start_point = None
            continue

        path.addPath(get_beam_path(x, top, bottom))

        end_point = QtCore.QPointF(x, top)
        if next_top is not None:
            if start_point is None:
                start_point = QtCore.QPointF(x, top)
            continue

        if start_point is None:
            if i % 2 != 0:
                tail = get_path(
                    TAIL,
                    rotation=-180 if direction == 'down' else None,
                    ratio=height / 8,
                    position=end_point,
                    mirrorh=direction == 'down')
                path.addPath(tail)
            continue
        path.addPath(get_beam_connection_path(start_point, end_point, height))

    return path


def get_eighth_rest_path(left, top, height):
    return get_path(
        EIGHTH_REST,
        ratio=height / 15,
        position=QtCore.QPointF(left, top + (height / 2)))


def get_measure_separator(rect, end=False):
    top = rect.top() + get_top_from_position(rect.height(), 33)
    bottom = rect.top() + get_top_from_position(rect.height(), 25)
    x = rect.right() if end is False else rect.right() - (rect.width() / 33)
    path = QtGui.QPainterPath(QtCore.QPointF(x, top))
    path.lineTo(QtCore.QPointF(x, bottom))
    if end is False:
        return path
    path.moveTo(rect.right(), top)
    path.lineTo(rect.right(), bottom)
    right = rect.right() - (rect.width() / 60)
    path.lineTo(right, bottom)
    path.lineTo(right, top)
    path.lineTo(rect.right(), top)
    return path


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
