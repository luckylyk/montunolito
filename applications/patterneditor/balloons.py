from PyQt4 import QtGui, QtCore
from draws import draw_balloon, draw_texts, draw_balloon_header_button
from coordinates import (
    get_balloon_background_path, get_balloon_drawable_rect,
    get_balloon_figure_rect, get_balloon_fingerstateselecter_rect,
    get_ballon_validator_rect, get_balloon_rejecter_path,
    get_balloon_approver_path, get_balloon_behavior_slider_rect)
from figure import Figure, FingerstateSelecter
from slider import Slider


class Balloon(QtGui.QDialog):
    TITLE = "Ballon Title"

    def __init__(self, size=None, parent=None):
        super().__init__(parent, QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self._rejecter_state = False
        self._approver_state = False
        if size:
            self.setFixedSize(size)
            self.move(
                QtGui.QCursor().pos().x() - 20,
                QtGui.QCursor().pos().y() - self.height())

        self.drawable_rect = get_balloon_drawable_rect(self.rect())
        self._rejecter_rect = get_ballon_validator_rect(self.rect(), index=0)
        self._rejecter_path = get_balloon_rejecter_path(self._rejecter_rect)
        self._approver_rect = get_ballon_validator_rect(self.rect(), index=1)
        self._approver_path = get_balloon_approver_path(self._approver_rect)
        self._background_path = get_balloon_background_path(self.rect())
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
        draw_balloon(painter, self._background_path, self.TITLE)
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


class BehaviorBalloon(Balloon):
    TITLE = 'Behaviors'

    def __init__(self, parent=None):
        super().__init__(size=QtCore.QSize(200, 150), parent=parent)
        self._mousepressed = False
        self._melodic_slider = Slider(
            get_balloon_behavior_slider_rect(
                self.drawable_rect, 0), value=2, max=6)
        self._arpegic_slider = Slider(
            get_balloon_behavior_slider_rect(
                self.drawable_rect, 1), value=4, max=6)
        self._static_slider = Slider(
            get_balloon_behavior_slider_rect(
                self.drawable_rect, 2), value=1, max=6)
        self._sliders = (
            self._melodic_slider,
            self._arpegic_slider,
            self._static_slider)

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
            self.drawable_rect, value=connection.strongness(), max=10)
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

    def __init__(self, figure, parent=None):
        size = QtCore.QSize(180, 220)
        super().__init__(size=size, parent=parent)
        self.figure = Figure(
            figure, get_balloon_figure_rect(self.drawable_rect))
        self.fingerstate_selecter = FingerstateSelecter(
            get_balloon_fingerstateselecter_rect(self.drawable_rect))

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
