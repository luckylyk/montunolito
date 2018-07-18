import os
import sys

_current_dir = os.path.dirname(os.path.realpath(__file__))
APPLICATIONS_FOLDER = os.path.dirname(_current_dir)
MONTUNOLITO_FOLDER = os.path.dirname(os.path.dirname(_current_dir))
sys.path.insert(0, APPLICATIONS_FOLDER)
sys.path.insert(0, MONTUNOLITO_FOLDER)


from PyQt4 import QtGui, QtCore

from balloons import *
from graph import *


class MainTest(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 500)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def paint(self, painter):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        draw_background(painter, self.rect())
        column = QtCore.QRect(50, 50, 150, 300)
        draw_column_background(painter, column, 1)
        column = QtCore.QRect(250, 50, 150, 300)
        draw_column_background(painter, column, 2)
        column = QtCore.QRect(450, 50, 150, 300)
        draw_column_background(painter, column, 3)
        column = QtCore.QRect(650, 50, 150, 300)
        draw_column_background(painter, column, 4)

        index = QtCore.QRect(60, 100, 130, 25)
        draw_index(painter, index, 0, hover=0)
        index = QtCore.QRect(60, 140, 130, 25)
        draw_index(painter, index, 25, hover=3)
        index = QtCore.QRect(60, 180, 130, 25)
        draw_index(painter, index, 50, hover=2)
        index = QtCore.QRect(60, 220, 130, 25)
        draw_index(painter, index, 75, hover=4)
        index = QtCore.QRect(60, 260, 130, 25)
        draw_index(painter, index, 100, hover=5)

import sys
application = QtGui.QApplication(sys.argv)
windows = MainTest()
windows.show()
application.exec_()