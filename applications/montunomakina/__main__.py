import os
import sys

_current_dir = os.path.dirname(os.path.realpath(__file__))
APPLICATIONS_FOLDER = os.path.dirname(_current_dir)
MONTUNOLITO_FOLDER = os.path.dirname(os.path.dirname(_current_dir))
sys.path.insert(0, APPLICATIONS_FOLDER)
sys.path.insert(0, MONTUNOLITO_FOLDER)


from PyQt5 import QtWidgets, QtCore
from montunolito.patterns import PATTERNS
from montunolito.core.chord import get_new_chordgrid

from patterneditor.application import PatternEditor
from chordeditor.application import ChordGridEditor


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__(None, QtCore.Qt.Window)

        pattern = PatternEditor(PATTERNS['montuno'])
        chords = ChordGridEditor(get_new_chordgrid())

        workspace = QtWidgets.QMdiArea()
        workspace.setViewMode(QtWidgets.QMdiArea.SubWindowView)
        workspace.addSubWindow(pattern.view)
        workspace.addSubWindow(chords.view)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(workspace)



application = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
application.exec_()