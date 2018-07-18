from PyQt4 import QtGui, QtCore
from draws import draw_fingerstate, draw_ballon, draw_closer, draw_texts


BEHAVIOR_NAMES = "- Melodic", "- Arpegic", "- Static"
BEHAVIOR_BUBBLE_TITLE = "Behaviors coeficients"


class Balloon(QtGui.QWidget):
    TITLE = "BUBBLE_TITLE"

    def __init__(self, size=None, parent=None):
        super().__init__(parent, QtCore.Qt.Popup)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self._closer_state = False
        if size:
            self.setFixedSize(size)
            self.move(
                QtGui.QCursor().pos().x() - 20,
                QtGui.QCursor().pos().y() - self.height())
        self.drawable_rect = QtCore.QRect(
            15, 40, self.width() - 30, self.height() - 60)
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


class BehaviorBalloon(Balloon):
    TITLE = BEHAVIOR_BUBBLE_TITLE

    def __init__(self, parent=None):
        super().__init__(size=QtCore.QSize(240, 130), parent=parent)

    def paint(self, painter):
        super().paint(painter)
        draw_texts(painter, self.drawable_rect, BEHAVIOR_NAMES)


class FingerstatesBalloon(Balloon):
    TITLE = 'Fingerstates'
    def __init__(self, fingerstates, parent=None):
        self.fingerstates = fingerstates
        size = QtCore.QSize(180, 25 * len(fingerstates) + 90)
        super().__init__(size=size, parent=parent)
        spacing = 3
        self._rects = [
            QtCore.QRect(
                self.drawable_rect.left(),
                self.drawable_rect.top() + (25 * index) + (spacing * index),
                25 * 5, 25)
            for index, fingerstate in enumerate(self.fingerstates)]
        self._hover_rect_index = None

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        for index, rect in enumerate(self._rects):
            if rect.contains(event.pos()) and index != self._hover_rect_index:
                self._hover_rect_index = index
                self.repaint()

    def paint(self, painter):
        super().paint(painter)
        for index, rect in enumerate(self._rects):
            border = index == self._hover_rect_index
            draw_fingerstate(
                painter, self.fingerstates[index], rect, border=border)