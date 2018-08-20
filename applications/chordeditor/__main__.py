import os
import sys

_current_dir = os.path.dirname(os.path.realpath(__file__))
APPLICATIONS_FOLDER = os.path.dirname(_current_dir)
MONTUNOLITO_FOLDER = os.path.dirname(os.path.dirname(_current_dir))
sys.path.insert(0, APPLICATIONS_FOLDER)
sys.path.insert(0, MONTUNOLITO_FOLDER)

from PyQt5 import QtWidgets
from montunolito.core.chord import get_new_chordgrid
from application import ChordGridEditor


application = QtWidgets.QApplication(sys.argv)
w5 = ChordGridEditor(chords=get_new_chordgrid())
w5.show()
application.exec_()