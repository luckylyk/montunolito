from PyQt4 import QtCore, QtGui
from config import (
    COLORS, ROWS_TOP, ROWS_LEFT, ROWS_SPACING, ROWS_WIDTH, ROWS_BOTTOM_SPACE,
    ROWS_HEADER_SPACE, INDEX_HEIGHT, INDEX_WIDTH, INDEX_SPACING, ROWS_PADDING)


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