from PyQt5 import QtWidgets, QtGui
from sequencereader.interactive import IGMeasure
from sequencereader.geometries import extract_measures_rects
from montunolito.core.utils import split_array, set_array_lenght_multiple


class SequenceReader(QtWidgets.QWidget):
    def __init__(self, sequence, parent=None):
        super().__init__(parent)
        self._sequence = set_array_lenght_multiple(
            sequence, multiple=8, default=[])

        self._igmeasures = [
            IGMeasure(None, s) for s in split_array(sequence, 8)]

    def update_geometries(self):
        rects = set_array_lenght_multiple(
            extract_measures_rects(self.rect()),
            len(self._igmeasures),
            default=None)

        for rect, igmeasure in zip(rects, self._igmeasures):
            igmeasure.rect = rect

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