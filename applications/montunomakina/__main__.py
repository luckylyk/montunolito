
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
from montunomakina.generators import SimpleGenerator


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.patterns = []
        self.chords = []
        self.generator = SimpleGenerator()
        self.generator.close = self.generator.hide

        self.workspace = QtWidgets.QMdiArea()
        # self.workspace.setViewMode(QtWidgets.QMdiArea.TabbedView)
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
        self.setCentralWidget(self.workspace)
        menubar.show()

    def new_pattereditor(self):
        pattern = PatternEditor(PATTERNS['montuno'])
        pattern.view.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        pattern.view.destroyed.connect(self.window_closed)
        self.patterns.append(pattern)
        self.workspace.addSubWindow(pattern.view)
        pattern.view.show()

    def new_chordeditor(self):
        chords = ChordGridEditor(get_new_chordgrid())
        chords.view.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        chords.view.destroyed.connect(self.window_closed)
        self.chords.append(chords)
        self.workspace.addSubWindow(chords.view)
        chords.view.show()

    def show_generator(self):
        try:
            self.generator.raise_()
        except RuntimeError:
            self.generator = SimpleGenerator()
            self.workspace.addSubWindow(self.generator)
            self.generator.show()

    def window_closed(self):
        self.patterns = [app for app in self.patterns if test_application(app)]
        self.chords = [app for app in self.chords if test_application(app)]



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


print(QtWidgets.QStyleFactory.keys())

"windowsxp", "windowsvista", "gtk", "macintosh"