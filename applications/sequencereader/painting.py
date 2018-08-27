from PyQt5 import QtGui


def draw_measure(painter, igmeasure):
    painter.setBrush(QtGui.QBrush(QtGui.QColor('red')))
    painter.setPen(QtGui.QPen(QtGui.QColor('black')))
    painter.drawRect(igmeasure.rect)