
from PyQt5 import QtWidgets, QtGui, QtCore

from montunolito.core.utils import split_array, set_array_lenght_multiple
from sequencereader.rules import Signature, SIGNATURES
from sequencereader.interactive import IGMeasure, IGKeySpace, IGSignature
from sequencereader.geometries import (
    extract_measures_rects, extract_rects_keyspaces, extract_signature_rects)

from itertools import cycle


SIGNATURES = cycle(SIGNATURES)


class SequenceReaderWidget(QtWidgets.QWidget):

    def __init__(self, sequence, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.sequencereader = SequenceReader(sequence)

        self._scroll_area = QtWidgets.QScrollArea()
        self._scroll_area.setWidget(self.sequencereader)
        self._scroll_area.setWidgetResizable(True)
        # hack to deactivate scroll on wheelEvent
        # self._scroll_area.wheelEvent = lambda x: None

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self._scroll_area)


class SequenceReader(QtWidgets.QWidget):
    def __init__(self, sequence, signature='A', mode='major', parent=None):
        super().__init__(parent)
        self._sequence = set_array_lenght_multiple(
            sequence, multiple=8, default=[])

        self._signature = Signature()
        self._signature.set_values(signature, mode)

        rects = extract_signature_rects(self.rect(), self._signature)
        self._igsignatures = [
            IGSignature(rect, self._signature) for rect in rects]

        self._igmeasures = [
            IGMeasure(None, s) for s in split_array(sequence, 8)]
        rects = extract_rects_keyspaces(self.rect())
        self._igmeasures[-1].end = True
        self._igkeyspaces = [IGKeySpace(rect) for rect in rects]

    def update_geometries(self):
        rects = set_array_lenght_multiple(
            extract_measures_rects(self.rect(), self._signature),
            len(self._igmeasures),
            default=None)

        for rect, igmeasure in zip(rects, self._igmeasures):
            igmeasure.set_rect(rect)

        rects = extract_rects_keyspaces(self.rect())
        self._igkeyspaces = [IGKeySpace(rect) for rect in rects]

        rects = extract_signature_rects(self.rect(), self._signature)
        self._igsignatures = [
            IGSignature(rect, self._signature) for rect in rects]

    def resizeEvent(self, _):
        self.update_geometries()
        self.repaint()

    def paintEvent(self, _):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def mousePressEvent(self, _):
        mode = 'major' if self._signature.mode == 'minor' else 'minor'
        self._signature.set_values(mode=mode)
        self.update_geometries()
        self.repaint()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self._signature.set_values(signature=next(SIGNATURES))
            self.update_geometries()
            self.repaint()

    def cursor(self):
        return self.mapFromGlobal(QtGui.QCursor.pos())

    def paint(self, painter):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        for igmeasure in self._igmeasures:
            igmeasure.draw(painter)
        for igkeyspace in self._igkeyspaces:
            igkeyspace.draw(painter)
        for igsignature in self._igsignatures:
            igsignature.draw(painter)
