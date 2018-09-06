import os
import sys

_current_dir = os.path.dirname(os.path.realpath(__file__))
APPLICATIONS_FOLDER = os.path.dirname(_current_dir)
MONTUNOLITO_FOLDER = os.path.dirname(os.path.dirname(_current_dir))
sys.path.insert(0, APPLICATIONS_FOLDER)
sys.path.insert(0, MONTUNOLITO_FOLDER)

from PyQt5 import QtWidgets
from sequencereader.widgets import SequenceReader#Test


def get_pre_registered_eighthkbnotes():
    a = [60]
    b = [34, 46]
    c = [38, 50]
    d = [40, 41, 46]
    # return (a, [], c, d)
    # return [a, [], [], [], a, [], [], []] #, [], [], [], [], [], [], [], [], [], []]
    # return [[i] for i in range(88)]
    # return [a, [], [], [], [], [], [], [], [], [], [], [], [], []]
    return [
        a, b, c, a, [], d, [], a, [], d, [], a, [], c, a, a] * 4

application = QtWidgets.QApplication(sys.argv)
# sequence_reader = Test()
sequence_reader = SequenceReader(get_pre_registered_eighthkbnotes())
sequence_reader.show()
application.exec_()


############################################################################
#################################  TESTS  ##################################
############################################################################
# from sequencereader.staff import get_beams_directions
# print(get_beams_directions(get_pre_registered_eighthkbnotes()))
# print(get_beams_directions(get_pre_registered_eighthkbnotes()))
# print(get_beams_directions(get_pre_registered_eighthkbnotes()))
# print(get_beams_directions(get_pre_registered_eighthkbnotes()))