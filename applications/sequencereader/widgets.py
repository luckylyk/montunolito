
from PyQt5 import QtWidgets, QtGui, QtCore
from montunolito.core.utils import split_array, set_array_lenght_multiple

# from sequencereader.interactive import IGMeasure, IGKeySpace
from sequencereader.geometries import (
    extract_measures_rects, extract_rects_keyspaces, extract_notes_rects,
    extract_quarters_rects)
from sequencereader.shapes import get_notes_path, get_notes_connections_path
from sequencereader.staff import get_note_position, get_standard_staff_lines, get_additional_staff_lines, get_beams_directions

from montunolito.core.solfege import NOTES, SCALE_LENGTH
from montunolito.core.utils import remap_number


def get_sample_sequence():
    a = [48]
    b = [40, 60]
    c = [65, 66, 75]
    d = [43, 50]
    return (a, [], b, d)


class Test(QtWidgets.QWidget):
    sequence = [33, 43, 44, 45, 75], [38, 45], [52], [33, 43, 44, 56, 60]
    sequence = get_sample_sequence()

    def paintEvent(self, _):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QBrush(QtGui.QColor('black')))
        quarterrects = extract_quarters_rects(self.rect())
        connections = []
        for quarterrect in quarterrects:
            noterects = extract_notes_rects(quarterrect)
            directions = get_beams_directions(self.sequence)
            for notes, noterect, d in zip(self.sequence, noterects, directions):
                path = get_notes_path(noterect, notes, direction=d)
                painter.drawPath(path)
            connections.append(get_notes_connections_path(noterects, self.sequence))
        painter.drawPath(get_standard_staff_lines(self.rect()))
        for connection in connections:
            painter.drawPath(connection)
        painter.end()


class SequenceReader(QtWidgets.QWidget):
    def __init__(self, sequence, parent=None):
        super().__init__(parent)
        self._sequence = set_array_lenght_multiple(
            sequence, multiple=8, default=[])

        self._igmeasures = [
            IGMeasure(None, s) for s in split_array(sequence, 8)]
        rects = extract_rects_keyspaces(self.rect())
        self._igkeyspaces = [IGKeySpace(rect) for rect in rects]

    def update_geometries(self):
        rects = set_array_lenght_multiple(
            extract_measures_rects(self.rect()),
            len(self._igmeasures),
            default=None)
        for rect, igmeasure in zip(rects, self._igmeasures):
            igmeasure.set_rect(rect)
        rects = extract_rects_keyspaces(self.rect())
        self._igkeyspaces = [IGKeySpace(rect) for rect in rects]

    def resizeEvent(self, event):
        self.update_geometries()
        self.repaint()

    def paintEvent(self, _):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def cursor(self):
        return self.mapFromGlobal(QtGui.QCursor.pos())

    def paint(self, painter):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        for igmeasure in self._igmeasures:
            igmeasure.draw(painter)
        for igkeyspace in self._igkeyspaces:
            igkeyspace.draw(painter)