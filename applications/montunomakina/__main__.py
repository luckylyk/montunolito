
import os
import sys

_current_dir = os.path.dirname(os.path.realpath(__file__))
APPLICATIONS_FOLDER = os.path.dirname(_current_dir)
MONTUNOLITO_FOLDER = os.path.dirname(os.path.dirname(_current_dir))
sys.path.insert(0, APPLICATIONS_FOLDER)
sys.path.insert(0, MONTUNOLITO_FOLDER)


from PyQt5 import QtWidgets, QtCore, QtGui
from montunolito.patterns import PATTERNS
from montunolito.core.chord import get_new_chordgrid

from patterneditor.application import PatternEditor
from chordeditor.application import ChordGridEditor
from sequencereader.application import SequenceReader
from montunomakina.generators import SimpleGenerator


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.setWindowTitle('Montuno Makina 0.1')

        self.patterns = []
        self.patterns_count = 0
        self.chords = []
        self.chords_count = 0
        self.viewer = []
        self.generator = SimpleGenerator()
        self.generator.sequenceGenerated.connect(self.view_sequence)

        self.workspace = QtWidgets.QMdiArea()
        self.workspace.addSubWindow(self.generator)

        menubar = self.menuBar()
        menu = menubar.addMenu('&Application')
        menu.addAction(
            '&Exit',
            QtWidgets.qApp.exit,
            QtGui.QKeySequence('Ctrl+Q'))
        menu = menubar.addMenu('&Window')
        new_window = menu.addMenu('New Window')
        new_window.addAction(
            'Pattern Editor',
            self.new_pattereditor,
            QtGui.QKeySequence('Ctrl+P'))
        new_window.addAction(
            'Chord Grid Editor',
            self.new_chordeditor,
            QtGui.QKeySequence('Ctrl+E'))
        menu.addMenu(new_window)
        menu.addAction(
            'Generator',
            self.show_generator,
            QtGui.QKeySequence('Ctrl+G'))
        menu.addSeparator()
        menu.addAction(
            '&Tile Windows',
            self.workspace.tileSubWindows )
        menu.addAction(
            '&Cascade Windows',
            self.workspace.cascadeSubWindows)
        menu = menubar.addMenu('&?')
        menu.addAction(
            '&About',
            self.workspace.cascadeSubWindows)
        self.setCentralWidget(self.workspace)
        menubar.show()
        self.update_generator()

    def new_pattereditor(self):
        self.patterns_count += 1
        pattern = PatternEditor(PATTERNS['montuno'])
        pattern.set_title('{} {}'.format(pattern.title, self.patterns_count))
        pattern.view.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        pattern.view.destroyed.connect(self.window_closed)
        self.patterns.append(pattern)
        self.workspace.addSubWindow(pattern.view)
        pattern.view.show()
        self.update_generator()

    def new_chordeditor(self):
        self.chords_count += 1
        chords = ChordGridEditor(get_new_chordgrid())
        chords.set_title('{} {}'.format(chords.title, self.chords_count))
        chords.view.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        chords.view.destroyed.connect(self.window_closed)
        self.chords.append(chords)
        self.workspace.addSubWindow(chords.view)
        chords.view.show()
        self.update_generator()

    def update_generator(self):
        self.generator.set_patterneditors(self.patterns)
        self.generator.set_chordeditors(self.chords)

    def show_generator(self):
        try:
            self.generator.raise_()
        except RuntimeError:
            self.generator = SimpleGenerator()
            self.generator.sequenceGenerated.connect(self.view_sequence)
            self.workspace.addSubWindow(self.generator)
            self.generator.show()

    def window_closed(self):
        self.patterns = [app for app in self.patterns if test_application(app)]
        self.chords = [app for app in self.chords if test_application(app)]
        self.update_generator()

    def view_sequence(self, sequence):
        sequence_reader = SequenceReader(sequence)
        self.workspace.addSubWindow(sequence_reader.view)
        self.viewer.append(sequence_reader)
        sequence_reader.show()


def test_application(app):
    try:
        app.view.show()
        return True
    except RuntimeError:
        return False


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    application.setStyle("Fusion")
    w = MainWindow()
    w.show()
    application.exec_()
