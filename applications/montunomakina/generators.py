
import json
from PyQt5 import QtWidgets, QtCore, QtGui
from montunolito.core.solfege import NOTES
from montunolito.core.iterators import montuno_generator
from montunolito.core.pattern import is_valid_pattern, is_iterable_pattern
from montunolito.core.chord import is_valid_chordgrid
from montunolito.libs.jsonutils import json_to_pattern
from montunolito.libs.qt.dialogs import (
    open_dialog, save_dialog, check_pattern_dialog, invalid_file_dialog)
from montunolito.converters.musicxml.convert import convert_to_musicxml


class SimpleGenerator(QtWidgets.QWidget):
    sequenceGenerated = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.setWindowTitle('simple generator')
        self._patterneditors = []
        self._chordeditors = []

        self._patterneditor_combo = QtWidgets.QComboBox()
        self._patterneditor_combo.currentIndexChanged.connect(self.update_states)
        self._patternfilepath_lineedit = QtWidgets.QLineEdit()
        self._patternfilepath_lineedit.setPlaceholderText('use pattern file')
        self._patternfilepath_browse = QtWidgets.QPushButton('browse')
        self._patternfilepath_browse.released.connect(self.open_pattern_file)
        self._pattern_layout = QtWidgets.QHBoxLayout()
        self._pattern_layout.setContentsMargins(0, 0, 0, 0)
        self._pattern_layout.addWidget(self._patternfilepath_lineedit)
        self._pattern_layout.addWidget(self._patternfilepath_browse)

        self._chordseditor_combo = QtWidgets.QComboBox()
        self._chordseditor_combo.currentIndexChanged.connect(self.update_states)
        self._chordspath_lineedit = QtWidgets.QLineEdit()
        self._chordspath_lineedit.setPlaceholderText('use chord file')
        self._chordspath_browse = QtWidgets.QPushButton('browse')
        self._chordspath_browse.released.connect(self.open_chords_file)
        self._chords_layout = QtWidgets.QHBoxLayout()
        self._chords_layout.setContentsMargins(0, 0, 0, 0)
        self._chords_layout.addWidget(self._chordspath_lineedit)
        self._chords_layout.addWidget(self._chordspath_browse)

        self._tonality = QtWidgets.QComboBox()
        self._tonality.addItems(NOTES)
        self._tempo = QtWidgets.QLineEdit('180')
        self._tempo.setValidator(QtGui.QIntValidator(30, 500))
        self._measures_lineedit = QtWidgets.QLineEdit('16')
        self._measures_lineedit.setValidator(QtGui.QIntValidator())

        font = QtGui.QFont()
        font.setPixelSize(15)
        font.setBold(True)
        self._generator = QtWidgets.QPushButton('Generate')
        self._generator.setFixedHeight(40)
        self._generator.setFont(font)
        self._generator.released.connect(self.generate)

        self._data_layout = QtWidgets.QFormLayout(self)
        self._data_layout.addRow('select pattern', self._patterneditor_combo)
        self._data_layout.addRow('', self._pattern_layout)
        self._data_layout.addRow('select chord', self._chordseditor_combo)
        self._data_layout.addRow('', self._chords_layout)
        self._data_layout.addRow('tonality', self._tonality)
        self._data_layout.addRow('tempo (bpm)', self._tempo)
        self._data_layout.addRow('number of measures', self._measures_lineedit)
        self._data_layout.addItem(QtWidgets.QSpacerItem(15, 8))
        self._data_layout.addRow(self._generator)

    def set_patterneditors(self, patterneditors):
        self._patterneditor_combo.clear()
        self._patterneditors = patterneditors
        self._patterneditor_combo.addItems([pe.title for pe in patterneditors])
        self._patterneditor_combo.addItem('Use custom file')
        self._patterneditor_combo.insertSeparator(len(patterneditors))

    def set_chordeditors(self, chordeditors):
        self._chordseditor_combo.clear()
        self._chordeditors = chordeditors
        self._chordseditor_combo.addItems([ce.title for ce in chordeditors])
        self._chordseditor_combo.addItem('Use custom file')
        self._chordseditor_combo.insertSeparator(len(chordeditors))

    def update_states(self):
        state = (
            self._patterneditor_combo.currentIndex() ==
            self._patterneditor_combo.count() - 1)
        self._patternfilepath_lineedit.setEnabled(state)
        self._patternfilepath_browse.setEnabled(state)

        state = (
            self._chordseditor_combo.currentIndex() ==
            self._chordseditor_combo.count() - 1)
        self._chordspath_lineedit.setEnabled(state)
        self._chordspath_browse.setEnabled(state)

    def open_pattern_file(self):
        filepath = open_dialog()
        if filepath:
            self._patternfilepath_lineedit.setText(filepath)

    def open_chords_file(self):
        filepath = open_dialog()
        if filepath:
            self._chordspath_lineedit.setText(filepath)

    def sizeHint(self):
        return QtCore.QSize(350, 268)

    def get_pattern(self):
        current_combo_index = self._patterneditor_combo.currentIndex()
        combo_lenght = self._patterneditor_combo.count() - 1
        if current_combo_index != combo_lenght:
            return self._patterneditors[current_combo_index].pattern

        filename = self._patternfilepath_lineedit.text()
        try:
            with open(filename, 'r') as f:
                    pattern = json.load(f)
                    pattern = json_to_pattern(pattern)
                    return pattern
        except:
            invalid_file_dialog(filename)
            return None

    def get_chords(self):
        current_combo_index = self._chordseditor_combo.currentIndex()
        combo_lenght = self._chordseditor_combo.count() - 1
        if current_combo_index != combo_lenght:
            return self._chordeditors[current_combo_index].chordgrid

        filename = self._chordspath_lineedit.text()
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            invalid_file_dialog(filename)
            return None

    def generate(self):
        pattern = self.get_pattern()
        if pattern is None:
            return
        result, details = is_iterable_pattern(pattern)
        if result is False:
            check_pattern_dialog(result, details)
            return
        chordgrid = self.get_chords()
        if not is_valid_chordgrid(chordgrid):
            message = 'Chordgrid need a start chord'
            QtWidgets.QMessageBox.critical(None, 'Error', message)
            return
        generator = montuno_generator(
            pattern=pattern,
            chord_grid=chordgrid,
            tonality=self._tonality.currentIndex())

        eighths_count = int(self._measures_lineedit.text()) * 8
        keyboard_sequence = []
        for _ in range(eighths_count):
            keyboard_eighth = next(generator)
            keyboard_sequence.append(keyboard_eighth)

        self.sequenceGenerated.emit(keyboard_sequence)