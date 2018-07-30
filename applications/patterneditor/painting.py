from PyQt5 import QtGui, QtCore


COLORS = {
    'menu': '#202020',
    'note':
        {
            'normal': 'black',
            'highlight': '#DDDD55',
            'selected': 'red'
        },
    'fingerstates':
        {
            'pressed': '#AA4455',
            'released': '#ABABAB',
        },
    'balloon':
        {
            'closer':
                {
                    'hover': '#d0a895',
                    'free': "#B3B3B3",
                    'cross': "#4b4b4b"
                },
            'border': '#4b4b4b',
            'title': '#4b4b4b',
            'background': '#c8c8c8',
            'text': '#6E6E6E'
        },
    'slider':
        {
            'normal': '#343434',
            'highlight': '#DDDD55',
            'pressed': '#AA4455'
        },
    'graph':
        {
            'background': '#292929',
            'grid':  '#343434',
            'row':
                {
                    'background': '#4a4a4a',
                    'background_highlight': '#535353',
                    'number': 'white'
                },
            'index':
                {
                    'background':
                        {
                            'min': 'red',
                            'max': 'green'
                        },
                    'border':
                        {
                            'highlight':  '#449999',
                            'selected': '#dfdfdf',
                        },
                    'plug_highlight': '#AA4455',
                    'item':
                        {
                            'background': '#9f9f9f',

                            'border':
                                {
                                    'highlight':  '#449999',
                                    'selected': '#dfdfdf',
                                },
                        },
                    'path':
                        {
                            'normal': '#AA4455',
                            'highlight': '#DDDD55',
                        },
                }
        },
}


def mix_colors(color_min, color_max, percent):
    zr, zg, zb, _ = color_min.getRgb()
    hr, hg, hb, _ = color_max.getRgb()

    r = abs(zr - hr) * (percent / 100) + min(zr, hr)
    g = abs(zg - hg) * (percent / 100) + min(zg, hg)
    b = abs(zb - hb) * (percent / 100) + min(zb, hb)
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


def draw_row_background(painter, rect, number, hover=False):
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)
    if hover is True:
        color = COLORS['graph']['row']['background_highlight']
    else:
        color = COLORS['graph']['row']['background']
    brush = QtGui.QBrush(QtGui.QColor(color))
    painter.setBrush(brush)
    painter.drawRoundedRect(
        rect.left(), rect.top() + 20, rect.width(), rect.height() - 5, 10, 10)

    painter.drawRoundedRect(
        rect.left() + rect.width() - 30, rect.top(), 30, 40, 10, 10)

    pen = QtGui.QPen(QtGui.QColor(COLORS['graph']['row']['number']))
    painter.setPen(pen)

    font = QtGui.QFont()
    font.setBold(True)
    font.setPointSize(12)
    painter.setFont(font)
    painter.drawText(
        rect.left() + rect.width() - 20, rect.top() + 20, str(number))


def draw_index(
        painter, occurence, inplug_rect, outplug_rect, body_rect,
        fingerstate_rect, behavior_rect, selected=False, highlight_rects=None):
    highlight_rects = highlight_rects or []

    background = mix_colors(
        QtGui.QColor(COLORS['graph']['index']['background']['min']),
        QtGui.QColor(COLORS['graph']['index']['background']['max']),
        occurence)

    draw_index_plug(
        painter,
        inplug_rect,
        bgcolor=background,
        hover=inplug_rect in highlight_rects)

    draw_index_plug(
        painter,
        outplug_rect,
        bgcolor=background,
        hover=outplug_rect in highlight_rects)

    draw_index_body(
        painter,
        body_rect,
        bgcolor=background,
        selected=selected,
        hover=body_rect in highlight_rects)

    draw_index_button(
        painter,
        fingerstate_rect,
        selected=selected,
        hover=fingerstate_rect in highlight_rects)

    draw_index_button(
        painter,
        behavior_rect,
        selected=selected,
        hover=behavior_rect in highlight_rects)


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


def draw_connection(painter, path, handler_rect, hover=False):
    if hover:
        color = QtGui.QColor(COLORS['graph']['index']['path']['highlight'])
    else:
        color = QtGui.QColor(COLORS['graph']['index']['path']['normal'])
    pen = QtGui.QPen(color)
    pen.setWidth(2)
    painter.setPen(pen)

    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
    painter.setBrush(brush)

    painter.drawPath(path)

    brush = QtGui.QBrush(color)
    painter.setBrush(brush)
    painter.drawEllipse(handler_rect)


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