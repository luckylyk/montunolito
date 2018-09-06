from PyQt5 import QtGui


def draw_measure(painter, igmeasure):
    painter.setBrush(QtGui.QBrush(QtGui.QColor('black')))
    painter.setPen(QtGui.QPen(QtGui.QColor('black')))
    # painter.drawRect(igmeasure.rect)
    painter.drawPath(igmeasure.staff_lines)
    painter.drawPath(igmeasure.separator)


def draw_quarter(painter, quarter):
    # painter.setBrush(QtGui.QBrush(QtGui.QColor('red')))
    painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 255)))
    # for rect in quarter.note_rects:
    #     painter.drawRect(rect)
    painter.setBrush(QtGui.QBrush(QtGui.QColor('black')))
    painter.drawPath(quarter.bodies)
    painter.drawPath(quarter.connections)
    painter.drawPath(quarter.alterations)
    for rest in quarter.rests:
        painter.drawPath(rest)


def draw_keyspace(painter, igkeyspace):
    painter.setBrush(QtGui.QBrush(QtGui.QColor('black')))
    painter.setPen(QtGui.QPen(QtGui.QColor('black')))
    # painter.drawRect(igkeyspace.rect)
    painter.drawPath(igkeyspace.staff_lines)
    painter.drawPath(igkeyspace.key)