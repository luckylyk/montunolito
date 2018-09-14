
import os

from PyQt5 import QtWidgets, QtGui, QtCore

from montunolito.core.utils import split_array, set_array_lenght_multiple
from sequencereader.rules import Signature, SIGNATURES
from sequencereader.interactive import IGMeasure, IGKeySpace, IGSignature
from sequencereader.geometries import (
    extract_measures_rects, extract_rects_keyspaces, extract_signature_rects,
    get_widget_size)


class SequenceReaderWidget(QtWidgets.QWidget):

    def __init__(self, sequence, signature, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.musicsheet = MusicSheetWidget(sequence, signature)
        self.menu = MenuWidget()

        self._scroll_area = QtWidgets.QScrollArea()
        self._scroll_area.setWidget(self.musicsheet)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setAlignment(QtCore.Qt.AlignHCenter)
        # hack to deactivate scroll on wheelEvent
        # self._scroll_area.wheelEvent = lambda x: None

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.menu)
        self.layout.addWidget(self._scroll_area)

        self.sizeHint = lambda: QtCore.QSize(1250, 600)


ICONDIR = os.path.dirname(__file__)
def icon(filename):
    return QtGui.QIcon(os.path.join(ICONDIR, 'icons', filename))


class MenuWidget(QtWidgets.QWidget):
    openSequenceRequested = QtCore.pyqtSignal()
    saveSequenceRequested = QtCore.pyqtSignal()
    exportWavRequested = QtCore.pyqtSignal()
    exportMidiRequested = QtCore.pyqtSignal()
    exportXmlRequested = QtCore.pyqtSignal()
    tonalityChanged = QtCore.pyqtSignal(str)
    modeChanged = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.open = QtWidgets.QAction(icon('open.png'), '', parent=self)
        self.open.triggered.connect(self.openSequenceRequested.emit)
        self.save = QtWidgets.QAction(icon('save.png'), '', parent=self)
        self.save.triggered.connect(self.saveSequenceRequested.emit)
        self.wav = QtWidgets.QAction(icon('wav.png'), '', parent=self)
        self.wav.triggered.connect(self.exportWavRequested.emit)
        self.mid = QtWidgets.QAction(icon('mid.png'), '', parent=self)
        self.mid.triggered.connect(self.exportMidiRequested.emit)
        self.xml = QtWidgets.QAction(icon('xml.png'), '', parent=self)
        self.xml.triggered.connect(self.exportXmlRequested.emit)

        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.addAction(self.open)
        self.toolbar.addAction(self.save)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.wav)
        self.toolbar.addAction(self.mid)
        self.toolbar.addAction(self.xml)

        self.tonality_label = QtWidgets.QLabel('tonality:')
        self.tonality_combo = QtWidgets.QComboBox()
        self.tonality_combo.addItems(SIGNATURES)
        self.tonality_combo.setCurrentText('A')
        method = self.tonalityChanged.emit
        self.tonality_combo.currentTextChanged.connect(method)

        self.mode_combo = QtWidgets.QComboBox()
        self.mode_combo.addItems(('major', 'minor'))
        self.mode_combo.setCurrentText('minor')
        method = self.modeChanged.emit
        self.mode_combo.currentTextChanged.connect(method)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 10, 0)
        self.layout.addWidget(self.toolbar)
        self.layout.addStretch(1)
        self.layout.addWidget(self.tonality_label)
        self.layout.addWidget(self.tonality_combo)
        self.layout.addWidget(self.mode_combo)


class MusicSheetWidget(QtWidgets.QWidget):
    def __init__(self, sequence, signature, parent=None):
        super().__init__(parent)
        self.sequence = set_array_lenght_multiple(
            sequence, multiple=8, default=[])

        self._signature = signature

        self._igsignatures = []
        self._igmeasures = []
        self._igkeyspaces = []
        self.update()

    def set_sequence(self, sequence):
        self.sequence = set_array_lenght_multiple(
            sequence, multiple=8, default=[])
        self.update()

    def update(self):
        sequences = split_array(self.sequence, 8)
        self.setFixedSize(get_widget_size(self._signature, len(split_array(sequences, 4))))

        self._igmeasures = [
            IGMeasure(None, s, self._signature)
            for s in sequences]
        self._igmeasures[-1].end = True

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

        self.repaint()

    def paintEvent(self, _):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def paint(self, painter):
        print('is painted')
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        for igmeasure in self._igmeasures:
            igmeasure.draw(painter)
        for igkeyspace in self._igkeyspaces:
            igkeyspace.draw(painter)
        for igsignature in self._igsignatures:
            igsignature.draw(painter)
