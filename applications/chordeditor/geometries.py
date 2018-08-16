from PyQt5 import QtCore, QtGui


GLOBAL_WIDTH = 1200
NOTESELECTER_HEIGHT = 30
CHORDSELECTER_HEIGHT = 20

STAFF_PADDING = 10
STAFF_TOP_PADDING = 30
STAFF_SPACING = 20
STAFF_HEIGHT = 30

REPEAT_WIDTH = 1.5
REPEAT_HEIGHT = 10
REPEAT_OFFSET = 2

DRAGPATH_ROUND_RADIUS = 5


def get_noteselecter_rect(rect):
    return QtCore.QRectF(
        rect.left(),
        rect.top(),
        GLOBAL_WIDTH,
        NOTESELECTER_HEIGHT)


def get_functionselecter_rect(rect):
    return QtCore.QRectF(
        rect.left(),
        rect.top() + NOTESELECTER_HEIGHT,
        GLOBAL_WIDTH,
        CHORDSELECTER_HEIGHT)


def get_staffs_rect(rect):
    top = (
        rect.top() +
        STAFF_TOP_PADDING +
        NOTESELECTER_HEIGHT +
        CHORDSELECTER_HEIGHT)
    return QtCore.QRectF(
        rect.left() + STAFF_PADDING,
        top,
        rect.width() - (STAFF_PADDING * 2),
        rect.height() - STAFF_TOP_PADDING)


def extract_items_rect(rect, index, count):
    width = rect.width() / count
    return QtCore.QRectF(
        rect.left() + (width * index),
        rect.top(),
        width,
        rect.height())


def get_staff_path(rect, final=False):
    start_point = QtCore.QPointF(rect.left(), rect.bottom())
    end_point = QtCore.QPointF(rect.right(), rect.bottom())
    path = QtGui.QPainterPath(start_point)
    path.lineTo(end_point)

    height = rect.height() * .15
    quarters_rect = QtCore.QRectF(
        rect.left(), rect.bottom() - height,
        rect.width(), height)

    path = graduate_path(rect, path, 2)
    path = graduate_path(quarters_rect, path, 8)

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
    for i in range(staff_count):
        top = STAFF_PADDING + rect.top() + (i * (STAFF_HEIGHT + STAFF_SPACING))
        rects.append(
            QtCore.QRectF(rect.left(), top, rect.width(), STAFF_HEIGHT))
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


def get_drag_path(points):
    path = QtGui.QPainterPath(points[0])
    for point in points:
        path.lineTo(point)
        if point == points[-1]:
            continue
        path.addEllipse(point, DRAGPATH_ROUND_RADIUS, DRAGPATH_ROUND_RADIUS)
        path.moveTo(point)
    return path


def get_selection_rects(staff):
    rects = []
    rect = None
    previous_selected = False
    for igchord in staff.chords:
        if igchord.selected:
            if previous_selected is False:
                rect = QtCore.QRectF(igchord.rect)
            else:
                rect.setBottomRight(igchord.rect.bottomRight())
        else:
            if rect is not None:
                rects.append(rect)
        previous_selected = igchord if igchord.selected else False
    if rect is not None:
        rects.append(rect)
    return rects


def get_square_rect(in_point, out_point):
    left = min([in_point.x(), out_point.x()])
    right = max([in_point.x(), out_point.x()])
    top = min([in_point.y(), out_point.y()])
    bottom = max([in_point.y(), out_point.y()])
    return QtCore.QRectF(left, top, right - left, bottom - top)