from PyQt5 import QtGui, QtCore


def draw_measure(painter, igmeasure):
    painter.setBrush(QtGui.QBrush(QtGui.QColor('black')))
    painter.setPen(QtGui.QPen(QtGui.QColor('black')))
    # painter.drawRect(igmeasure.rect)
    painter.drawPath(igmeasure.staff_lines)
    painter.drawPath(igmeasure.separator)
    if not igmeasure.positions: return
    option = QtGui.QTextOption()
    option.setAlignment(QtCore.Qt.AlignCenter)
    for i, p in enumerate(igmeasure.positions):
        painter.drawText(QtCore.QRectF(p.x() - 15, p.y() - 15, 30, 30), str(i), option)


def draw_quarter(painter, quarter):
    # painter.setBrush(QtGui.QBrush(QtGui.QColor('red')))
    painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 255)))
    # for rect in quarter.note_rects:
    #     painter.drawRect(rect)
    painter.setBrush(QtGui.QBrush(QtGui.QColor('black')))
    painter.drawPath(quarter.bodies)
    painter.drawPath(quarter.connections)
    painter.drawPath(quarter.alterations)
    for lines in quarter.extralines:
        painter.drawPath(lines)
    for rest in quarter.rests:
        painter.drawPath(rest)


def draw_keyspace(painter, igkeyspace):
    painter.setBrush(QtGui.QBrush(QtGui.QColor('black')))
    painter.setPen(QtGui.QPen(QtGui.QColor('black')))
    # painter.drawRect(igkeyspace.rect)
    painter.drawPath(igkeyspace.staff_lines)
    painter.drawPath(igkeyspace.key)