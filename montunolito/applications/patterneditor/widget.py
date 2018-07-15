from PyQt4 import QtGui, QtCore


class MainTest(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 500)
        self._ballon = None

    def mousePressEvent(self, event):
        if QtCore.QRect(35, 35, self.height() - 35, self.width() - 35).contains(event.pos()):
            self._ballon = BehaviorBalloon()
            self._ballon.show()


BEHAVIOR_NAMES = "- Melodic", "- Arpegic", "- Static"
BEHAVIOR_BUBBLE_TITLE = "Behaviors coeficients"

class BehaviorBalloon(QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Popup)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(240, 130)
        self.move(
            QtGui.QCursor().pos().x() - 20,
            QtGui.QCursor().pos().y() - self.height())

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def paint(self, painter):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        pen = QtGui.QPen(QtGui.QColor(175, 175, 175, 255))
        pen.setWidth(2)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)

        painter.setBrush(QtGui.QBrush(QtGui.QColor(200, 200, 200)))
        painter.setPen(pen)

        polygon = QtGui.QPolygon([
            QtCore.QPoint(28, self.height() - 30),
            QtCore.QPoint(20, self.height()),
            QtCore.QPoint(50, self.height() - 30)])

        painter.drawPolygon(polygon)
        painter.drawRoundedRect(
            2, 2, self.width() - 4, self.height() - 29, 22, 18)

        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRoundedRect(self.width() - 30, 10, 17, 17, 5, 5)
        painter.drawLine(
            QtCore.QPoint(self.width() - 25, 15),
            QtCore.QPoint(self.width() - 18, 22))
        painter.drawLine(
            QtCore.QPoint(self.width() - 18, 15),
            QtCore.QPoint(self.width() - 25, 22))

        pen = QtGui.QPen(QtGui.QColor(75, 75, 75))
        painter.setPen(pen)

        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(12)
        painter.setFont(font)
        painter.drawText(20, 25, BEHAVIOR_BUBBLE_TITLE)

        font.setBold(False)
        font.setPointSize(11)
        painter.setFont(font)

        pen = QtGui.QPen(QtGui.QColor(110, 110, 110))
        painter.setPen(pen)
        top_offset = 50
        for i, text in enumerate(BEHAVIOR_NAMES):
            painter.drawText(27, (20 * i) + top_offset, text)



if __name__ == "__main__":
    import sys
    application = QtGui.QApplication(sys.argv)
    windows = MainTest()
    windows.show()
    application.exec_()
