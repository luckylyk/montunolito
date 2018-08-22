from functools import partial
import os
from PyQt5 import QtWidgets, QtGui, QtCore

from patterneditor.interactive import IGPattern
from patterneditor.context import DrawContext
from patterneditor.painting import draw_background, draw_menu_background
from patterneditor.geometries import get_pattern_size, get_balloon_spike_point, GRID_SPACING
from patterneditor.themes import THEMES


class PatternEditorWidget(QtWidgets.QWidget):

    def __init__(self, pattern, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.drawcontext = DrawContext()
        self.graph = GraphWidget(pattern, self.drawcontext)
        self.menu = MenuWidget()

        self._scroll_area = QtWidgets.QScrollArea()
        self._scroll_area.setWidget(self.graph)
        self._scroll_area.setWidgetResizable(True)
        # hack to deactivate scroll on wheelEvent
        self._scroll_area.wheelEvent = lambda x: None

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.menu)
        self.layout.addWidget(self._scroll_area)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control:
            self.graph.add_selection_context = True

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control:
            self.graph.add_selection_context = False

    def set_theme(self, theme):
        self.drawcontext.set_theme(theme)
        self.graph.repaint()
        self.menu.repaint()


ICONDIR = os.path.dirname(__file__)
def icon(filename):
    return QtGui.QIcon(os.path.join(ICONDIR, 'icons', filename))


class MenuWidget(QtWidgets.QWidget):
    newPatternRequested = QtCore.pyqtSignal()
    openPatternRequested = QtCore.pyqtSignal()
    savePatternRequested = QtCore.pyqtSignal()
    undoRequested = QtCore.pyqtSignal()
    redoRequested = QtCore.pyqtSignal()
    deleteRequested = QtCore.pyqtSignal()
    themesRequested = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.new = QtWidgets.QAction(icon('new.png'), '', parent=self)
        self.new.triggered.connect(self.newPatternRequested.emit)
        self.open = QtWidgets.QAction(icon('open.png'), '', parent=self)
        self.open.triggered.connect(self.openPatternRequested.emit)
        self.save = QtWidgets.QAction(icon('save.png'), '', parent=self)
        self.save.triggered.connect(self.savePatternRequested.emit)

        self.delete = QtWidgets.QAction(icon('delete.png'), '', parent=self)
        self.delete.triggered.connect(self.deleteRequested.emit)

        self.undo = QtWidgets.QAction(icon('undo.png'), '', parent=self)
        self.undo.triggered.connect(self.savePatternRequested.emit)
        self.redo = QtWidgets.QAction(icon('redo.png'), '', parent=self)
        self.redo.triggered.connect(self.redoRequested.emit)

        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.addAction(self.new)
        self.toolbar.addAction(self.open)
        self.toolbar.addAction(self.save)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.delete)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.undo)
        self.toolbar.addAction(self.redo)

        self.themes_label = QtWidgets.QLabel('theme:')
        self.themes_combo = QtWidgets.QComboBox()
        self.themes_combo.addItems(THEMES)
        method = self.themesRequested.emit
        self.themes_combo.currentTextChanged.connect(method)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 10, 0)
        self.layout.addWidget(self.toolbar)
        self.layout.addStretch(1)
        self.layout.addWidget(self.themes_label)
        self.layout.addWidget(self.themes_combo)


class GraphWidget(QtWidgets.QWidget):
    figureClicked = QtCore.pyqtSignal(object, object)
    behaviorClicked = QtCore.pyqtSignal(object, object)
    connectionClicked = QtCore.pyqtSignal(object, object, object)
    rowClicked = QtCore.pyqtSignal(object)

    def __init__(self, pattern, drawcontext=None, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding)
        self._drawcontext = drawcontext or DrawContext()
        self.pattern = IGPattern(
            pattern.copy(),
            drawcontext=self._drawcontext)
        self._row = None
        self.add_selection_context = False
        self.setMinimumSize(self.sizeHint())

    def set_pattern(self, pattern):
        selected_indexes = [
            i.index for i in self.pattern.selected_indexes() if i.selected]
        self.pattern = IGPattern(
            pattern.copy(),
            drawcontext=self._drawcontext)
        self.pattern.select_indexes(selected_indexes)
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
            self.pattern.set_selected_states(
                self.cursor(), add=self.add_selection_context)
            self.repaint()
        action, item = self.pattern.get_index_action_hovered(self.cursor())
        if action is None:
            return

        if action == 'figure':
            point = self.mapToGlobal(item.figure_rect.center())
            self.figureClicked.emit(item.index, point)
        elif action == 'behavior':
            point = self.mapToGlobal(item.behavior_rect.center())
            self.behaviorClicked.emit(item.index, point)
        elif action == 'connection':
            point = self.mapToGlobal(item.handler_rect.center())
            in_index = item.in_index.index
            out_index = item.out_index.index
            self.connectionClicked.emit(in_index, out_index, point)
        elif action == 'row':
            self.rowClicked.emit(item.number)


    def paintEvent(self, _):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def cursor(self):
        return self.mapFromGlobal(QtGui.QCursor.pos())

    def paint(self, painter):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        draw_background(painter, self._drawcontext, GRID_SPACING, self.rect())
        self.pattern.draw(painter, self.cursor())

    def sizeHint(self):
        return get_pattern_size(self._drawcontext, self.pattern)


class NewMenu(QtWidgets.QMenu):

    def __init__(self, templates, parent=None):
        super().__init__(parent)
        self.result = None
        self._empty = QtWidgets.QAction('empty', parent=self)
        self.addAction(self._empty)
        self.addSeparator()
        for template in templates:
            action = QtWidgets.QAction(template, parent=self)
            action.name = template
            self.addAction(action)

    def set_result(self, result):
        self.result = result

    def exec_(self):
        result = super().exec_(QtGui.QCursor.pos())
        if result is not None and result.text() != 'empty':
            return result.text()


class ThemesMenu(QtWidgets.QMenu):

    def __init__(self, themes, parent=None):
        super().__init__(parent)
        self.result = None
        self.addSeparator()
        for theme in themes:
            action = QtWidgets.QAction(theme, parent=self)
            action.name = theme
            self.addAction(action)

    def set_result(self, result):
        self.result = result

    def exec_(self):
        result = super().exec_(QtGui.QCursor.pos())
        if result:
            return result.text()
