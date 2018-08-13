import os
import sys

_current_dir = os.path.dirname(os.path.realpath(__file__))
APPLICATIONS_FOLDER = os.path.dirname(_current_dir)
MONTUNOLITO_FOLDER = os.path.dirname(os.path.dirname(_current_dir))
sys.path.insert(0, APPLICATIONS_FOLDER)
sys.path.insert(0, MONTUNOLITO_FOLDER)

from PyQt5 import QtWidgets, QtCore, QtGui
from interactive import IGNoteSelecter, IGChordSelecter, IGChordGrid


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


class WidgetTest(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.setMouseTracking(True)
        self.noteselecter = IGNoteSelecter(
            QtCore.QRect(
                self.rect().left(),
                self.rect().top(),
                self.rect().width(),
                self.rect().height() / 20),
            0)
        self.chordselecter = IGChordSelecter(
            QtCore.QRect(
                self.rect().left(),
                self.rect().top() + (self.rect().height() / 20),
                self.rect().width(),
                self.rect().height() / 20),
            0)

    def resizeEvent(self, event):
        self.noteselecter = IGNoteSelecter(
            QtCore.QRect(
                self.rect().left(),
                self.rect().top(),
                self.rect().width(),
                self.rect().height() / 20),
            0)
        self.chordselecter = IGChordSelecter(
            QtCore.QRect(
                self.rect().left(),
                self.rect().top() + (self.rect().height() / 20),
                self.rect().width(),
                self.rect().height() / 20),
            0)
        self.staff = IGChordGrid(
            QtCore.QRect(
                self.rect().left(),
                self.rect().top() + (self.rect().height() / 10),
                self.rect().width(),
                self.rect().height() - (self.rect().height() / 10)),
            CHORD)
        self.repaint()

    def mouseMoveEvent(self, event):
        self.repaint()

    def paintEvent(self, _):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def paint(self, painter):
        self.noteselecter.draw(painter)
        self.chordselecter.draw(painter)
        self.staff.draw(painter)


application = QtWidgets.QApplication(sys.argv)
w = WidgetTest()
w.show()
application.exec_()
