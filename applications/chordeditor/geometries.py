from PyQt5 import QtCore, QtGui


STAFF_PADDING = 10
STAFF_SPACING = 15
STAFF_HEIGHT = 40

REPEAT_WIDTH = 1.5
REPEAT_HEIGHT = 10
REPEAT_OFFSET = 2



def extract_noteitem_rect(rect, index):
    width = rect.width() / 12
    return QtCore.QRect(
        rect.left() + (width * index),
        rect.top(),
        width,
        rect.height())


def extract_chordname_rect(rect, index):
    width = rect.width() / 18
    return QtCore.QRect(
        rect.left() + (width * index),
        rect.top(),
        width,
        rect.height())


def get_staff_path(rect, final=False):
    v_center = rect.top() + (rect.height() / 2)
    start_point = QtCore.QPointF(rect.left(), v_center)
    end_point = QtCore.QPointF(rect.right(), v_center)
    path = QtGui.QPainterPath(start_point)
    path.lineTo(end_point)

    height = rect.height() * .3
    quarters_rect = QtCore.QRectF(
        rect.left(), v_center - (height / 2),
        rect.width(), height)

    height = rect.height() * .15
    heighth_rect = QtCore.QRectF(
        rect.left(), v_center - (height / 2),
        rect.width(), height)

    path = graduate_path(rect, path, 2)
    path = graduate_path(quarters_rect, path, 8)
    path = graduate_path(heighth_rect, path, 16)

    if not final:
        return path

    path.moveTo(rect.right() - 3, rect.top())
    path.lineTo(rect.right() - 3, rect.bottom())

    final_rect = QtCore.QRectF(rect.right() - 1, rect.top(), 1, rect.height())
    path.addRect(final_rect)

    return path


def extract_heighth_rects(staffrect):
    rects = []
    increment = staffrect.width() / 16
    for i in range(17):
        left = staffrect.left() + (i * increment)
        rects.append(
            QtCore.QRectF(
                left, staffrect.top(), increment, staffrect.height()))
    return rects


def extract_staffs_rects(rect, staff_count):
    rects = []
    left = rect.left() + STAFF_PADDING
    width = rect.width() - (STAFF_PADDING * 2)
    for i in range(staff_count):
        top = STAFF_PADDING + rect.top() + (i * (STAFF_HEIGHT + STAFF_SPACING))
        rects.append(QtCore.QRectF(left, top, width, STAFF_HEIGHT))
    return rects


def get_repeat_path(rect):
    center = rect.center()

    point_1 = QtCore.QPointF(
        center.x() + REPEAT_OFFSET - (REPEAT_WIDTH / 2),
        center.y() - (REPEAT_HEIGHT / 2))

    point_2 = QtCore.QPointF(
        center.x() - REPEAT_OFFSET - (REPEAT_WIDTH / 2),
        center.y() + (REPEAT_HEIGHT / 2))

    point_3 = QtCore.QPointF(
        center.x() - REPEAT_OFFSET + (REPEAT_WIDTH / 2),
        center.y() + (REPEAT_HEIGHT / 2))

    point_4 = QtCore.QPointF(
        center.x() + REPEAT_OFFSET + (REPEAT_WIDTH / 2),
        center.y() - (REPEAT_HEIGHT / 2))

    path = QtGui.QPainterPath(point_1)
    path.lineTo(point_2)
    path.lineTo(point_3)
    path.lineTo(point_4)
    path.lineTo(point_1)
    return path


def graduate_path(rect, path, value):
    increment = rect.width() / value
    for i in range(value + 1):
        left = rect.left() + (i * increment)
        start_point = QtCore.QPointF(left, rect.top())
        end_point = QtCore.QPointF(left, rect.bottom())
        path.moveTo(start_point)
        path.lineTo(end_point)
    return path
