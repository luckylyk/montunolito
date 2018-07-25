from PyQt4 import QtCore, QtGui
from config import (
    COLORS, ROWS_TOP, ROWS_LEFT, ROWS_SPACING, ROWS_WIDTH, ROWS_BOTTOM_SPACE,
    ROWS_HEADER_SPACE, INDEX_HEIGHT, INDEX_WIDTH, INDEX_SPACING, ROWS_PADDING,
    CONNECTION_HANDLER_SIZE, BEAM_CONNECTION_WIDTH)


def get_fingerstate_rect(rect):
    offset = 3
    width = rect.height() - (offset * 2)
    left = rect.left() + ((rect.width() / 6) * 2)
    return QtCore.QRect(left, rect.top() + offset, width, width)


def get_behavior_rect(rect):
    offset = 3
    width = rect.height() - (offset * 2)
    left = rect.left() + ((rect.width() / 6) * 3)
    return QtCore.QRect(left, rect.top() + offset, width, width)


def get_index_body_rect(rect):
    offset = 15
    return QtCore.QRect(
        rect.left() + offset,
        rect.top(),
        rect.width() - (offset * 2),
        rect.height())


def get_index_inplug_rect(rect):
    width = 10
    return QtCore.QRect(
        rect.left(), rect.top() + (rect.height() / 2) - (width / 2),
        width, width)


def get_index_outplug_rect(rect):
    width = 10
    return QtCore.QRect(
        rect.left() + rect.width() - width,
        rect.top() + (rect.height() / 2) - (width / 2),
        width, width)


def get_index_rect(row, column):
    left = ROWS_LEFT + (row * (ROWS_SPACING + ROWS_WIDTH)) + ROWS_PADDING
    top = (
        ROWS_TOP + ROWS_HEADER_SPACE +
        (column * (INDEX_HEIGHT + INDEX_SPACING)))

    return QtCore.QRect(
        left,
        top,
        INDEX_WIDTH,
        INDEX_HEIGHT)


def get_row_rect(row_number, row_len):
    left = ROWS_LEFT + ((ROWS_WIDTH + ROWS_SPACING) * row_number)
    height = (
        ROWS_HEADER_SPACE +
        ((INDEX_HEIGHT + INDEX_SPACING) * row_len) +
        ROWS_BOTTOM_SPACE)
    return QtCore.QRect(left, ROWS_TOP, ROWS_WIDTH, height)


def get_connection_path(start_point, end_point):
    path = QtGui.QPainterPath(start_point)
    control_point_1 = QtCore.QPoint(
        (
            start_point.x() +
            round((end_point.x() - start_point.x()) / 2)
        ),
        start_point.y())

    control_point_2 = QtCore.QPoint(
        (
            end_point.x() -
            round((end_point.x() - start_point.x()) / 2)
        ),
        end_point.y())
    path.cubicTo(control_point_1, control_point_2, end_point)
    return path


def get_connection_handler_rect(path):
    center = path.pointAtPercent(0.5).toPoint()
    top = center.y() - (CONNECTION_HANDLER_SIZE // 2)
    left = center.x() - (CONNECTION_HANDLER_SIZE // 2)
    return QtCore.QRect(
        left, top, CONNECTION_HANDLER_SIZE, CONNECTION_HANDLER_SIZE)


def get_note_path(
        noterect, note1=False, note2=False, note3=False, note4=False):
    notes = note1, note2, note3, note4
    round_rect = QtCore.QRect(
        noterect.left(),
        noterect.top() + noterect.height() - noterect.width(),
        noterect.width(),
        noterect.width())

    path = QtGui.QPainterPath(noterect.topLeft())
    centers = [
        QtCore.QPoint(
            round_rect.center().x(),
            round_rect.center().y() - (noterect.width() * i))
        for i, n in enumerate(notes) if n is True]

    for center in centers:
        path.addEllipse(
            center,
            noterect.width() / 2,
            (noterect.width() - round(noterect.width() / 3)) / 2)

    if not any(notes):
        return path

    path.moveTo(
        QtCore.QPoint(noterect.right(), noterect.top()))
    path.lineTo(
        QtCore.QPoint(
            noterect.right(),
            centers[0].y()))

    return path


def get_beam_tail_path(noterect):
    start_point = noterect.topRight()
    end_point = QtCore.QPoint(
        noterect.right() + round(((noterect.width() / 3) * 2)),
        noterect.top() + ((noterect.height() / 2)))

    control_point_1 = QtCore.QPoint(
        start_point.x(),
        start_point.y() + round((end_point.y() - start_point.y()) / 2))

    control_point_2 = QtCore.QPoint(
        start_point.x() + noterect.width() + round(noterect.width() / 2),
        end_point.y() - round((end_point.y() - start_point.y()) / 2))

    path = QtGui.QPainterPath(start_point)
    path.cubicTo(control_point_1, control_point_2, end_point)

    end_point = QtCore.QPoint(
        start_point.x(), start_point.y() + round(noterect.height() / 7))

    start_point = path.currentPosition()

    control_point_1 = QtCore.QPoint(
        start_point.x() + (noterect.width() / 2),
        start_point.y() - round((start_point.y() - end_point.y()) / 2))

    control_point_2 = QtCore.QPoint(
        end_point.x() + (noterect.width() / 10),
        end_point.y() + round((start_point.y() - end_point.y()) / 2))

    path.cubicTo(control_point_1, control_point_2, end_point)
    return path


def get_beams_connection_path(noterect1, noterect2):
    rect = QtCore.QRectF(
        noterect1.topRight(),
        QtCore.QPoint(
            noterect2.topRight().x(),
            noterect2.topRight().y() + BEAM_CONNECTION_WIDTH))
    path = QtGui.QPainterPath()
    path.addRect(rect)
    return path


def get_eighth_rest_path(noterect):
    start_point = QtCore.QPoint(
        noterect.left() - round(noterect.width() / 2),
        noterect.top() + round(noterect.height() / 3))

    path = QtGui.QPainterPath(start_point)

    control_point = QtCore.QPoint(
        start_point.x() + (noterect.width() / 5),
        start_point.y() + round(noterect.height() / 8))

    control_point_2 = QtCore.QPoint(
        start_point.x() + noterect.width(),
        start_point.y() + round(noterect.height() / 10))

    end_point = QtCore.QPoint(
        noterect.right() + round(noterect.width() / 2),
        noterect.top() + round(noterect.height() / 4))

    path.cubicTo(control_point, control_point_2, end_point)

    path.lineTo(QtCore.QPoint(
        noterect.left(), noterect.bottom() - round(noterect.height() / 3)))

    path.lineTo(QtCore.QPoint(
        start_point.x() + round(noterect.width() / 3),
        noterect.bottom() - round(noterect.height() / 3)))

    path.lineTo(end_point)

    control_point = QtCore.QPoint(
        control_point.x() + (noterect.width() / 2),
        control_point.y() + round(noterect.height() / 20))

    control_point_2 = QtCore.QPoint(
        control_point.x() - ((noterect.width() / 3) * 2),
        control_point_2.y() + round(noterect.height() / 30))

    path.cubicTo(control_point, control_point_2, start_point)

    path.addEllipse(
        QtCore.QPoint(
            start_point.x() + round(noterect.width() / 2),
            start_point.y()),
        noterect.width() / 2.1, noterect.width() / 2.1)

    return path


def extract_noterects(rect):
    width = rect.height() / 6
    left_offset = (rect.width() - width) / 3

    return [
        QtCore.QRect(
            rect.left() + (width / 2) + (left_offset * i),
            rect.top(),
            width,
            rect.height())
        for i in range(4)]
