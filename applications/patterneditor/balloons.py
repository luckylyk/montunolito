from PyQt5 import QtWidgets, QtGui, QtCore
from painting import (
    draw_balloon, draw_balloon_header_button, draw_balloon_text)
from context import DrawContext
from geometries import (
    get_balloon_background_path, get_balloon_drawable_rect,
    get_balloon_figure_rect, get_balloon_fingerstateselecter_rect,
    get_balloon_validator_rect, get_balloon_rejecter_path,
    get_balloon_approver_path, get_balloon_behavior_slider_rect,
    get_balloon_behavior_text_point)
from figure import Figure, FingerstateSelecter
from slider import Slider


class Balloon(QtWidgets.QDialog):
    TITLE = "Ballon Title"

    def __init__(self, size=None, drawcontext=DrawContext(), parent=None):
        super().__init__(parent, QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.drawcontext = drawcontext
        self._rejecter_state = False
        self._approver_state = False
        if size:
            self.setFixedSize(size)
            self.move(
                QtGui.QCursor().pos().x() - 20,
                QtGui.QCursor().pos().y() - self.height())

        self.drawable_rect = get_balloon_drawable_rect(
            self.drawcontext, self.rect())
        self._rejecter_rect = get_balloon_validator_rect(
            self.drawcontext, self.rect(), index=0)
        self._rejecter_path = get_balloon_rejecter_path(self._rejecter_rect)
        self._approver_rect = get_balloon_validator_rect(
            self.drawcontext, self.rect(), index=1)
        self._approver_path = get_balloon_approver_path(self._approver_rect)
        self._background_path = get_balloon_background_path(
            self.drawcontext, self.rect())
        self.setMouseTracking(True)

    def cursor(self):
        return self.mapFromGlobal(QtGui.QCursor.pos())

    def mouseMoveEvent(self, event):
        if self._rejecter_rect.contains(event.pos()) != self._rejecter_state:
            self._rejecter_state = self._rejecter_rect.contains(event.pos())
            self.repaint()
            return
        if self._approver_rect.contains(event.pos()) != self._approver_state:
            self._approver_state = self._approver_rect.contains(event.pos())
            self.repaint()
            return

    def mouseReleaseEvent(self, _):
        if self._rejecter_state:
            self.reject()
        if self._approver_state:
            self.accept()

    def keyPressEvent(self, event):
        accept_keys = QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return
        if event.key() in accept_keys:
            self.accept()
        if event.key() == QtCore.Qt.Key_Escape:
            self.reject()

    def paintEvent(self, _):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def paint(self, painter):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        draw_balloon(
            painter,
            self._background_path,
            self.TITLE)
        draw_balloon_header_button(
            painter,
            self._rejecter_rect,
            self._rejecter_path,
            self._rejecter_state)
        draw_balloon_header_button(
            painter,
            self._approver_rect,
            self._approver_path,
            self._approver_state)


BEHAVIOR_NAMES = 'Melodic', 'Arpegic', 'Static'


class BehaviorBalloon(Balloon):
    TITLE = 'Behaviors'

    def __init__(self, index, parent=None):
        super().__init__(size=QtCore.QSize(210, 150), parent=parent)
        self._index = index
        self._mousepressed = False
        self._melodic_slider = Slider(
            get_balloon_behavior_slider_rect(self.drawable_rect, 0),
            value=index.behaviors['melodic'],
            maxvalue=6)
        self._arpegic_slider = Slider(
            get_balloon_behavior_slider_rect(self.drawable_rect, 1),
            value=index.behaviors['arpegic'],
            maxvalue=6)
        self._static_slider = Slider(
            get_balloon_behavior_slider_rect(self.drawable_rect, 2),
            value=index.behaviors['static'],
            maxvalue=6)
        self._sliders = (
            self._melodic_slider,
            self._arpegic_slider,
            self._static_slider)
        self._text_points = [
            get_balloon_behavior_text_point(
                self.drawcontext, self.drawable_rect, index)
            for index in range(3)]

    def hovered_slider(self):
        for slider in self._sliders:
            if slider.rect.contains(self.cursor()):
                return slider

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self._mousepressed is True:
            slider = self.hovered_slider()
            if slider:
                slider.set_value(self.cursor())
        self.repaint()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        slider = self.hovered_slider()
        if slider:
            slider.set_value(self.cursor())
        self._mousepressed = self.drawable_rect.contains(self.cursor())
        self.repaint()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self._mousepressed = False

    def paint(self, painter):
        super().paint(painter)
        for i, point in enumerate(self._text_points):
            draw_balloon_text(painter, point, BEHAVIOR_NAMES[i])

        slider = self.hovered_slider()
        self._melodic_slider.draw(
            painter,
            self.cursor(),
            pressed=slider == self._melodic_slider and self._mousepressed)
        self._arpegic_slider.draw(
            painter,
            self.cursor(),
            pressed=slider == self._arpegic_slider and self._mousepressed)
        self._static_slider.draw(
            painter,
            self.cursor(),
            pressed=slider == self._static_slider and self._mousepressed)


class ConnectionBalloon(Balloon):
    TITLE = 'Strongness'

    def __init__(self, connection, parent=None):
        super().__init__(size=QtCore.QSize(200, 115), parent=parent)
        self._connection = connection
        self._slider = Slider(
            self.drawable_rect,
            value=connection.strongness(),
            maxvalue=10,
            drawcontext=self.drawcontext)
        self._mousepressed = False

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self._mousepressed is True:
            self._slider.set_value(self.cursor())
        self.repaint()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self._slider.set_value(self.cursor())
        self._mousepressed = self.drawable_rect.contains(self.cursor())
        self.repaint()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self._mousepressed = False

    def paint(self, painter):
        super().paint(painter)
        self._slider.draw(painter, self.cursor(), pressed=self._mousepressed)


class FigureBalloon(Balloon):
    TITLE = 'Figure'

    def __init__(self, index, parent=None):
        size = QtCore.QSize(180, 220)
        super().__init__(size=size, parent=parent)
        self._index = index
        self.figure = Figure(
            index.figure,
            get_balloon_figure_rect(self.drawcontext, self.drawable_rect))
        selected_rect = get_balloon_fingerstateselecter_rect(self.drawable_rect)
        self.fingerstate_selecter = FingerstateSelecter(selected_rect)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.repaint()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.figure.set_selected_state(self.cursor())
        if self.figure.selected is None:
            self.repaint()
            return

        hovered = self.fingerstate_selecter.get_hovered_index(self.cursor())
        if hovered is None:
            self.repaint()
            return
        self.figure.set_fingerstate(self.figure.selected, hovered)
        self.repaint()

    def paint(self, painter):
        super().paint(painter)
        self.figure.draw(painter, self.cursor())
        self.fingerstate_selecter.draw(painter, self.cursor())
