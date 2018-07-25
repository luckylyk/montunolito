from PyQt4 import QtGui, QtCore
from draws import draw_ballon, draw_closer, draw_texts
from fingerstates import Fingerstates


BEHAVIOR_NAMES = "- Melodic", "- Arpegic", "- Static"
BEHAVIOR_BUBBLE_TITLE = "Behaviors coeficients"


class Balloon(QtGui.QWidget):
    TITLE = "BUBBLE_TITLE"

    def __init__(self, size=None, parent=None):
        super().__init__(parent, QtCore.Qt.Popup)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self._closer_state = False
        if size:
            self.setFixedSize(size)
            self.move(
                QtGui.QCursor().pos().x() - 20,
                QtGui.QCursor().pos().y() - self.height())
        self.drawable_rect = QtCore.QRect(
            15, 40, self.width() - 50, self.height() - 80)
        self._closer_rect = QtCore.QRect(self.width() - 30, 10, 17, 17)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        if self._closer_rect.contains(event.pos()) != self._closer_state:
            self._closer_state = self._closer_rect.contains(event.pos())
            self.repaint()

    def mouseReleaseEvent(self, _):
        if self._closer_state:
            self.close()

    def paintEvent(self, _):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def paint(self, painter):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        draw_ballon(painter, self.rect(), self.TITLE)
        draw_closer(painter, self._closer_rect, self._closer_state)

    def cursor(self):
        return self.mapFromGlobal(QtGui.QCursor.pos())


class BehaviorBalloon(Balloon):
    TITLE = BEHAVIOR_BUBBLE_TITLE

    def __init__(self, parent=None):
        super().__init__(size=QtCore.QSize(200, 90), parent=parent)

    def paint(self, painter):
        super().paint(painter)
        draw_texts(painter, self.drawable_rect, BEHAVIOR_NAMES)


class FingerstatesBalloon(Balloon):
    TITLE = 'Fingerstates'

    def __init__(self, fingerstates, parent=None):
        size = QtCore.QSize(180, 150)
        super().__init__(size=size, parent=parent)
        self.fingerstates = Fingerstates(fingerstates, self.drawable_rect)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.repaint()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.fingerstates.set_selected_state(self.cursor())
        self.repaint()

    def paint(self, painter):
        super().paint(painter)
        self.fingerstates.draw(painter, self.cursor())
