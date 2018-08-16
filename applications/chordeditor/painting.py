from PyQt5 import QtCore, QtGui

COLORS = {
    'noteitem.background.normal': '#FFEFE3',
    'noteitem.background.highlight': '#EEDED2',
    'noteitem.background.active': 'yellow',
    'noteitem.text': 'black',
    'staff.lines': 'black',
    'dragpath': 'red',
    'background': '#FFEFE3',
    'chord.text': 'black',
    'chord.background.active': 'yellow',
    'chord.background.highlight': '#EEDED2',
    'chord.path': 'black',
    'chord.border.selected': 'red',
    'selectionsquare': 'blue'
}

def draw_background(painter, rect):
    color = QtGui.QColor(COLORS['background'])
    painter.setPen(QtGui.QPen(color))
    painter.setBrush(QtGui.QBrush(color))
    painter.drawRect(rect)


def draw_chord(painter, igchord):
    if igchord.active is True:
        color = COLORS['chord.background.active']
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(color)))
        painter.drawRect(igchord.rect)
    elif igchord.hovered is True:
        color = COLORS['chord.background.highlight']
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(color)))
        painter.drawRect(igchord.rect)

    if igchord.path is not None:
        color = COLORS['chord.path']
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(color)))
        painter.drawPath(igchord.path)

    if igchord.name is None:
        return

    color = COLORS['chord.text']
    painter.setPen(QtGui.QPen(QtGui.QColor(color)))
    option = QtGui.QTextOption()
    option.setAlignment(QtCore.Qt.AlignCenter)
    font = QtGui.QFont()
    font.setBold(True)
    size = min([igchord.rect.width(), igchord.rect.height()]) * .5
    font.setPixelSize(size)
    painter.setFont(font)
    text_rect = QtCore.QRectF(igchord.rect)
    painter.drawText(text_rect, igchord.name, option)


def draw_note_item(painter, noteitem):
    if noteitem.active is True:
        color = COLORS['noteitem.background.active']
    elif noteitem.hovered is True:
        color = COLORS['noteitem.background.highlight']
    else:
        color = COLORS['noteitem.background.normal']

    painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))
    painter.setBrush(QtGui.QBrush(QtGui.QColor(color)))
    painter.drawRect(noteitem.rect)

    color = COLORS['noteitem.text']
    painter.setPen(QtGui.QPen(QtGui.QColor(color)))
    option = QtGui.QTextOption()
    option.setAlignment(QtCore.Qt.AlignCenter)
    font = QtGui.QFont()
    font.setBold(True)
    size = min([noteitem.rect.width(), noteitem.rect.height()]) * .66
    font.setPixelSize(size)
    painter.setFont(font)
    text_rect = QtCore.QRectF(noteitem.rect)
    painter.drawText(text_rect, noteitem.text, option)


def draw_staff(painter, path):
    color = QtGui.QColor(COLORS['staff.lines'])
    painter.setPen(QtGui.QPen(color))
    painter.setBrush(QtGui.QBrush(color))
    painter.drawPath(path)


def draw_selection_rects(painter, rects):
    color = COLORS['chord.border.selected']
    pen = QtGui.QPen(QtGui.QColor(color))
    pen.setWidth(2)
    painter.setPen(pen)
    painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 0)))
    for rect in rects:
        painter.drawRect(rect)

def draw_drag_path(painter, path):
    color = QtGui.QColor(COLORS['dragpath'])
    painter.setPen(QtGui.QPen(color))
    painter.setBrush(QtGui.QBrush(color))
    painter.drawPath(path)


def draw_selection_square(painter, rect):
    if rect is None:
        return
    color = QtGui.QColor(COLORS['selectionsquare'])
    painter.setPen(QtGui.QPen(color))
    color.setAlpha(75)
    painter.setBrush(QtGui.QBrush(color))
    painter.drawRect(rect)