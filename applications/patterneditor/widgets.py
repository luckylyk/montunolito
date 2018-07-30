from PyQt5 import QtWidgets, QtGui, QtCore

from balloons import FigureBalloon, BehaviorBalloon, ConnectionBalloon
from graph import IGPattern
from context import DrawContext
from painting import draw_background, draw_menu_background
from geometries import get_pattern_size, get_balloon_spike_point, GRID_SPACING
from menu import Menu


class PatternEditorWidget(QtWidgets.QWidget):

    def __init__(self, pattern, parent=None):
        super().__init__(parent=parent)
        self.graph = GraphWidget(pattern)
        self.menu = MenuWidget()

        self._scroll_area = QtWidgets.QScrollArea()
        self._scroll_area.setWidget(self.graph)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.wheelEvent = lambda x: None

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.menu)
        self.layout.addWidget(self._scroll_area)


class MenuWidget(QtWidgets.QWidget):
    newPatternRequested = QtCore.pyqtSignal()
    openPatternRequested = QtCore.pyqtSignal()
    savePatternRequested = QtCore.pyqtSignal()
    undoRequested = QtCore.pyqtSignal()
    redoRequested = QtCore.pyqtSignal()
    deleteRequested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(50)
        self.setMouseTracking(True)
        self.signals = (
            self.newPatternRequested,
            self.openPatternRequested,
            self.savePatternRequested,
            self.undoRequested,
            self.redoRequested,
            self.deleteRequested)
        self._menu = Menu(self.rect())

    def paintEvent(self, _):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self._menu.set_hovered_states(self.cursor())
        self.repaint()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._menu.set_clicked_states(self.cursor())
            self.repaint()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            index = self._menu.hovered_index()
            if index is not None:
                self.signals[index].emit()
            self._menu.set_clicked_states(self.cursor(), False)
            self.repaint()

    def leaveEvent(self, _):
        self._menu.set_clicked_states(self.cursor(), False)

    def cursor(self):
        return self.mapFromGlobal(QtGui.QCursor.pos())

    def paint(self, painter):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        draw_menu_background(painter, self.rect())
        self._menu.draw(painter)


class GraphWidget(QtWidgets.QWidget):
    figureClicked = QtCore.pyqtSignal(object, object)
    behaviorClicked = QtCore.pyqtSignal(object, object)
    connectionClicked = QtCore.pyqtSignal(object, object)

    def __init__(self, pattern, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding)
        self._drawcontext = DrawContext()
        self.pattern = IGPattern(
            pattern.copy(),
            drawcontext=self._drawcontext)
        self._row = None
        self.setMinimumSize(self.sizeHint())

    def set_pattern(self, pattern):
        self.pattern = IGPattern(
            pattern.copy(),
            drawcontext=self._drawcontext)
        self.repaint()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.repaint()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self._drawcontext.increase_size()
        else:
            self._drawcontext.decrease_size()

        self.pattern.update_geometries()
        self.setMinimumSize(self.sizeHint())
        self.repaint()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.pattern.set_selected_states(self.cursor())
            self.repaint()
        action, item = self.pattern.get_index_action_hovered(self.cursor())
        if action is None:
            return

        if action == 'figure':
            balloon = FigureBalloon(item, parent=None)
            pos = item._figure_rect.center()
        elif action == 'behavior':
            balloon = BehaviorBalloon(item, parent=None)
            pos = item._behavior_rect.center()
        elif action == 'connection':
            balloon = ConnectionBalloon(item, parent=None)
            pos = item._handler_rect.center()
        spike_tip = get_balloon_spike_point(self._drawcontext, balloon.rect())
        balloon.move(pos - self.mapFromGlobal(spike_tip))
        balloon.exec_()

    def paintEvent(self, _):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def cursor(self):
        return self.mapFromGlobal(QtGui.QCursor.pos())

    def paint(self, painter):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        draw_background(painter, GRID_SPACING, self.rect())
        self.pattern.draw(painter, self.cursor())

    def sizeHint(self):
        return get_pattern_size(self._drawcontext, self.pattern)