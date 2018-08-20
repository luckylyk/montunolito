import os
import sys

_current_dir = os.path.dirname(os.path.realpath(__file__))
APPLICATIONS_FOLDER = os.path.dirname(_current_dir)
MONTUNOLITO_FOLDER = os.path.dirname(os.path.dirname(_current_dir))
sys.path.insert(0, APPLICATIONS_FOLDER)
sys.path.insert(0, MONTUNOLITO_FOLDER)

from PyQt5 import QtWidgets
from montunolito.patterns import PATTERNS
from application import PatternEditor

application = QtWidgets.QApplication(sys.argv)
pe = PatternEditor(PATTERNS['montuno'])
pe.show()
application.exec_()
