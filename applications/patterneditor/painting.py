from PyQt5 import QtGui, QtCore
import math


COLORS = {
    'menu': '#202020',
    'note': {
        'normal': 'black',
        'highlight': '#DDDD55',
        'selected': 'red'},
    'fingerstates': {
        'pressed': '#AA4455',
        'released': '#ABABAB'},
    'balloon': {
        'closer':{
            'hover': '#d0a895',
            'free': "#B3B3B3",
            'cross': "#4b4b4b"},
        'border': '#4b4b4b',
        'title': '#4b4b4b',
        'background': '#c8c8c8',
        'text': '#6E6E6E'},
    'slider': {
        'normal': '#343434',
        'highlight': '#DDDD55',
        'pressed': '#AA4455'},
    'graph': {
        'background': '#303030',
        'grid':  '#383838',
        'row': {
            'number':{
                'highlight': 'yellow',
                'normal': 'white'},
            'background': {
                'highlight': '#535353',
                'normal': '#4a4a4a'}},
        'connection': {
            'dead': '#252525',
            'min': '#440715',
            'max': '#AA4455',
            'highlight': '#DDDD55'},
        'index':{
            'mas': {
                'min': '#313100',
                'max': '#858565'},
            'background': {
                'dead': '#252525',
                'min': '#302512',
                'max': 'orange'},
            'border': {
                'highlight':  '#449999',
                'selected': '#dfdfdf'},
            'plug_highlight': '#AA4455',
            'item': {
                'background': '#9f9f9f',
                'border': {
                    'highlight':  '#449999',
                    'selected': '#dfdfdf'}}}}
}


def mix_colors(color_min, color_max, percent):
    zr, zg, zb, _ = color_min.getRgb()
    hr, hg, hb, _ = color_max.getRgb()

    percent = (100 - percent) / 100.0
    ro = (abs(zr - hr) * percent)
    go = (abs(zg - hg) * percent)
    bo = (abs(zb - hb) * percent)

    r = hr - ro if zr < hr else hr + ro
    g = hg - go if zg < hg else hg + go
    b = hb - bo if zb < hb else hb + bo

    return QtGui.QColor(r, g, b)


def draw_balloon(painter, path, title):
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    pen.setWidth(0)
    pen.setJoinStyle(QtCore.Qt.MiterJoin)

    painter.setBrush(
        QtGui.QBrush(QtGui.QColor(COLORS['balloon']['background'])))
    painter.setPen(pen)

    painter.drawPath(path)

    pen = QtGui.QPen(QtGui.QColor(COLORS['balloon']['title']))
    painter.setPen(pen)

    font = QtGui.QFont()
    font.setBold(True)
    font.setPointSize(12)
    painter.setFont(font)
    painter.drawText(20, 25, title)


def draw_balloon_header_button(painter, rect, path, state):
    state = 'hover' if state is True else 'free'
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)

    brush = QtGui.QBrush(QtGui.QColor(COLORS['balloon']['closer'][state]))
    painter.setBrush(brush)

    painter.drawRoundedRect(rect, 5, 5)
    pen = QtGui.QPen(QtGui.QColor(COLORS['balloon']['closer']['cross']))
    pen.setWidth(2)
    painter.setPen(pen)

    painter.drawPath(path)


def draw_balloon_text(painter, point, text):
    font = QtGui.QFont()
    font.setBold(False)
    font.setPointSize(11)
    painter.setFont(font)

    pen = QtGui.QPen(QtGui.QColor(COLORS['balloon']['text']))
    painter.setPen(pen)
    painter.drawText(point, text)


def draw_background(painter, spacing, rect):
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)

    brush = QtGui.QBrush(QtGui.QColor(COLORS['graph']['background']))
    painter.setBrush(brush)
    painter.drawRect(rect)

    pen = QtGui.QPen(QtGui.QColor(COLORS['graph']['grid']))
    painter.setPen(pen)
    left = 0
    while left < rect.width():
        left += spacing
        painter.drawLine(
            QtCore.QPoint(left, 0),
            QtCore.QPoint(left, rect.height()))

    top = 0
    while top < rect.height():
        top += spacing
        painter.drawLine(
            QtCore.QPoint(0, top),
            QtCore.QPoint(rect.width(), top))


def draw_row_background(painter, path, hover=False):
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)
    if hover is True:
        color = COLORS['graph']['row']['background']['highlight']
    else:
        color = COLORS['graph']['row']['background']['normal']

    brush = QtGui.QBrush(QtGui.QColor(color))
    painter.setBrush(brush)
    painter.drawPath(path)


def draw_row_plus(painter, rect, hover=False):
    if hover is True:
        color = COLORS['graph']['row']['number']['highlight']
    else:
        color = COLORS['graph']['row']['number']['normal']

    text_option = QtGui.QTextOption()
    text_option.setAlignment(QtCore.Qt.AlignCenter)
    pen = QtGui.QPen(QtGui.QColor(color))
    painter.setPen(pen)
    font = QtGui.QFont()
    font.setBold(True)
    font.setPointSize(rect.width() * 0.6)
    painter.setFont(font)
    painter.drawText(QtCore.QRectF(rect), '+', text_option)


def draw_index(painter, index, highlight_rects=None):
    highlight_rects = highlight_rects or []
    occurence = index.occurence
    if occurence:
        background = mix_colors(
            QtGui.QColor(COLORS['graph']['index']['background']['min']),
            QtGui.QColor(COLORS['graph']['index']['background']['max']),
            occurence)
    else:
        background = QtGui.QColor(
            COLORS['graph']['index']['background']['dead'])

    draw_index_plug(
        painter,
        index.inplug_rect,
        bgcolor=background,
        hover=index.inplug_rect in highlight_rects)

    draw_index_plug(
        painter,
        index.outplug_rect,
        bgcolor=background,
        hover=index.outplug_rect in highlight_rects)

    draw_index_body(
        painter,
        index.body_rect,
        bgcolor=background,
        selected=index.selected,
        hover=index.body_rect in highlight_rects)

    draw_index_button(
        painter,
        index.figure_rect,
        selected=index.selected,
        hover=index.figure_rect in highlight_rects)

    draw_index_button(
        painter,
        index.behavior_rect,
        selected=index.selected,
        hover=index.behavior_rect in highlight_rects)


def draw_index_plug(painter, rect, bgcolor=None, hover=False):
    if hover is True:
        color = QtGui.QColor(COLORS['graph']['index']['plug_highlight'])
    else:
        color = QtGui.QColor(bgcolor)
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)
    brush = QtGui.QBrush(color)
    painter.setBrush(brush)
    painter.drawEllipse(rect)


def draw_index_body(painter, rect, bgcolor=None, selected=False, hover=False):
    painter.setBrush(bgcolor)
    if selected is True:
        color = QtGui.QColor(COLORS['graph']['index']['border']['selected'])
    elif hover is True:
        color = QtGui.QColor(COLORS['graph']['index']['border']['highlight'])
    else:
        color = QtGui.QColor(0, 0, 0, 0)
    pen = QtGui.QPen(QtGui.QColor(color))
    pen.setWidth(3)
    painter.setPen(pen)
    painter.drawRoundedRect(rect, 3, 3)


def draw_index_button(painter, rect, selected=False, hover=False):
    if selected is True:
        color = QtGui.QColor(
            COLORS['graph']['index']['item']['border']['selected'])
    elif hover is True:
        color = QtGui.QColor(
            COLORS['graph']['index']['item']['border']['selected'])
    else:
        color = QtGui.QColor(0, 0, 0, 0)

    pen = QtGui.QPen(color)
    pen.setWidth(3)
    painter.setPen(pen)
    background_color = COLORS['graph']['index']['item']['background']
    brush = QtGui.QBrush(QtGui.QColor(background_color))
    painter.setBrush(brush)
    painter.drawRoundedRect(rect, 5, 5)


def draw_connection(painter, connection, hover=False):
    painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 75))
    painter.setBrush(brush)
    painter.drawEllipse(connection.handler_rect)

    if hover:
        color = QtGui.QColor(COLORS['graph']['connection']['highlight'])
    elif not connection.strongness:
        color = QtGui.QColor(COLORS['graph']['connection']['dead'])
    else:
        color = mix_colors(
            QtGui.QColor(COLORS['graph']['connection']['min']),
            QtGui.QColor(COLORS['graph']['connection']['max']),
            (connection.strongness / 10) * 100)
    pen = QtGui.QPen(color)
    pen.setWidth(2)
    painter.setPen(pen)

    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
    painter.setBrush(brush)
    painter.drawPath(connection.path)

    pen.setJoinStyle(QtCore.Qt.MiterJoin)
    painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))
    brush = QtGui.QBrush(color)
    painter.setBrush(brush)
    painter.drawPath(connection.triangle_path)


def draw_note_path(painter, path, selected=False, hover=False):
    if selected is True:
        color = QtGui.QColor(COLORS['note']['selected'])
    elif hover is True:
        color = QtGui.QColor(COLORS['note']['highlight'])
    else:
        color = QtGui.QColor(COLORS['note']['normal'])
    painter.setPen(QtGui.QPen(color))
    painter.setBrush(QtGui.QBrush(color))
    painter.drawPath(path)


def draw_slider_path(
        painter, path, background=False, hover=False, pressed=False):
    if pressed is True:
        color = QtGui.QColor(COLORS['slider']['pressed'])
    elif hover is True:
        color = QtGui.QColor(COLORS['slider']['highlight'])
    else:
        color = QtGui.QColor(COLORS['slider']['normal'])
    if background is True:
        painter.setBrush(QtGui.QBrush(color))
    else:
        painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 0)))
    painter.setPen(QtGui.QPen(color))
    painter.drawPath(path)


def draw_menu_background(painter, rect):
    painter.setBrush(QtGui.QBrush(QtGui.QColor(COLORS['menu'])))
    painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))
    painter.drawRect(rect)


def draw_icon(painter, icon, rect, hover=False, clicked=False):
    if clicked is True:
        mode = QtGui.QIcon.Selected
    elif hover is True:
        mode = QtGui.QIcon.Active
    else:
        mode = QtGui.QIcon.Normal
    icon.paint(painter, rect, mode=mode)


def get_icon(pixmappath=None, mirrored=False):
    pixmap = QtGui.QPixmap(pixmappath)
    if mirrored:
        pixmap = pixmap.transformed(QtGui.QTransform().scale(-1, 1))

    image = QtGui.QImage(pixmap)
    active_image = QtGui.QImage(
        image.width(), image.height(), image.format())
    selected_image = QtGui.QImage(
        image.width(), image.height(), image.format())

    for i in range(image.width()):
        for j in range(image.height()):
            color = image.pixelColor(i, j)
            active_image.setPixelColor(i, j, color.lighter(120))
            selected_image.setPixelColor(i, j, color.lighter(80))

    icon = QtGui.QIcon(pixmap)

    active_pixmap = QtGui.QPixmap()
    active_pixmap.convertFromImage(active_image)
    icon.addPixmap(active_pixmap, icon.Active)

    selected_pixmap = QtGui.QPixmap()
    selected_pixmap.convertFromImage(selected_image)
    icon.addPixmap(selected_pixmap, icon.Selected)

    return icon


def draw_mas(painter, rects, melodic=50, arpegic=50, static=50):
    font = QtGui.QFont()
    text_option = QtGui.QTextOption()
    text_option.setAlignment(QtCore.Qt.AlignCenter)

    min_color = QtGui.QColor(COLORS['graph']['index']['mas']['min'])
    max_color = QtGui.QColor(COLORS['graph']['index']['mas']['max'])

    letters = (
        ('M', melodic, rects[0]),
        ('A', arpegic, rects[1]),
        ('S', static, rects[2]))
    for text, value, rect in letters:
        total = sum([melodic, arpegic, static])
        percent = (value / total) * 100 if total else total
        color = mix_colors(min_color, max_color, percent)
        font.setBold(value == max(melodic, arpegic, static))
        font.setPointSize(rect.width() * 0.9)
        painter.setFont(font)
        painter.setPen(QtGui.QPen(color))
        painter.drawText(rect, text, text_option)