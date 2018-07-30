import os
import sys

_current_dir = os.path.dirname(os.path.realpath(__file__))
APPLICATIONS_FOLDER = os.path.dirname(_current_dir)
MONTUNOLITO_FOLDER = os.path.dirname(os.path.dirname(_current_dir))
sys.path.insert(0, APPLICATIONS_FOLDER)
sys.path.insert(0, MONTUNOLITO_FOLDER)


from PyQt5 import QtWidgets, QtGui, QtCore

from montunolito.patterns import PATTERNS

from balloons import FigureBalloon, BehaviorBalloon, ConnectionBalloon
from graph import IGPattern
from draws import draw_background
from coordinates import (
    get_balloon_spike_point, GRID_SPACING,
    ROWS_TOP, ROWS_LEFT, ROWS_SPACING, ROWS_WIDTH, ROWS_BOTTOM_SPACE,
    ROWS_HEADER_SPACE, INDEX_HEIGHT, INDEX_SPACING)


class MainTest(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self._pattern = IGPattern(PATTERNS['montuno'].copy())
        self._row = None

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.repaint()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._pattern.set_selected_states(self.cursor())
            self.repaint()
        action, item = self._pattern.get_index_action_hovered(self.cursor())
        if action is None:
            return

        if action == 'fingerstate':
            balloon = FigureBalloon(item.figure(), parent=None)
            pos = item._figure_rect.center()
        elif action == 'behavior':
            balloon = BehaviorBalloon(parent=None)
            pos = item._behavior_rect.center()
        elif action == 'connection':
            balloon = ConnectionBalloon(item, parent=None)
            pos = item._handler_rect.center()
        spike_tip = get_balloon_spike_point(balloon.rect())
        balloon.move(pos - self.mapFromGlobal(spike_tip))
        balloon.exec_()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def cursor(self):
        return self.mapFromGlobal(QtGui.QCursor.pos())

    def paint(self, painter):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        draw_background(painter,GRID_SPACING, self.rect())
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
application = QtWidgets.QApplication(sys.argv)
windows = MainTest()
windows.show()
application.exec_()