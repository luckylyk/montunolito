from PyQt5 import QtGui, QtCore


def get_staff_lines(rect):
    path = QtGui.QPainterPath()
    # 88 max
    # 55 max in rect
    # 44 top staff line
    # 33 bot staff line
    # 22 min in rect
    # 0  min
    space = rect.height() / 33
    top = rect.top() + (11 * space)
    for _ in range(5):
        path.moveTo(rect.left(), top)
        path.lineTo(rect.right(), top)
        top += space * 2
    return path


def get_measure_separator(rect, left=False):
    left = rect.left() if left else rect.right()
    space = rect.height() / 33
    top = rect.top() + (11 * space)
    bottom = rect.top() + (19 * space)
    path = QtGui.QPainterPath(QtCore.QPointF(rect.right(), top))
    path.lineTo(rect.right(), bottom)
    return path


def get_notes_paths(noterects, sequence):
    paths = []
    for rect, notes in zip(noterects, sequence):
        print (notes)
        if not notes:
            paths.append(get_eighth_rest(rect))
    return paths


def get_eighth_rest(noterect):
    vpadding = noterect.height() * .35
    hpadding = noterect.width() * .3
    noterect = QtCore.QRectF(
        noterect.left() + hpadding,
        noterect.top() + (vpadding * .9),
        noterect.width() - (hpadding * 2),
        noterect.height() - (vpadding * 2))

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
            start_point.x() + round(noterect.width() / 2.5),
            start_point.y()),
        noterect.width() / 2.7, noterect.width() / 2.7)
    return path
