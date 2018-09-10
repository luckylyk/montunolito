import os
import sys

_current_dir = os.path.dirname(os.path.realpath(__file__))
APPLICATIONS_FOLDER = os.path.dirname(_current_dir)
MONTUNOLITO_FOLDER = os.path.dirname(os.path.dirname(_current_dir))
sys.path.insert(0, APPLICATIONS_FOLDER)
sys.path.insert(0, MONTUNOLITO_FOLDER)

from PyQt5 import QtWidgets
from sequencereader.widgets import SequenceReaderWidget
from sequencereader.rules import (
    get_signature_positions, is_bemol_signature, get_bemol_signatures,
    get_sharp_signatures)


def get_pre_registered_eighthkbnotes():
    a = [60, 69, 75]
    b = [25, 31, 35]
    c = [38, 50]
    d = [40, 41, 46]
    # return (a, [], c, d)
    # return [a, [], [], [], a, [], [], []] #, [], [], [], [], [], [], [], [], [], []]
    # return [[i] for i in range(88)]
    # return [a, [], [], [], [], [], [], [], [], [], [], [], [], []]
    return [
        [39, 51, 63], [42, 54], [46, 58], [39, 51, 63], [], [46, 58], [51, 63],
        [49, 61, 73], [], [53, 61, 65, 73], [], [49, 61, 73], [41, 53, 65], [],
        [44, 56, 68], [], [44, 56, 68], [], [48, 54, 60, 66], [44, 56, 68], [],
        [48, 54, 60, 66], [], [44, 56, 68], [], [46, 50, 58, 62], [],
        [41, 53, 65], [41, 53, 65], [], [40, 52, 64], [], [39, 51, 63],
        [39, 51], [42, 54], [34, 46, 58], [], [39, 51], [34, 46], [25, 37, 49],
        [], [25, 37], [29, 41], [20, 32, 44], [25, 37, 49], [], [32, 44, 56],
        [], [27, 39, 51], [32, 44], [36, 48], [27, 39, 51], [], [30, 42, 54],
        [], [32, 44, 56], [], [34, 46], [34, 46], [26, 38, 50], [29, 41, 53],
        [], [32, 44, 56], [], [27, 39, 51], [], [30, 39, 42, 51], [34, 46, 58],
        [], [39, 42, 51, 54], [], [37, 49, 61], [], [41, 44, 53, 56], [],
        [32, 44, 56], [], [37, 41, 49, 53], [], [37, 49, 61], [32, 44, 56],
        [36, 48], [39, 51], [30, 42, 54], [], [32, 44], [32, 44], [36, 48, 60],
        [], [38, 46, 50, 58], [], [32, 44, 56], [34, 46, 58], [], [36, 48, 60],
        [], [38, 50, 62], [39, 51], [42, 54], [34, 46, 58], [], [39, 51],
        [34, 46], [25, 37, 49], [], [25, 37], [29, 41], [20, 32, 44], [],
        [25, 29, 37, 41], [25, 37, 49], [32, 44, 56], [27, 39, 51], [],
        [30, 36, 42, 48], [32, 44, 56], [], [36, 42, 48, 54], [], [32, 44, 56],
        [], [34, 38, 46, 50], [], [34, 38, 46, 50], [34, 46, 58], [],
        [38, 50, 62], [], [39, 51, 63], [39, 51], [42, 54], [34, 46, 58], [],
        [39, 51], [44, 56], [32, 44, 56], [], [36, 48], [39, 51], [30, 42, 54],
        [32, 44, 56], [], [32, 44, 56], [], [27, 39, 51], [], [30, 36, 42, 48],
        [30, 42, 54], [], [34, 36, 46, 48], [], [34, 46, 58], [],
        [36, 46, 48, 58], [], [36, 46, 48, 58], [], [36, 46, 48, 58],
        [39, 51, 63], [], [42, 54, 66], [], [46, 48, 58, 60], [34, 46, 58], [],
        [30, 42, 54], [], [32, 44, 56], [], [32, 44], [35, 47], [27, 39, 51],
        [32, 44, 56], [], [27, 39, 51], [], [27, 39, 51], [27, 39], [27, 39],
        [24, 36, 48], [], [22, 34, 46], [], [27, 39, 51], [], [30, 36, 42, 48],
        [], [30, 36, 42, 48], [34, 46, 58], [], [36, 48, 60], [], [37, 49, 61],
        [39, 51], [41, 53], [30, 42, 54], [], [39, 51], [42, 54], [32, 44, 56],
        [], [32, 44], [35, 47], [27, 39, 51], [], [29, 35, 41, 47], [],
        [29, 41, 53], [35, 47, 59], [], [39, 44, 51, 56], [35, 47, 59], [],
        [39, 51, 63], [], [42, 54, 66], [], [44, 56], [47, 59], [35, 47, 59],
        [35, 47, 59], [], [37, 49, 61], [], [39, 51, 63], [], [42, 44, 54, 56],
        [40, 52, 64], [], [42, 44, 54, 56], [], [39, 51, 63], [],
        [42, 44, 54, 56], [], [40, 52, 64], [42, 54, 66], [], [44, 56, 68], [],
        [39, 51, 63], [], [42, 48, 54, 60], [42, 54, 66], [], [34, 46, 58], [],
        [36, 48, 60], [], [42, 48, 54, 60], [], [34, 46, 58], [],
        [36, 42, 48, 54], [34, 46, 58], [34, 46, 58]]

    return [a, b, c, a, [], d, [], a, [], d, [], a, [], c, a, a] * 4

application = QtWidgets.QApplication(sys.argv)
# sequence_reader = Test()
sequence_reader = SequenceReaderWidget(get_pre_registered_eighthkbnotes())
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

# from sequencereader.rules import get_signature_positions
# print(get_signature_positions('A', major=False))
# print(get_bemol_signatures())
# print(get_sharp_signatures())
# print(get_signature_positions('G', major=True))
# print(get_signature_positions('Db', major=True))
# print(get_signature_positions('C', major=True))
# print(get_signature_positions('A', major=True))
# print(get_signature_positions('F', major=True))
# print(get_signature_positions('F#', major=True))
# print(get_signature_positions('E', major=True))


# from sequencereader.rules import get_alteration_value
# print (get_alteration_value(55, 33))
# print (get_alteration_value(81, 47))
