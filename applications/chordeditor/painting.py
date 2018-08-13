from PyQt5 import QtCore, QtGui

def draw_note_item(painter, noteitem):
    painter.drawRect(noteitem.rect)
    option = QtGui.QTextOption()
    option.setAlignment(QtCore.Qt.AlignCenter)
    font = QtGui.QFont()
    font.setBold(True)
    size = min([noteitem.rect.width(), noteitem.rect.height()]) * .66
    font.setPixelSize(size)
    painter.setFont(font)
    text_rect = QtCore.QRectF(noteitem.rect)
    painter.drawText(text_rect, noteitem.displayname, option)


def draw_staff(painter, path):
    painter.drawPath(path)
