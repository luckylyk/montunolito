import os
import sys

_current_dir = os.path.dirname(os.path.realpath(__file__))
APPLICATIONS_FOLDER = os.path.dirname(_current_dir)
MONTUNOLITO_FOLDER = os.path.dirname(os.path.dirname(_current_dir))
sys.path.insert(0, APPLICATIONS_FOLDER)
sys.path.insert(0, MONTUNOLITO_FOLDER)


from PyQt4 import QtGui, QtCore

from montunolito.patterns import PATTERNS
from montunolito.core.pattern import (
    get_new_pattern, append_quarter_row, append_fingerstates_indexes,
    delete_fingerstates_indexes)

from balloons import *
from graph import *
from draws import *
from config import ROWS_SPACING


class MainTest(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 500)
        self.setMouseTracking(True)
        self._pattern = get_new_pattern()
        self._row = None

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.repaint()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            append_quarter_row(self._pattern)
            self.repaint()
            return

        if self._row is None:
            return

        if event.button() == QtCore.Qt.RightButton:
            append_fingerstates_indexes(self._pattern, (1, 3, 5, 7), self._row)
        elif event.button() == QtCore.Qt.MiddleButton:
            index = self._row, self._column
            delete_fingerstates_indexes(self._pattern, index)
        self.repaint()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def paint(self, painter):
        cursor = self.mapFromGlobal(QtGui.QCursor.pos())
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        draw_background(painter, self.rect())
        self._row, self._column = draw_pattern(painter, self._pattern, cursor)

import sys
application = QtGui.QApplication(sys.argv)
windows = MainTest()
windows.show()
application.exec_()