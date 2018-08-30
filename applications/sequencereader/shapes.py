from PyQt5 import QtGui, QtCore
import sys
from sequencereader.staff import (
    get_note_position, get_top_from_position, POSITIONS_COUNT, get_additional_staff_lines)


def get_notes_path(noterect, notes):
    radius = noterect.height() / POSITIONS_COUNT
    x = noterect.center().x()
    previous_position = sys.maxsize
    points = []
    for note in notes:
        position = get_note_position(note)
        top = get_top_from_position(noterect, position)
        difference = abs(position - previous_position)
        left = x - radius if difference > 1 else x + radius
        points.append(QtCore.QPointF(left, top))
        previous_position = position

    path = QtGui.QPainterPath()
    for point in points:
        transform = QtGui.QTransform()
        transform.translate(point.x(), point.y())
        transform.rotate(-25)
        transform.translate(-point.x(), -point.y())
        note_path = QtGui.QPainterPath()
        note_path.addEllipse(point, radius, radius * .75)
        note_path = transform.map(note_path)
        path.addPath(note_path)

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
