from PyQt4 import QtGui, QtCore


BEHAVIOR_NAMES = "- Melodic", "- Arpegic", "- Static"
BEHAVIOR_BUBBLE_TITLE = "Behaviors coeficients"
COLORS = {
    'fingerstates': 
        {
            'pressed': '#AADDBB',
            'released': '#ABABAB',
        },
    'bubble':
        {
            'closer':
                {
                    'over': '#d0a895',
                    'free': "#B3B3B3",
                    'cross': "#4b4b4b"
                },
            'border': '#4b4b4b',
            'title': '#4b4b4b',
            'background': '#c8c8c8'
        }
}


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

    def mouseReleaseEvent(self, event):
        if self._closer_state:
            self.close()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def paint(self, painter):
        draw_ballon(painter, self.rect(), self.TITLE)
        draw_closer(painter, self._closer_rect, self._closer_state)


class BehaviorBalloon(Balloon):
    TITLE = BEHAVIOR_BUBBLE_TITLE

    def __init__(self, parent=None):
        super().__init__(size=QtCore.QSize(240, 130), parent=parent)

    def paint(self, painter):
        super().paint(painter)

        font = QtGui.QFont()
        font.setBold(False)
        font.setPointSize(11)
        painter.setFont(font)

        pen = QtGui.QPen(QtGui.QColor(110, 110, 110))
        painter.setPen(pen)
        top_offset = self.drawable_rect.top() + 5
        for i, text in enumerate(BEHAVIOR_NAMES):
            painter.drawText(27, (20 * i) + top_offset, text)


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
            draw_fingerstate(painter, self.fingerstates[index], rect, border=border)


def draw_fingerstate(painter, fingerstate, rect, border=False):
    pen = QtGui.QPen(QtGui.QColor(0,0,0,0))
    pen.setWidth(0)
    painter.setPen(pen)
    width = round(rect.width() / 5.0)

    rects = [
        QtCore.QRect(
            rect.left() + (i * width),
            rect.top(), width, rect.height()) for i in range(5)]

    brush_pressed = QtGui.QBrush(
        QtGui.QColor(COLORS['fingerstates']['pressed']))
    brush_released = QtGui.QBrush(
        QtGui.QColor(COLORS['fingerstates']['released']))

    for r, s in zip(rects, fingerstate):
        painter.setBrush(brush_pressed if s is True else brush_released)
        painter.drawRect(r)

    if border is False:
        return

    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
    pen = QtGui.QPen(QtGui.QColor(COLORS['bubble']['border']))
    painter.setPen(pen)
    painter.setBrush(brush)
    painter.drawRect(rect)

    brush = QtGui.QBrush(QtGui.QColor(COLORS['bubble']['border']))
    painter.setBrush(brush)
    comborect = QtCore.QRect(
        rect.width() + rect.left(), rect.top(), 20, rect.height())
    painter.drawRect(comborect)

    brush = QtGui.QBrush(QtGui.QColor(COLORS['bubble']['background']))
    painter.setBrush(brush)
    polygon = QtGui.QPolygon([
        QtCore.QPoint(rect.width() + rect.left() + 5, rect.top() + 7),
        QtCore.QPoint(rect.width() + rect.left() + 15, rect.top() + 7),
        QtCore.QPoint(rect.width() + rect.left() + 10, rect.top() + 12)])
    painter.drawPolygon(polygon) 


def draw_ballon(painter, rect, title):
    painter.setRenderHint(QtGui.QPainter.Antialiasing)

    pen = QtGui.QPen(QtGui.QColor(0,0,0,0))
    pen.setWidth(0)
    pen.setJoinStyle(QtCore.Qt.MiterJoin)

    painter.setBrush(QtGui.QBrush(QtGui.QColor(COLORS['bubble']['background'])))
    painter.setPen(pen)

    polygon = QtGui.QPolygon([
        QtCore.QPoint(28, rect.height() - 30),
        QtCore.QPoint(20, rect.height()),
        QtCore.QPoint(50, rect.height() - 30)])

    painter.drawPolygon(polygon)
    painter.drawRoundedRect(
        2, 2, rect.width() - 4, rect.height() - 29, 22, 22)

    pen = QtGui.QPen(QtGui.QColor(COLORS['bubble']['title']))
    painter.setPen(pen)

    font = QtGui.QFont()
    font.setBold(True)
    font.setPointSize(12)
    painter.setFont(font)
    painter.drawText(20, 25, title)


def draw_closer(painter, rect, state):
    state = 'over' if state is True else 'free'
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)

    brush = QtGui.QBrush(QtGui.QColor(COLORS['bubble']['closer'][state]))
    painter.setBrush(brush)

    painter.drawRoundedRect(rect, 5, 5)
    pen = QtGui.QPen(QtGui.QColor(COLORS['bubble']['closer']['cross']))
    pen.setWidth(2)
    painter.setPen(pen)
    shrink = 5
    painter.drawLine(
        QtCore.QPoint(rect.left() + shrink, rect.top() + shrink),
        QtCore.QPoint(
            rect.left() + rect.width() - shrink,
            rect.top() + rect.height() - shrink))
    painter.drawLine(
        QtCore.QPoint(
            rect.left() + rect.width() - shrink, rect.top() + shrink),
        QtCore.QPoint(
            rect.left() + shrink, rect.top() + rect.height() - shrink))


if __name__ == "__main__":

    TEST_FINGERSTATES = [
        (True, False, False, False, True), (False, True, False, True, False),
        (True, False, False, False, True), (False, True, False, True, False)]


    class MainTest(QtGui.QMainWindow):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedSize(800, 500)
            self._ballon = None

        def mousePressEvent(self, event):
            if QtCore.QRect(35, 35, self.height() - 35, self.width() - 35).contains(event.pos()):
                if event.button() == QtCore.Qt.LeftButton:
                    self._ballon = FingerstatesBalloon(fingerstates=TEST_FINGERSTATES)
                    self._ballon.show()
                elif event.button() == QtCore.Qt.RightButton:
                    self._ballon = BehaviorBalloon()
                    self._ballon.show()
    import sys
    application = QtGui.QApplication(sys.argv)
    windows = MainTest()
    windows.show()
    application.exec_()