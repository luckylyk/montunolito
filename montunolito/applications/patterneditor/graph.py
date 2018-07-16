from PyQt4 import QtGui, QtCore


GRID_SPACING = 33
PATTERN_WIDTH = 120
COLORS = {
    'graph': 
        {
            'background': '#4b4b4b',
            'grid':  '#555555'
        },
}

def draw_background(painter, rect):
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)

    brush = QtGui.QBrush(QtGui.QColor(COLORS['graph']['background']))
    painter.setBrush(brush)
    painter.drawRect(rect)

    pen = QtGui.QPen(QtGui.QColor(COLORS['graph']['grid']))
    painter.setPen(pen)
    left = 0
    while left < rect.width():
        left += GRID_SPACING
        painter.drawLine(
            QtCore.QPoint(left, 0),
            QtCore.QPoint(left, rect.height()))

    top = 0
    while top < rect.height():
        top += GRID_SPACING
        painter.drawLine(
            QtCore.QPoint(0, top),
            QtCore.QPoint(rect.width(), top))


def draw_column(painter, column, pattern):
    pass


if __name__ == '__main__':
    class MainTest(QtGui.QMainWindow):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedSize(800, 500)

        def paintEvent(self, event):
            painter = QtGui.QPainter()
            painter.begin(self)
            self.paint(painter)
            painter.end()

        def paint(self, painter):
            draw_background(painter, self.rect())

    import sys
    application = QtGui.QApplication(sys.argv)
    windows = MainTest()
    windows.show()
    application.exec_()