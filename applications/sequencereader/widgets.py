
import os
from scipy.io.wavfile import write
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia


from montunolito.converters.wav.convert import convert_sequence_to_int16
from montunolito.core.utils import split_array, set_array_lenght_multiple
from sequencereader.rules import Signature, SIGNATURES
from sequencereader.interactive import IGMeasure, IGKeySpace, IGSignature
from sequencereader.geometries import (
    extract_measures_rects, extract_rects_keyspaces, extract_signature_rects,
    get_widget_size)


DEFAULT_VOLUME = 60
TMP_FILE = os.path.join(os.path.expanduser("~"), '_tmp_mm_{}.wav')


class SequenceReaderWidget(QtWidgets.QWidget):

    def __init__(self, sequence, signature, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.musicsheet = MusicSheetWidget(sequence, signature)
        self.player = SequencePlayer()
        self.menu = MenuWidget(player=self.player)
        self.player.set_sequence(sequence)

        self._scroll_area = QtWidgets.QScrollArea()
        self._scroll_area.setWidget(self.musicsheet)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setAlignment(QtCore.Qt.AlignHCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.menu)
        self.layout.addWidget(self._scroll_area)

        self.sizeHint = lambda: QtCore.QSize(1250, 600)

    def closeEvent(self, event):
        super().closeEvent(event)
        self.player.close()


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

    def __init__(self, player=None, parent=None):
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
        if player:
            self.layout.addWidget(player)
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
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        for igmeasure in self._igmeasures:
            igmeasure.draw(painter)
        for igkeyspace in self._igkeyspaces:
            igkeyspace.draw(painter)
        for igsignature in self._igsignatures:
            igsignature.draw(painter)


class SequencePlayer(QtWidgets.QWidget):
    BUTTON_SIZE = 25
    def __init__(self, parent=None):
        super().__init__(parent)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.positionChanged.connect(self.position_changed)
        self.player.setVolume(DEFAULT_VOLUME)
        self.playlist = QtMultimedia.QMediaPlaylist()

        self.sequence = None
        self.sound_array = None
        self.tmpfile_path = None

        self.play = QtWidgets.QPushButton(icon('play.png'), '')
        self.play.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        self.play.released.connect(self._call_play)
        self.pause = QtWidgets.QPushButton(icon('pause.png'), '')
        self.pause.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        self.pause.released.connect(self._call_pause)
        self.stop = QtWidgets.QPushButton(icon('stop.png'), '')
        self.stop.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        self.stop.released.connect(self._call_stop)

        self.seeker = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.seeker.setRange(0, 100)
        self.seeker.setTracking(False)
        self.seeker.sliderMoved.connect(self.seek_position)

        self.volumelabel = QtWidgets.QLabel('volume:')
        self.volume = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.volume.setRange(0, 100)
        self.volume.setFixedWidth(60)
        self.volume.setValue(DEFAULT_VOLUME)
        self.volume.valueChanged.connect(self.player.setVolume)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.play)
        self.layout.addWidget(self.pause)
        self.layout.addWidget(self.stop)
        self.layout.addWidget(self.seeker)
        self.layout.addWidget(self.volumelabel)
        self.layout.addWidget(self.volume)

    def set_sequence(self, sequence):
        self.sequence = sequence
        self.sound_array = None

    def _create_media(self):
        self.sound_array = convert_sequence_to_int16(self.sequence)
        self.tmpfile_path = get_tempfile_path()
        write(self.tmpfile_path, 44100, self.sound_array)
        url = QtCore.QUrl('file:///' + self.tmpfile_path)
        self.playlist.clear()
        self.playlist.addMedia(QtMultimedia.QMediaContent(url))
        self.player.setPlaylist(self.playlist)

    def _call_play(self):
        if self.sequence is None:
            return

        if self.sound_array is None:
            self._create_media()

        self.seeker.setRange(0, self.player.duration())
        if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            return
        self.player.play()

    def _call_pause(self):
        if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.player.pause()

    def _call_stop(self):
        if self.player.state() != QtMultimedia.QMediaPlayer.StoppedState:
            self.player.stop()

    def seek_position(self, position):
        if self.player.isSeekable():
            self.player.setPosition(position)

    def position_changed(self, position):
        self.seeker.setValue(position)

    def closeEvent(self, event):
        super().closeEvent(event)
        self.playlist.clear()
        try:
            if self.tmpfile_path:
                os.remove(self.tmpfile_path)
        except (OSError, FileNotFoundError):
            print('file not removed {}'.format(self.tmpfile_path))


def get_tempfile_path():
    inc = 0
    tmpfile = TMP_FILE.format(str(inc).zfill(2))
    while os.path.exists(tmpfile):
        inc += 1
        tmpfile = TMP_FILE.format(str(inc).zfill(2))
    return tmpfile