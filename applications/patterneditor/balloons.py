from PyQt5 import QtWidgets, QtGui, QtCore
from painting import (
    draw_balloon, draw_balloon_header_button, draw_balloon_text)
from context import DrawContext
from geometries import (
    get_balloon_background_path, get_balloon_drawable_rect,
    get_balloon_figure_rect, get_balloon_fingerstateselecter_rect,
    get_balloon_validator_rect, get_balloon_rejecter_path,
    get_balloon_approver_path, get_balloon_behavior_slider_rect,
    get_balloon_behavior_text_point, get_balloon_spike_point)
from figure import IGFigure, IGFingerstateSelecter
from slider import IGSlider


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

    def exec_(self, point=None):
        point = point or self.cursor()
        self.move(point - self.spike_tip)
        result = super().exec_()
        return result == QtWidgets.QDialog.Accepted

    def mouseMoveEvent(self, event):
        if self._rejecter_rect.contains(event.pos()) != self._rejecter_state:
            self._rejecter_state = self._rejecter_rect.contains(event.pos())
            self.repaint()
            return
        if self._approver_rect.contains(event.pos()) != self._approver_state:
            self._approver_state = self._approver_rect.contains(event.pos())
            self.repaint()
            return

    def cursor(self):
        return self.mapFromGlobal(QtGui.QCursor.pos())

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

    @property
    def spike_tip(self):
        return get_balloon_spike_point(self.drawcontext, self.rect())

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


class BehaviorsBalloon(Balloon):
    TITLE = 'Behaviors'
    BEHAVIOR_NAMES = 'Melodic', 'Arpegic', 'Static'

    def __init__(self, behaviors, parent=None):
        super().__init__(size=QtCore.QSize(210, 150), parent=parent)
        self._mousepressed = False
        self._melodic_slider = IGSlider(
            get_balloon_behavior_slider_rect(self.drawable_rect, 0),
            value=behaviors['melodic'],
            maxvalue=6)
        self._arpegic_slider = IGSlider(
            get_balloon_behavior_slider_rect(self.drawable_rect, 1),
            value=behaviors['arpegic'],
            maxvalue=6)
        self._static_slider = IGSlider(
            get_balloon_behavior_slider_rect(self.drawable_rect, 2),
            value=behaviors['static'],
            maxvalue=6)
        self._igsliders = (
            self._melodic_slider,
            self._arpegic_slider,
            self._static_slider)
        self._text_points = [
            get_balloon_behavior_text_point(
                self.drawcontext, self.drawable_rect, index)
            for index in range(3)]

    @property
    def behaviors(self):
        return {
            'melodic': self._melodic_slider.value,
            'arpegic': self._arpegic_slider.value,
            'static': self._static_slider.value}

    def hovered_slider(self):
        for igslider in self._igsliders:
            if igslider.rect.contains(self.cursor()):
                return igslider

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
            draw_balloon_text(painter, point, self.BEHAVIOR_NAMES[i])

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
    TITLE = 'Relationship'

    def __init__(self, value, parent=None):
        super().__init__(size=QtCore.QSize(200, 115), parent=parent)
        self._igslider = IGSlider(
            self.drawable_rect,
            value=value,
            maxvalue=10,
            drawcontext=self.drawcontext)
        self._mousepressed = False

    @property
    def value(self):
        return self._igslider.value

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self._mousepressed is True:
            self._igslider.set_value(self.cursor())
        self.repaint()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self._igslider.set_value(self.cursor())
        self._mousepressed = self.drawable_rect.contains(self.cursor())
        self.repaint()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self._mousepressed = False

    def paint(self, painter):
        super().paint(painter)
        self._igslider.draw(painter, self.cursor(), pressed=self._mousepressed)


class FigureBalloon(Balloon):
    TITLE = 'Figure'

    def __init__(self, figure, parent=None):
        size = QtCore.QSize(180, 220)
        super().__init__(size=size, parent=parent)

        self._igfigure = IGFigure(
            figure,
            get_balloon_figure_rect(self.drawcontext, self.drawable_rect))
        selected_rect = get_balloon_fingerstateselecter_rect(self.drawable_rect)
        self._igfingerstate_selecter = IGFingerstateSelecter(selected_rect)

    @property
    def figure(self):
        return self._igfigure.figure

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.repaint()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self._igfigure.set_selected_state(self.cursor())
        if self._igfigure.selected is None:
            self.repaint()
            return

        hovered = self._igfingerstate_selecter.get_hovered_index(self.cursor())
        if hovered is None:
            self.repaint()
            return
        self._igfigure.set_fingerstate(self._igfigure.selected, hovered)
        self.repaint()

    def paint(self, painter):
        super().paint(painter)
        self._igfigure.draw(painter, self.cursor())
        self._igfingerstate_selecter.draw(painter, self.cursor())
