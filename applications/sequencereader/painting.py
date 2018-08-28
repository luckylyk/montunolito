from PyQt5 import QtGui


def draw_measure(painter, igmeasure):
    painter.setBrush(QtGui.QBrush(QtGui.QColor('red')))
    painter.setPen(QtGui.QPen(QtGui.QColor('black')))
    # painter.drawRect(igmeasure.rect)
    painter.drawPath(igmeasure.staff_lines)
    painter.drawPath(igmeasure.separator)


def draw_quarter(painter, quarter):
    painter.setBrush(QtGui.QBrush(QtGui.QColor('red')))
    painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))
    # for rect in quarter.note_rects:
    #     painter.drawRect(rect)
    painter.setBrush(QtGui.QBrush(QtGui.QColor('black')))
    for path in quarter.paths:
        painter.drawPath(path)


def draw_keyspace(painter, igkeyspace):
    painter.setBrush(QtGui.QBrush(QtGui.QColor('red')))
    painter.setPen(QtGui.QPen(QtGui.QColor('black')))
    # painter.drawRect(igkeyspace.rect)
    painter.drawPath(igkeyspace.staff_lines)