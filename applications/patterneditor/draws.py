from PyQt4 import QtGui, QtCore
from config import COLORS, GRID_SPACING


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
    state = 'hover' if state is True else 'free'
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


def draw_row_background(painter, rect, number, hover=False):
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)
    if hover is True:
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


def draw_index(
        painter, occurence, inplug_rect, outplug_rect, body_rect,
        fingerstate_rect, behavior_rect, selected=False, highlight_rects=None):
    highlight_rects = highlight_rects or []

    background = mix_colors(
        QtGui.QColor(COLORS['graph']['index']['background']['min']),
        QtGui.QColor(COLORS['graph']['index']['background']['max']),
        occurence)

    draw_index_plug(
        painter,
        inplug_rect,
        bgcolor=background,
        hover=inplug_rect in highlight_rects)

    draw_index_plug(
        painter,
        outplug_rect,
        bgcolor=background,
        hover=outplug_rect in highlight_rects)

    draw_index_body(
        painter,
        body_rect,
        bgcolor=background,
        selected=selected,
        hover=body_rect in highlight_rects)

    draw_index_button(
        painter,
        fingerstate_rect,
        selected=selected,
        hover=fingerstate_rect in highlight_rects)

    draw_index_button(
        painter,
        behavior_rect,
        selected=selected,
        hover=behavior_rect in highlight_rects)


def draw_index_plug(painter, rect, bgcolor=None, hover=False):
    if hover is True:
        color = QtGui.QColor(COLORS['graph']['index']['plug_highlight'])
    else:
        color = QtGui.QColor(bgcolor)
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)
    brush = QtGui.QBrush(color)
    painter.setBrush(brush)
    painter.drawEllipse(rect)


def draw_index_body(painter, rect, bgcolor=None, selected=False, hover=False):
    painter.setBrush(bgcolor)
    if selected is True:
        color = QtGui.QColor(COLORS['graph']['index']['border']['selected'])
    elif hover is True:
        color = QtGui.QColor(COLORS['graph']['index']['border']['highlight'])
    else:
        color = QtGui.QColor(0, 0, 0, 0)
    pen = QtGui.QPen(QtGui.QColor(color))
    pen.setWidth(3)
    painter.setPen(pen)
    painter.drawRoundedRect(rect, 3, 3)


def draw_index_button(painter, rect, selected=False, hover=False):
    if selected is True:
        color = QtGui.QColor(
            COLORS['graph']['index']['item']['border']['selected'])
    elif hover is True:
        color = QtGui.QColor(
            COLORS['graph']['index']['item']['border']['selected'])
    else:
        color = QtGui.QColor(0, 0, 0, 0)

    pen = QtGui.QPen(color)
    pen.setWidth(3)
    painter.setPen(pen)
    background_color = COLORS['graph']['index']['item']['background']
    brush = QtGui.QBrush(QtGui.QColor(background_color))
    painter.setBrush(brush)
    painter.drawEllipse(rect)


def draw_connection(painter, path, handler_rect, hover=False):
    if hover:
        color = QtGui.QColor(COLORS['graph']['index']['path']['highlight'])
    else:
        color = QtGui.QColor(COLORS['graph']['index']['path']['normal'])
    pen = QtGui.QPen(color)
    pen.setWidth(2)
    painter.setPen(pen)

    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
    painter.setBrush(brush)

    painter.drawPath(path)

    brush = QtGui.QBrush(color)
    painter.setBrush(brush)
    painter.drawEllipse(handler_rect)


def mix_colors(color_min, color_max, percent):
    zr, zg, zb, _ = color_min.getRgb()
    hr, hg, hb, _ = color_max.getRgb()

    r = abs(zr - hr) * (percent / 100) + min(zr, hr)
    g = abs(zg - hg) * (percent / 100) + min(zg, hg)
    b = abs(zb - hb) * (percent / 100) + min(zb, hb)
    return QtGui.QColor(r, g, b)


def draw_note_path(painter, path, selected=False, hover=False):
    if selected is True:
        color = QtGui.QColor(COLORS['note']['selected'])
    elif hover is True:
        color = QtGui.QColor(COLORS['note']['highlight'])
    else:
        color = QtGui.QColor(COLORS['note']['normal'])
    painter.setPen(QtGui.QPen(color))
    painter.setBrush(QtGui.QBrush(color))
    painter.drawPath(path)
