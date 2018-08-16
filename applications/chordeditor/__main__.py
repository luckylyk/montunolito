import os
import sys

_current_dir = os.path.dirname(os.path.realpath(__file__))
APPLICATIONS_FOLDER = os.path.dirname(_current_dir)
MONTUNOLITO_FOLDER = os.path.dirname(os.path.dirname(_current_dir))
sys.path.insert(0, APPLICATIONS_FOLDER)
sys.path.insert(0, MONTUNOLITO_FOLDER)

from widgets import ChordGridEditor
from PyQt5 import QtWidgets

CHORD = [
    {'degree': 1, 'name': 'Minor'},
    None,
    None,
    {'degree': 4, 'name': 'Minor'},
    None,
    None,
    {'degree': 5, 'name': 'M7'},
    None,
    None,
    None,
    None,
    {'degree': 4, 'name': 'Minor'},
    None,
    None, 
    {'degree': 1, 'name': 'Minor'},
    None,
    {'degree': 1, 'name': 'Minor'},
    None,
    None,
    {'degree': 4, 'name': 'Minor'},
    None,
    None,
    {'degree': 5, 'name': 'M7'},
    None,
    None,
    None,
    None,
    {'degree': 4, 'name': 'Minor'},
    None,
    None, 
    {'degree': 1, 'name': 'Minor'},
    None,
    {'degree': 1, 'name': 'Minor'},
    None,
    None,
    {'degree': 4, 'name': 'Minor'},
    None,
    None,
    {'degree': 5, 'name': 'M7'},
    None,
    None,
    None,
    None,
    {'degree': 4, 'name': 'Minor'},
    None,
    None, 
    {'degree': 1, 'name': 'Minor'},
    None,
    {'degree': 1, 'name': 'Minor'},
    None,
    None,
    {'degree': 4, 'name': 'Minor'},
    None,
    None,
    {'degree': 5, 'name': 'M7'},
    None,
    None,
    None,
    None,
    {'degree': 4, 'name': 'Minor'},
    None,
    None, 
    {'degree': 1, 'name': 'Minor'},
    None,
    {'degree': 1, 'name': 'Minor'},
    None,
    None,
    {'degree': 4, 'name': 'Minor'},
    None,
    None,
    {'degree': 5, 'name': 'M7'},
    None,
    None,
    None,
    None,
    {'degree': 4, 'name': 'Minor'},
    None,
    None, 
    {'degree': 1, 'name': 'Minor'},
    None]




application = QtWidgets.QApplication(sys.argv)
w = ChordGridEditor(chords=CHORD, tonality=4)
w.show()
application.exec_()
