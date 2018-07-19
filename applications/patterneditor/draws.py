from PyQt4 import QtGui, QtCore
from montunolito.core.pattern import get_index_occurence_probablity
from config import COLORS, GRID_SPACING
from rects import (
    get_behavior_rect, get_fingerstate_rect, get_index_inplug_rect,
    get_index_outplug_rect, get_index_body_rect, get_row_rect, get_index_rect)


def draw_fingerstate(painter, fingerstate, rect, border=False):
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    pen.setWidth(0)
    painter.setPen(pen)
    width = round(rect.width() / 5.0)

    rects = [
        QtCore.QRect(
            rect.left() + (i * width),
            rect.top(), width, rect.height()) for i in range(5)]

    brush_pressed = QtGui.QBrush(
        QtGui.QColor(COLORS['fingerstates']['pressed']))
    brush_released = QtGui.QBrush(
        QtGui.QColor(COLORS['fingerstates']['released']))

    for r, s in zip(rects, fingerstate):
        painter.setBrush(brush_pressed if s is True else brush_released)
        painter.drawRect(r)

    if border is False:
        return

    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
    pen = QtGui.QPen(QtGui.QColor(COLORS['bubble']['border']))
    painter.setPen(pen)
    painter.setBrush(brush)
    painter.drawRect(rect)

    brush = QtGui.QBrush(QtGui.QColor(COLORS['bubble']['border']))
    painter.setBrush(brush)
    comborect = QtCore.QRect(
        rect.width() + rect.left(), rect.top(), 20, rect.height())
    painter.drawRect(comborect)

    brush = QtGui.QBrush(QtGui.QColor(COLORS['bubble']['background']))
    painter.setBrush(brush)
    polygon = QtGui.QPolygon([
        QtCore.QPoint(rect.width() + rect.left() + 5, rect.top() + 7),
        QtCore.QPoint(rect.width() + rect.left() + 15, rect.top() + 7),
        QtCore.QPoint(rect.width() + rect.left() + 10, rect.top() + 12)])
    painter.drawPolygon(polygon)


def draw_ballon(painter, rect, title):
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    pen.setWidth(0)
    pen.setJoinStyle(QtCore.Qt.MiterJoin)

    painter.setBrush(
        QtGui.QBrush(QtGui.QColor(COLORS['bubble']['background'])))
    painter.setPen(pen)

    polygon = QtGui.QPolygon([
        QtCore.QPoint(28, rect.height() - 30),
        QtCore.QPoint(20, rect.height()),
        QtCore.QPoint(50, rect.height() - 30)])

    painter.drawPolygon(polygon)
    painter.drawRoundedRect(
        2, 2, rect.width() - 4, rect.height() - 29, 22, 22)

    pen = QtGui.QPen(QtGui.QColor(COLORS['bubble']['title']))
    painter.setPen(pen)

    font = QtGui.QFont()
    font.setBold(True)
    font.setPointSize(12)
    painter.setFont(font)
    painter.drawText(20, 25, title)


def draw_closer(painter, rect, state):
    state = 'over' if state is True else 'free'
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)

    brush = QtGui.QBrush(QtGui.QColor(COLORS['bubble']['closer'][state]))
    painter.setBrush(brush)

    painter.drawRoundedRect(rect, 5, 5)
    pen = QtGui.QPen(QtGui.QColor(COLORS['bubble']['closer']['cross']))
    pen.setWidth(2)
    painter.setPen(pen)
    shrink = 5
    painter.drawLine(
        QtCore.QPoint(rect.left() + shrink, rect.top() + shrink),
        QtCore.QPoint(
            rect.left() + rect.width() - shrink,
            rect.top() + rect.height() - shrink))
    painter.drawLine(
        QtCore.QPoint(
            rect.left() + rect.width() - shrink, rect.top() + shrink),
        QtCore.QPoint(
            rect.left() + shrink, rect.top() + rect.height() - shrink))


def draw_texts(painter, rect, texts):
    font = QtGui.QFont()
    font.setBold(False)
    font.setPointSize(11)
    painter.setFont(font)

    pen = QtGui.QPen(QtGui.QColor(110, 110, 110))
    painter.setPen(pen)
    top_offset = rect.top() + 5
    for i, text in enumerate(texts):
        painter.drawText(27, (20 * i) + top_offset, text)


def draw_background(painter, rect):
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)

    brush = QtGui.QBrush(QtGui.QColor(COLORS['graph']['background']))
    painter.setBrush(brush)
    painter.drawRect(rect)

    pen = QtGui.QPen(QtGui.QColor(COLORS['graph']['grid']))
    painter.setPen(pen)
    left = 0
    while left < rect.width():
        left += GRID_SPACING
        painter.drawLine(
            QtCore.QPoint(left, 0),
            QtCore.QPoint(left, rect.height()))

    top = 0
    while top < rect.height():
        top += GRID_SPACING
        painter.drawLine(
            QtCore.QPoint(0, top),
            QtCore.QPoint(rect.width(), top))


def draw_row_background(painter, rect, number, cursor):
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)
    hover = rect.contains(cursor)
    if hover:
        color = COLORS['graph']['row']['background_highlight']
    else:
        color = COLORS['graph']['row']['background']
    brush = QtGui.QBrush(QtGui.QColor(color))
    painter.setBrush(brush)
    painter.drawRoundedRect(
        rect.left(), rect.top() + 20, rect.width(), rect.height() - 5, 10, 10)

    painter.drawRoundedRect(
        rect.left() + rect.width() - 30, rect.top(), 30, 40, 10, 10)

    pen = QtGui.QPen(QtGui.QColor(COLORS['graph']['row']['number']))
    painter.setPen(pen)

    font = QtGui.QFont()
    font.setBold(True)
    font.setPointSize(12)
    painter.setFont(font)
    painter.drawText(
        rect.left() + rect.width() - 20, rect.top() + 20, str(number))
    return hover


def draw_index(painter, rect, occurence, cursor):
    inplug_rect = get_index_inplug_rect(rect)
    outplug_rect = get_index_outplug_rect(rect)
    body_rect = get_index_body_rect(rect)
    fingerstate_rect = get_fingerstate_rect(rect)
    behavior_rect = get_behavior_rect(rect)
    rects = (
        inplug_rect, outplug_rect, body_rect, fingerstate_rect, behavior_rect)
    hover = 0

    for i, r in enumerate(rects):
        if r.contains(cursor):
            hover = i + 1

    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)

    background = get_index_background_color(occurence)
    plug_highlight = QtGui.QColor(COLORS['graph']['index']['plug_highlight'])
    brush = QtGui.QBrush(plug_highlight if hover == 1 else background)
    painter.setBrush(brush)
    painter.drawEllipse(inplug_rect)

    brush = QtGui.QBrush(plug_highlight if hover == 2 else background)
    painter.setBrush(brush)
    painter.drawEllipse(outplug_rect)

    painter.setBrush(background)
    if hover == 3:
        color = COLORS['graph']['index']['border_highlight']
        pen = QtGui.QPen(QtGui.QColor(color))
        pen.setWidth(3)
        painter.setPen(pen)
    painter.drawRoundedRect(body_rect, 3, 3)

    color = COLORS['graph']['index']['item']['background']
    brush = QtGui.QBrush(QtGui.QColor(color))
    painter.setBrush(brush)
    if hover == 4:
        color = COLORS['graph']['index']['item']['border_highlight']
        pen = QtGui.QPen(QtGui.QColor(color))
        pen.setWidth(3)
    else:
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)
    painter.drawEllipse(fingerstate_rect)
    if hover == 5:
        color = COLORS['graph']['index']['item']['border_highlight']
        pen = QtGui.QPen(QtGui.QColor(color))
        pen.setWidth(3)
    else:
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)
    painter.drawEllipse(behavior_rect)
    return hover


def draw_pattern(painter, pattern, cursor):
    cursor_hover_row = None
    cursor_hover_column = None
    cursor_hover = False

    for row_number, row in enumerate(pattern['quarters']):
        row_rect = get_row_rect(row_number, len(row))
        cursor_hover = draw_row_background(
            painter, row_rect, row_number + 1, cursor)
        if cursor_hover:
            cursor_hover_row = row_number

        for column in range(len(row)):
            index = row_number, column
            rect = get_index_rect(*index)
            probabilty = get_index_occurence_probablity(pattern, index)
            cursor_hover = draw_index(painter, rect, probabilty, cursor)
            if cursor_hover:
                cursor_hover_column = column

    return cursor_hover_row, cursor_hover_column


def get_index_background_color(percent):
    zero = QtGui.QColor(COLORS['graph']['index']['background_0'])
    hundred = QtGui.QColor(COLORS['graph']['index']['background_100'])
    zr, zg, zb, _ = zero.getRgb()
    hr, hg, hb, _ = hundred.getRgb()

    r = abs(zr - hr) * (percent / 100) + min(zr, hr)
    g = abs(zg - hg) * (percent / 100) + min(zg, hg)
    b = abs(zb - hb) * (percent / 100) + min(zb, hb)
    return QtGui.QColor(r, g, b)
