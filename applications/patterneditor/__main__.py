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
from graph import Pattern
from fingerstates import Fingerstates
from draws import draw_background, draw_note_path
from coordinates import get_note_path, get_beam_tail_path, get_beams_connection_path, get_eighth_rest_path
from config import (
    ROWS_TOP, ROWS_LEFT, ROWS_SPACING, ROWS_WIDTH, ROWS_BOTTOM_SPACE,
    ROWS_HEADER_SPACE, INDEX_HEIGHT, INDEX_WIDTH, INDEX_SPACING, ROWS_PADDING)


class MainTest(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self._pattern = Pattern(PATTERNS['montuno'].copy())
        self._row = None

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.repaint()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._pattern.set_selected_states(self.cursor())
            self.repaint()
    #     if event.button() == QtCore.Qt.LeftButton:
    #         append_quarter_row(self._pattern)
    #         self.repaint()
    #         self.setMinimumSize(self.sizeHint())
    #         return

    #     if self._row is None:
    #         return

    #     if event.button() == QtCore.Qt.RightButton:
    #         append_fingerstates_indexes(self._pattern, (1, 3, 5, 7), self._row)
    #     elif event.button() == QtCore.Qt.MiddleButton:
    #         index = self._row, self._column
    #         delete_fingerstates_indexes(self._pattern, index)
    #     self.setMinimumSize(self.sizeHint())
    #     self.repaint()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            balloon = FingerstatesBalloon((3, 0, 6, 2), parent=self)
            pos = self.cursor()
            balloon.move(pos.x() - 100, pos.y() - 200)
            balloon.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def cursor(self):
        return self.mapFromGlobal(QtGui.QCursor.pos())

    def paint(self, painter):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        draw_background(painter, self.rect())
        self._pattern.draw(painter, self.cursor())

    def sizeHint(self):
        width = (
            ((ROWS_WIDTH + ROWS_SPACING) * len(self._pattern.rows)) + 
            (ROWS_LEFT * 2))

        rows = self._pattern.rows
        longer_row_len = max([len(row) for row in rows]) if rows else 0
        height = (
            (ROWS_TOP * 2) +
            ROWS_HEADER_SPACE +
            ROWS_BOTTOM_SPACE +
            ((INDEX_HEIGHT + INDEX_SPACING) * longer_row_len))
        return QtCore.QSize(width, height)

import sys
application = QtGui.QApplication(sys.argv)
windows = MainTest()
windows.show()
application.exec_()