from PyQt5 import QtWidgets, QtGui


def set_shortcut(keysquence, parent, method):
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(keysquence), parent)
        shortcut.activated.connect(method)