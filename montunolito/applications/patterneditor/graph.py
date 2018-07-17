from PyQt4 import QtGui, QtCore


GRID_SPACING = 33
PATTERN_WIDTH = 120
COLORS = {
    'graph': 
        {
            'background': '#4b4b4b',
            'grid':  '#555555',
            'column':
                {
                    'background': '#5d5d5d',
                    'number': '#998532'
                },
            'index':
                {
                    'background': '#6e6e6e',
                    'border_highlight': '#449999',
                    'plug_highlight': '#CCAA88',
                    'item':
                        {
                            'background': '#7f7f7f',
                            'border_highlight': '#449999'
                        }
                }

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



def draw_column_background(painter, rect, number):
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)

    brush = QtGui.QBrush(QtGui.QColor(COLORS['graph']['column']['background']))
    painter.setBrush(brush)
    painter.drawRoundedRect(
        rect.left(), rect.top() + 20, rect.width(), rect.height() - 5, 10, 10)

    painter.drawRoundedRect(
        rect.left() + rect.width() - 30, rect.top(), 30, 40, 10, 10)

    pen = QtGui.QPen(QtGui.QColor(COLORS['graph']['column']['number']))
    painter.setPen(pen)

    font = QtGui.QFont()
    font.setBold(True)
    font.setPointSize(12)
    painter.setFont(font)
    painter.drawText(
        rect.left() + rect.width() - 20, rect.top() + 20, str(number))


def draw_index(painter, rect, occurence, hover=0):
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)

    background = QtGui.QColor(COLORS['graph']['index']['background'])
    plug_highlight = QtGui.QColor(COLORS['graph']['index']['plug_highlight'])
    brush = QtGui.QBrush(plug_highlight if hover == 1 else background)
    painter.setBrush(brush)
    painter.drawEllipse(get_index_inplug_rect(rect))

    brush = QtGui.QBrush(plug_highlight if hover == 2 else background)
    painter.setBrush(brush)
    painter.drawEllipse(get_index_outplug_rect(rect))

    painter.setBrush(background)
    if hover == 3:
        color = COLORS['graph']['index']['border_highlight']
        pen = QtGui.QPen(QtGui.QColor(color))
        pen.setWidth(3)
        painter.setPen(pen)
    painter.drawRoundedRect(get_index_rect(rect), 3, 3)

    color = COLORS['graph']['index']['item']['background']
    brush = QtGui.QBrush(QtGui.QColor(color))
    painter.setBrush(brush)
    if hover == 4:
        color = COLORS['graph']['index']['item']['border_highlight']
        pen = QtGui.QPen(QtGui.QColor(color))
    else:
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)
    painter.drawEllipse(get_fingerstate_rect(rect))
    if hover == 5:
        color = COLORS['graph']['index']['item']['border_highlight']
        pen = QtGui.QPen(QtGui.QColor(color))
    else:
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)
    painter.drawEllipse(get_behavior_rect(rect))


def get_index_rect(rect):
    offset = 15
    return QtCore.QRect(
        rect.left() + offset, 
        rect.top(),
        rect.width() - (offset * 2),
        rect.height())


def get_index_inplug_rect(rect):
    width = 10
    return QtCore.QRect(
        rect.left(), rect.top() + (rect.height() / 2) - (width / 2),
        width, width)


def get_index_outplug_rect(rect):
    width = 10
    return QtCore.QRect(
        rect.left() + rect.width() - width,
        rect.top() + (rect.height() / 2) - (width / 2),
        width, width)


def get_fingerstate_rect(rect):
    offset = 3
    width = rect.height() - (offset * 2)
    left = rect.left() + ((rect.width() / 6) * 2)
    return QtCore.QRect(left, rect.top() + offset, width, width)


def get_behavior_rect(rect):
    offset = 3
    width = rect.height() - (offset * 2)
    left = rect.left() + ((rect.width() / 6) * 3)
    return QtCore.QRect(left, rect.top() + offset, width, width)


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
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            draw_background(painter, self.rect())
            column = QtCore.QRect(50, 50, 150, 300)
            draw_column_background(painter, column, 1)
            column = QtCore.QRect(250, 50, 150, 300)
            draw_column_background(painter, column, 2)
            column = QtCore.QRect(450, 50, 150, 300)
            draw_column_background(painter, column, 3)
            column = QtCore.QRect(650, 50, 150, 300)
            draw_column_background(painter, column, 4)

            index = QtCore.QRect(60, 100, 130, 25)
            draw_index(painter, index, 0, hover=0)
            index = QtCore.QRect(60, 140, 130, 25)
            draw_index(painter, index, 0, hover=3)
            index = QtCore.QRect(60, 180, 130, 25)
            draw_index(painter, index, 0, hover=2)
            index = QtCore.QRect(60, 220, 130, 25)
            draw_index(painter, index, 0, hover=4)
            index = QtCore.QRect(60, 260, 130, 25)
            draw_index(painter, index, 0, hover=5)

    import sys
    application = QtGui.QApplication(sys.argv)
    windows = MainTest()
    windows.show()
    application.exec_()