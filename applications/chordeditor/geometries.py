from PyQt5 import QtCore, QtGui


GLOBAL_WIDTH = 1200
NOTESELECTER_HEIGHT = 30
CHORDSELECTER_HEIGHT = 20

STAFF_PADDING = 10
STAFF_TOP_PADDING = 15
STAFF_LEFT = 15
STAFF_SELECTION_RADIUS = STAFF_LEFT * .5
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


def get_chordgrid_rect(rect):
    top = (
        rect.top() +
        STAFF_TOP_PADDING)
    return QtCore.QRectF(
        rect.left() + STAFF_PADDING,
        top,
        rect.width() - (STAFF_PADDING * 2),
        rect.height() - STAFF_TOP_PADDING)


def get_chord_constructor_size():
    height = NOTESELECTER_HEIGHT + CHORDSELECTER_HEIGHT
    return QtCore.QSize(GLOBAL_WIDTH, height)


def get_chordgrid_minimumsize(chordgrid):
    height = (
        NOTESELECTER_HEIGHT +
        CHORDSELECTER_HEIGHT +
        STAFF_TOP_PADDING +
        ((STAFF_HEIGHT + STAFF_SPACING) * len(chordgrid.staffs)) +
        STAFF_TOP_PADDING)
    return QtCore.QSize(GLOBAL_WIDTH, height)


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
    rect = QtCore.QRectF(
        rect.left() + STAFF_LEFT, rect.top(),
        rect.width() - STAFF_LEFT, rect.height())
    start_point = QtCore.QPointF(rect.left(), rect.bottom())
    end_point = QtCore.QPointF(rect.right(), rect.bottom())
    path = QtGui.QPainterPath(start_point)
    path.lineTo(end_point)

    height = rect.height() * .15
    quarters_rect = QtCore.QRectF(
        rect.left(), rect.bottom() - height,
        rect.width(), height)

    path = graduate_path(rect, path, 4)
    path = graduate_path(quarters_rect, path, 16)

    if not final:
        return path

    path.moveTo(rect.right() - 3, rect.top())
    path.lineTo(rect.right() - 3, rect.bottom())

    final_rect = QtCore.QRectF(rect.right() - 1, rect.top(), 1, rect.height())
    path.addRect(final_rect)

    return path


def extract_heighth_rects(staffrect):
    rect = QtCore.QRectF(
        staffrect.left() + STAFF_LEFT, staffrect.top(),
        staffrect.width() - STAFF_LEFT, staffrect.height())
    rects = []
    increment = rect.width() / 32
    for i in range(33):
        left = rect.left() + (i * increment)
        rects.append(
            QtCore.QRectF(
                left, rect.top(), increment, rect.height()))
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


def get_drag_path(items, cursor):
    points = [item.rect.center() for item in items if item] + [cursor]
    if len(points) == 1:
        return

    path = QtGui.QPainterPath(points[0])
    for point in points:
        path.lineTo(point)
        if point == points[-1]:
            continue
        path.addEllipse(point, DRAGPATH_ROUND_RADIUS, DRAGPATH_ROUND_RADIUS)
        path.moveTo(point)
    return path


def get_selection_rects(items, grow=2):
    rects = []
    rect = None
    previous_selected = False
    for item in items:
        if item.selected:
            if previous_selected is False:
                rect = QtCore.QRectF(item.rect)
            else:
                rect = rect.united(item.rect)
        elif rect is not None:
            rects.append(grow_rect(rect, grow))
        previous_selected = item if item.selected else False
    if rect is not None:
        rects.append(grow_rect(rect, grow))
    return rects


def grow_rect(rect, value):
    return QtCore.QRectF(
        rect.left() - value,
        rect.top() - value,
        rect.width() + (value * 2),
        rect.height() + (value * 2))


def get_staff_selecter_rect(rect):
    return QtCore.QRectF(rect.left(), rect.top(), STAFF_LEFT, rect.height())


def get_staff_selecter_path(rect):
    path = QtGui.QPainterPath()
    path.addEllipse(
        rect.center().x() - (STAFF_SELECTION_RADIUS / 2),
        rect.center().y() - (STAFF_SELECTION_RADIUS / 2),
        STAFF_SELECTION_RADIUS,
        STAFF_SELECTION_RADIUS)
    return path


def get_square_rect(in_point, out_point):
    left = min([in_point.x(), out_point.x()])
    right = max([in_point.x(), out_point.x()])
    top = min([in_point.y(), out_point.y()])
    bottom = max([in_point.y(), out_point.y()])
    return QtCore.QRectF(left, top, right - left, bottom - top)