


from PyQt5 import QtWidgets, QtCore, QtGui
from montunolito.core.solfege import NOTES
from painting import draw_drag_path, draw_background
from interactive import (
    IGNoteSelecter, IGFunctionSelecter, IGChordGrid, IGSelectionSquare)
from geometries import (
    get_noteselecter_rect, get_functionselecter_rect, GLOBAL_WIDTH,
    get_staffs_rect, get_drag_path)


class ChordGridEditor(QtWidgets.QWidget):
    chordEdited = QtCore.pyqtSignal(object, object)
    # index in chordgrid, montunolito chord as dict

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
        self.noteselecter = IGNoteSelecter(noteselecter_rect, self.tonality)
        self.functionselecter = IGFunctionSelecter(functionselecter_rect)
        self.chordgrid = IGChordGrid(get_staffs_rect(self.rect()), self.chords, self.tonality)
        self.selectionsquare = IGSelectionSquare()

    def resizeEvent(self, _):
        self.noteselecter.rect = get_noteselecter_rect(self.rect())
        self.functionselecter.rect = get_functionselecter_rect(self.rect())
        self.chordgrid.rect = get_staffs_rect(self.rect())
        self.repaint()

    def cursor(self):
        return self.mapFromGlobal(QtGui.QCursor.pos())

    def mouseMoveEvent(self, _):
        self.noteselecter.set_states(self.cursor(), self.clicked)
        self.functionselecter.set_states(self.cursor(), self.clicked)
        self.chordgrid.set_hover(self.cursor())
        if self.get_contructed_chord():
            self.chordgrid.activate(self.cursor())

        if self.selectionsquare.in_point is not None:
            self.selectionsquare.out_point = self.cursor()
        self.repaint()

    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            return
        self.clicked = True
        self.noteselecter.enable = self.noteselecter.rect.contains(self.cursor())
        self.noteselecter.set_states(self.cursor(), self.clicked)
        if self.noteselecter.active_note():
            self.functionselecter.enable = True
            if self.functionselecter.active_chord():
                self.chordgrid.activate(self.cursor())
        if self.selection_mode not in ('add', 'in_between'):
            self.selection_mode = self.chordgrid.rect.contains(self.cursor())
            if self.chordgrid.rect.contains(self.cursor()):
                self.selectionsquare.in_point = self.cursor()
        self.functionselecter.set_states(self.cursor(), self.clicked)
        self.repaint()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control:
            self.selection_mode = 'add'

        if event.key() == QtCore.Qt.Key_Shift:
            self.selection_mode = 'in_between'

    def keyReleaseEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Control, QtCore.Qt.Key_Shift):
            self.selection_mode = self.chordgrid.rect.contains(self.cursor())

        if event.key() in (QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete):
            for igchord in self.chordgrid.selected_chords():
                igchord.set_chord(None)
            self.repaint()

    def mouseReleaseEvent(self, _):
        self.clicked = False
        chord = self.get_contructed_chord()
        if chord is not None:
            self.modify_active_chord(self.get_contructed_chord())

        if self.selection_mode not in (False, 'in_between'):
            self.chordgrid.clear_selection()
            self.chordgrid.select_hovered(self.selectionsquare.rect)
            self.last_selected = self.chordgrid.hovered_index()

        if self.selection_mode == 'in_between':
            self.chordgrid.clear_selection()
            if self.last_selected is None:
                self.chordgrid.select_hovered(self.selectionsquare.rect)
                self.last_selected = self.chordgrid.hovered_index()
            else:
                index = self.chordgrid.hovered_index()
                self.chordgrid.select_range(self.last_selected, index)


        self.selectionsquare.reset()
        self.noteselecter.set_states(self.cursor(), self.clicked)
        self.noteselecter.released()
        self.noteselecter.enable = False
        self.functionselecter.enable = False
        self.functionselecter.set_states(self.cursor())
        self.functionselecter.released()
        self.chordgrid.released()
        self.repaint()

    def paintEvent(self, _):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def get_contructed_chord(self):
        note = self.noteselecter.active_note()
        chord = self.functionselecter.active_chord()
        if not all([note, chord]):
            return None
        return {'degree': note.index, 'name': chord.text}

    def modify_active_chord(self, chord):
        igchord = self.chordgrid.igchord(self.chordgrid.active_index())
        if igchord is not None:
            igchord.set_chord(chord)

    def get_drag_path(self):
        points = []

        note = self.noteselecter.active_note()
        if note:
            points.append(note.rect.center())
        chord = self.functionselecter.active_chord()
        if chord:
            points.append(chord.rect.center())

        points.append(self.cursor())
        if len(points) > 1:
            return get_drag_path(points)
        else:
            return None

    def paint(self, painter):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        draw_background(painter, self.rect())
        self.noteselecter.draw(painter)
        self.functionselecter.draw(painter)
        self.chordgrid.draw(painter)
        path = self.get_drag_path()
        if path:
            draw_drag_path(painter, path)
        self.selectionsquare.draw(painter)