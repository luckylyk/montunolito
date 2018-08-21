

import os
from PyQt5 import QtWidgets, QtCore, QtGui
from montunolito.core.solfege import NOTES
from painting import draw_drag_path, draw_background

from interactive import (
    IGNoteSelecter, IGFunctionSelecter, IGChordGrid, IGSelectionSquare)

from geometries import (
    get_noteselecter_rect, get_functionselecter_rect, GLOBAL_WIDTH,
    get_staffs_rect, get_drag_path, get_chordgrid_rect,
    get_chordgrid_minimumsize, get_chord_constructor_size)


ICONDIR = os.path.dirname(__file__)
def icon(filename):
    return QtGui.QIcon(os.path.join(ICONDIR, 'icons', filename))


class ChordGridView(QtWidgets.QWidget):
    def __init__(self, chords=None, parent=None):
        super().__init__(parent=parent)
        self.setMaximumWidth(GLOBAL_WIDTH)

        self.chordgrid_editor = ChordGridWidget(chords)
        self.menu = ChordGridMenu()
        self.menu.tonalityRequested.connect(self.chordgrid_editor.set_tonality)

        self._scroll_area = QtWidgets.QScrollArea()
        self._scroll_area.setWidget(self.chordgrid_editor)
        self._scroll_area.setWidgetResizable(True)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.menu)
        self.layout.addWidget(self._scroll_area)

        # horrible hack to pass the key events from children widget
        self.keyPressEvent = self.chordgrid_editor.keyPressEvent
        self.keyReleaseEvent = self.chordgrid_editor.keyReleaseEvent


class ChordGridMenu(QtWidgets.QWidget):
    newRequested = QtCore.pyqtSignal()
    openRequested = QtCore.pyqtSignal()
    saveRequested = QtCore.pyqtSignal()
    addRequested = QtCore.pyqtSignal()
    deleteRequested = QtCore.pyqtSignal()
    cutRequested = QtCore.pyqtSignal()
    copyRequested = QtCore.pyqtSignal()
    pasteRequested = QtCore.pyqtSignal()
    undoRequested = QtCore.pyqtSignal()
    redoRequested = QtCore.pyqtSignal()
    tonalityRequested = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.new = QtWidgets.QAction(icon('new.png'), '', parent=self)
        self.new.triggered.connect(self.newRequested.emit)
        self.open = QtWidgets.QAction(icon('open.png'), '', parent=self)
        self.open.triggered.connect(self.openRequested.emit)
        self.save = QtWidgets.QAction(icon('save.png'), '', parent=self)
        self.save.triggered.connect(self.saveRequested.emit)

        self.add = QtWidgets.QAction(icon('add.png'), '', parent=self)
        self.add.triggered.connect(self.addRequested.emit)
        self.delete = QtWidgets.QAction(icon('delete.png'), '', parent=self)
        self.delete.triggered.connect(self.deleteRequested.emit)

        self.cut = QtWidgets.QAction(icon('cut.png'), '', parent=self)
        self.cut.triggered.connect(self.cutRequested.emit)
        self.copy = QtWidgets.QAction(icon('copy.png'), '', parent=self)
        self.copy.triggered.connect(self.copyRequested.emit)
        self.paste = QtWidgets.QAction(icon('paste.png'), '', parent=self)
        self.paste.triggered.connect(self.pasteRequested.emit)

        self.undo = QtWidgets.QAction(icon('undo.png'), '', parent=self)
        self.undo.triggered.connect(self.undoRequested.emit)
        self.redo = QtWidgets.QAction(icon('redo.png'), '', parent=self)
        self.redo.triggered.connect(self.redoRequested.emit)

        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.addAction(self.new)
        self.toolbar.addAction(self.open)
        self.toolbar.addAction(self.save)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.cut)
        self.toolbar.addAction(self.copy)
        self.toolbar.addAction(self.paste)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.add)
        self.toolbar.addAction(self.delete)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.undo)
        self.toolbar.addAction(self.redo)

        self.tonality_label = QtWidgets.QLabel('tonality display:')
        self.tonality_combo = QtWidgets.QComboBox()
        self.tonality_combo.addItems(NOTES)
        method = self.tonalityRequested.emit
        self.tonality_combo.currentIndexChanged.connect(method)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 10, 0)
        self.layout.addWidget(self.toolbar)
        self.layout.addStretch(1)
        self.layout.addWidget(self.tonality_label)
        self.layout.addWidget(self.tonality_combo)


class ChordGridWidget(QtWidgets.QWidget):
    gridModified = QtCore.pyqtSignal()
    lastIndexModified = QtCore.pyqtSignal(object)

    def __init__(self, chords=None, parent=None, tonality=0):
        super().__init__(parent, QtCore.Qt.Window)
        self.setFixedWidth(GLOBAL_WIDTH)
        self.setMouseTracking(True)
        self.selection_mode = False
        self.last_selected = None

        self.tonality = tonality
        self.chords = chords
        self.clicked = False

        noteselecter_rect = get_noteselecter_rect(self.rect())
        functionselecter_rect = get_functionselecter_rect(self.rect())
        staffs_rect = get_staffs_rect(self.rect())
        self.noteselecter = IGNoteSelecter(noteselecter_rect, self.tonality)
        self.functionselecter = IGFunctionSelecter(functionselecter_rect)
        self.igchordgrid = IGChordGrid(staffs_rect, self.chords, self.tonality)
        self.selectionsquare = IGSelectionSquare()

        self.setMinimumSize(get_chordgrid_minimumsize(self.igchordgrid))

    @property
    def chordgrid(self):
        return self.igchordgrid.chordgrid

    def set_chordgrid(self, chordgrid):
        self.igchordgrid.set_chordgrid(chordgrid)
        self.repaint()

    def resizeEvent(self, _):
        self.noteselecter.rect = get_noteselecter_rect(self.rect())
        self.functionselecter.rect = get_functionselecter_rect(self.rect())
        self.igchordgrid.rect = get_staffs_rect(self.rect())
        self.repaint()

    def mouseMoveEvent(self, _):
        self.noteselecter.set_states(cursor(self), self.clicked)
        self.functionselecter.set_states(cursor(self), self.clicked)
        self.igchordgrid.set_hover(cursor(self))
        if self.contructed_chord():
            self.igchordgrid.activate(cursor(self))
        if self.selectionsquare.in_point is not None:
            self.selectionsquare.out_point = cursor(self)
        self.repaint()

    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            return

        self.clicked = True
        self.noteselecter.enable = self.noteselecter.rect.contains(cursor(self))
        self.noteselecter.set_states(cursor(self), self.clicked)
        if self.noteselecter.active_note():
            self.functionselecter.enable = True
            if self.functionselecter.active_chord():
                self.igchordgrid.activate(cursor(self))
        if self.selection_mode not in ('add', 'in_between'):
            self.selection_mode = self.igchordgrid.rect.contains(cursor(self))
            if self.igchordgrid.rect.contains(cursor(self)):
                self.selectionsquare.in_point = cursor(self)
        self.functionselecter.set_states(cursor(self), self.clicked)
        self.repaint()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control:
            self.selection_mode = 'add'

        if event.key() == QtCore.Qt.Key_Shift:
            self.selection_mode = 'in_between'

    def keyReleaseEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Control, QtCore.Qt.Key_Shift):
            self.selection_mode = self.igchordgrid.rect.contains(cursor(self))

        # if event.key() in (QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete):
        #     self.delete_selection()

    def mouseReleaseEvent(self, _):
        self.clicked = False
        chord = self.contructed_chord()
        if chord is not None:
            self.set_active_chord(self.contructed_chord())

        if self.selection_mode not in ('add', 'in_between'):
            self.igchordgrid.clear_selection()
            self.lastIndexModified.emit(None)

        if self.selection_mode not in (False, 'in_between'):
            self.igchordgrid.select_hovered(self.selectionsquare.rect)
            self.igchordgrid.select_staff()
            self.last_selected = self.igchordgrid.hovered_index()
            self.lastIndexModified.emit(self.last_selected)

        if self.selection_mode == 'in_between':
            if self.last_selected is None:
                self.igchordgrid.select_hovered(self.selectionsquare.rect)
                self.last_selected = self.igchordgrid.hovered_index()
                self.lastIndexModified.emit(self.last_selected)
            else:
                index = self.igchordgrid.hovered_index()
                self.igchordgrid.select_range(self.last_selected, index)

        self.selectionsquare.reset()
        self.noteselecter.set_states(cursor(self), self.clicked)
        self.noteselecter.released()
        self.noteselecter.enable = False
        self.functionselecter.enable = False
        self.functionselecter.set_states(cursor(self))
        self.functionselecter.released()
        self.igchordgrid.released()
        self.repaint()

    def paintEvent(self, _):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        draw_background(painter, self.rect())
        self.noteselecter.draw(painter)
        self.functionselecter.draw(painter)
        self.igchordgrid.draw(painter)
        items = [self.noteselecter.active_note(), self.functionselecter.active_chord()]
        path = get_drag_path(items, cursor(self))
        if path:
            draw_drag_path(painter, path)
        self.selectionsquare.draw(painter)
        painter.end()

    def contructed_chord(self):
        note = self.noteselecter.active_note()
        chord = self.functionselecter.active_chord()
        if not all([note, chord]):
            return None
        return {'degree': note.index, 'name': chord.text}

    def set_active_chord(self, chord):
        igchord = self.igchordgrid.igchord(self.igchordgrid.active_index())
        if igchord is not None:
            igchord.set_chord(chord)
        self.gridModified.emit()

    def set_tonality(self, tonality):
        self.noteselecter.set_tonality(tonality)
        self.igchordgrid.tonality = tonality
        for igchord in self.igchordgrid.igchords():
            igchord.set_tonality(tonality)
        self.repaint()

    def delete_selection(self):
        selected_chords = self.igchordgrid.selected_chords()
        for igchord in selected_chords:
            igchord.set_chord(None)
        self.igchordgrid.delete_selected_staffs()
        self.gridModified.emit()
        self.repaint()

    def is_index_selected(self, index):
        return self.igchordgrid.igchord(index).selected

def cursor(widget):
    return widget.mapFromGlobal(QtGui.QCursor.pos())
