from PyQt4 import QtCore, QtGui
from config import (
    COLORS, ROWS_TOP, ROWS_LEFT, ROWS_SPACING, ROWS_WIDTH, ROWS_BOTTOM_SPACE,
    ROWS_HEADER_SPACE, INDEX_HEIGHT, INDEX_WIDTH, INDEX_SPACING, ROWS_PADDING,
    CONNECTION_HANDLER_SIZE)

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