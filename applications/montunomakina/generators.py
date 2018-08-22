from PyQt5 import QtWidgets, QtCore


class SimpleGenerator(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)

        self._patterneditors = []
        self._chordeditors = []

        self._patterneditor_combo = QtWidgets.QComboBox()
        self._patternfilepath_lineedit = QtWidgets.QLineEdit()
        self._patternfilepath_lineedit.setPlaceholderText('use pattern file')

        self._chordseditor_combo = QtWidgets.QComboBox()
        self._chordspath_lineedit = QtWidgets.QLineEdit()
        self._chordspath_lineedit.setPlaceholderText('use chord file')
        
        self._data_layout = QtWidgets.QFormLayout()
        self._data_layout.addRow('select pattern', self._patterneditor_combo)
        self._data_layout.addRow('', self._patternfilepath_lineedit)
        self._data_layout.addRow('select chord', self._chordseditor_combo)
        self._data_layout.addRow('', self._chordspath_lineedit)

        self._generator = QtWidgets.QPushButton('Generate')
        self._convertor = QtWidgets.QPushButton('Convert')

        self._buttons_layout = QtWidgets.QHBoxLayout()
        self._buttons_layout.addWidget(self._generator)
        self._buttons_layout.addWidget(self._convertor)

        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.addLayout(self._data_layout)
        self._layout.addLayout(self._buttons_layout)

    def set_patterneditors(self, patterneditors):
        self._patterneditors = patterneditors

    def set_chordeditors(self, chordeditors):
        self._chordeditors = chordeditors
