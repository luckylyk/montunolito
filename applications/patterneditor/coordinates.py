from PyQt4 import QtCore, QtGui

SLIDER_SEGMENT_HEIGHT = 3

INDEX_HEIGHT = 25
INDEX_WIDTH = 130
INDEX_SPACING = 15
INDEX_PLUG_WIDTH = 10
INDEX_BODY_RIGHTLEFT_PADDING = 15

ROWS_TOP = 25
ROWS_LEFT = 35
ROWS_SPACING = 50
ROWS_PADDING = 10
ROWS_WIDTH = INDEX_WIDTH + (ROWS_PADDING * 2)
ROWS_HEADER_SPACE = 50
ROWS_BOTTOM_SPACE = 0

CONNECTION_HANDLER_SIZE = 10
BEAM_CONNECTION_WIDTH = 5

BALLOON_SPIKE_HEIGHT = 29
BALLOON_SPIKE_BASE_LEFT = 30
BALLOON_SPIKE_TIP_LEFT = 20
BALLOON_SPIKE_BASE_RIGHT = 50
BALLOON_ROUNDNESS = 22
BALLOON_DRAWABLE_LEFT_PADDING = 15
BALLOON_DRAWABLE_TOP_PADDING = 40
BALLOON_DRAWABLE_RIGHT_PADDING = 25
BALLOON_DRAWABLE_BOTTOM_PADDING = 40
BALLOON_HEADER_VALIDATOR_SIZE = 20
BALLOON_HEADER_VALIDATOR_LEFT_PADDING = 30
BALLOON_HEADER_VALIDATOR_TOP_PADDING = 10
BALLOON_HEADER_VALIDATOR_SPACING = 3

FIGURE_BALLON_SPACING = 10

GRID_SPACING = 33
PATTERN_WIDTH = 120


def get_balloon_drawable_rect(rect):
    return QtCore.QRect(
        BALLOON_DRAWABLE_LEFT_PADDING,
        BALLOON_DRAWABLE_TOP_PADDING,
        rect.width() - BALLOON_DRAWABLE_LEFT_PADDING -
        BALLOON_DRAWABLE_RIGHT_PADDING,
        rect.height() - BALLOON_DRAWABLE_TOP_PADDING -
        BALLOON_DRAWABLE_BOTTOM_PADDING)


def get_balloon_background_path(rect):
    path = QtGui.QPainterPath(rect.topLeft())
    path.addRoundedRect(
        rect.top(), rect.left(), rect.width(),
        rect.height() - BALLOON_SPIKE_HEIGHT,
        BALLOON_ROUNDNESS, BALLOON_ROUNDNESS)

    spike_point_1 = QtCore.QPoint(
        BALLOON_SPIKE_BASE_LEFT,
        rect.height() - BALLOON_SPIKE_HEIGHT)
    spike_point_2 = QtCore.QPoint(BALLOON_SPIKE_TIP_LEFT, rect.height())
    spike_point_3 = QtCore.QPoint(
        BALLOON_SPIKE_BASE_RIGHT,
        rect.height() - BALLOON_SPIKE_HEIGHT)
    spike = QtGui.QPolygonF([spike_point_1, spike_point_2, spike_point_3])
    path.addPolygon(spike)
    return path


def get_ballon_validator_rect(balloonrect, index=0):
    offset = (
        (BALLOON_HEADER_VALIDATOR_SIZE + BALLOON_HEADER_VALIDATOR_SPACING) *
        index)
    return QtCore.QRect(
        balloonrect.right() - BALLOON_HEADER_VALIDATOR_LEFT_PADDING - offset,
        BALLOON_HEADER_VALIDATOR_TOP_PADDING,
        BALLOON_HEADER_VALIDATOR_SIZE,
        BALLOON_HEADER_VALIDATOR_SIZE)


def get_balloon_rejecter_path(rejecterrect):
    shrink = 5 # move in constant
    path = QtGui.QPainterPath(
        QtCore.QPoint(rejecterrect.left() + shrink, rejecterrect.top() + shrink))
    path.lineTo(
        QtCore.QPoint(
            rejecterrect.right() - shrink,
            rejecterrect.bottom() - shrink))
    path.moveTo(
        QtCore.QPoint(
            rejecterrect.right() - shrink,
            rejecterrect.top() + shrink))
    path.lineTo(
        QtCore.QPoint(
            rejecterrect.left() + shrink,
            rejecterrect.bottom() - shrink))
    return path


def get_balloon_approver_path(approverrect):
    shrink = 5 # move in constant
    left, right = approverrect.left(), approverrect.right()
    top, bottom = approverrect.top(), approverrect.bottom()

    path = QtGui.QPainterPath(
        QtCore.QPoint(
            left + shrink,
            top + (shrink * 1.5)))
    path.lineTo(
        QtCore.QPoint(
            left + ((right - left) * .45),
            bottom - shrink))
    path.lineTo(
        QtCore.QPoint(
            right - shrink,
            top + shrink))
    return path


def get_balloon_spike_point(balloonrect):
    return QtCore.QPoint(BALLOON_SPIKE_TIP_LEFT, balloonrect.height())


def get_balloon_figure_rect(drawablerect):
    return QtCore.QRect(
        drawablerect.left(),
        drawablerect.top(),
        drawablerect.width(),
        (drawablerect.height() / 3 * 2) - FIGURE_BALLON_SPACING)


def get_balloon_fingerstateselecter_rect(drawablerect):
    height = drawablerect.height() / 3
    return QtCore.QRect(
        drawablerect.left(),
        drawablerect.top() + (height * 2),
        drawablerect.width(),
        height)


def get_balloon_behavior_slider_rect(rect, index):
    offset = rect.width() / 3
    left = rect.left() + offset
    width = rect.width() - offset
    height = rect.height() / 3
    top = rect.top() + (height * index)
    return QtCore.QRect(left, top, width, height)



def get_index_figure_rect(rect):
    offset = 3
    width = rect.height() - (offset * 2)
    left = rect.left() + ((rect.width() / 6) * 2)
    return QtCore.QRect(left, rect.top() + offset, width, width)


def get_index_behavior_rect(rect):
    offset = 3
    width = rect.height() - (offset * 2)
    left = rect.left() + ((rect.width() / 6) * 3)
    return QtCore.QRect(left, rect.top() + offset, width, width)


def get_index_body_rect(rect):
    return QtCore.QRect(
        rect.left() + INDEX_BODY_RIGHTLEFT_PADDING,
        rect.top(),
        rect.width() - (INDEX_BODY_RIGHTLEFT_PADDING * 2),
        rect.height())


def get_index_inplug_rect(rect):
    return QtCore.QRect(
        rect.left(), rect.top() + (rect.height() / 2) - (INDEX_PLUG_WIDTH / 2),
        INDEX_PLUG_WIDTH, INDEX_PLUG_WIDTH)


def get_index_outplug_rect(rect):
    return QtCore.QRect(
        rect.left() + rect.width() - INDEX_PLUG_WIDTH,
        rect.top() + (rect.height() / 2) - (INDEX_PLUG_WIDTH / 2),
        INDEX_PLUG_WIDTH, INDEX_PLUG_WIDTH)


def get_index_rect(row, column):
    left = ROWS_LEFT + (row * (ROWS_SPACING + ROWS_WIDTH)) + ROWS_PADDING
    top = (
        ROWS_TOP + ROWS_HEADER_SPACE +
        (column * (INDEX_HEIGHT + INDEX_SPACING)))

    return QtCore.QRect(
        left,
        top,
        INDEX_WIDTH,
        INDEX_HEIGHT)


def get_row_rect(row_number, row_len):
    left = ROWS_LEFT + ((ROWS_WIDTH + ROWS_SPACING) * row_number)
    height = (
        ROWS_HEADER_SPACE +
        ((INDEX_HEIGHT + INDEX_SPACING) * row_len) +
        ROWS_BOTTOM_SPACE)
    return QtCore.QRect(left, ROWS_TOP, ROWS_WIDTH, height)


def get_connection_path(start_point, end_point):
    path = QtGui.QPainterPath(start_point)
    control_point_1 = QtCore.QPoint(
        (
            start_point.x() +
            round((end_point.x() - start_point.x()) / 2)
        ),
        start_point.y())

    control_point_2 = QtCore.QPoint(
        (
            end_point.x() -
            round((end_point.x() - start_point.x()) / 2)
        ),
        end_point.y())
    path.cubicTo(control_point_1, control_point_2, end_point)
    return path


def get_connection_handler_rect(path):
    center = path.pointAtPercent(0.5).toPoint()
    top = center.y() - (CONNECTION_HANDLER_SIZE // 2)
    left = center.x() - (CONNECTION_HANDLER_SIZE // 2)
    return QtCore.QRect(
        left, top, CONNECTION_HANDLER_SIZE, CONNECTION_HANDLER_SIZE)


def get_note_path(
        noterect, note1=False, note2=False, note3=False, note4=False,
        note5=False):
    notes = note1, note2, note3, note4, note5
    round_rect = QtCore.QRect(
        noterect.left(),
        noterect.top() + noterect.height() - noterect.width(),
        noterect.width(),
        noterect.width())

    path = QtGui.QPainterPath(noterect.topLeft())
    centers = [
        QtCore.QPoint(
            round_rect.center().x(),
            round_rect.center().y() - (noterect.width() * i))
        for i, n in enumerate(notes) if n is True]

    for center in centers:
        path.addEllipse(
            center,
            noterect.width() / 2,
            (noterect.width() - round(noterect.width() / 3)) / 2)

    if not any(notes):
        return path

    path.moveTo(
        QtCore.QPoint(noterect.right(), noterect.top()))
    path.lineTo(
        QtCore.QPoint(
            noterect.right(),
            centers[0].y()))

    return path


def get_beam_tail_path(noterect):
    start_point = noterect.topRight()
    end_point = QtCore.QPoint(
        noterect.right() + round(((noterect.width() / 3) * 2)),
        noterect.top() + ((noterect.height() / 2)))

    control_point_1 = QtCore.QPoint(
        start_point.x(),
        start_point.y() + round((end_point.y() - start_point.y()) / 2))

    control_point_2 = QtCore.QPoint(
        start_point.x() + noterect.width() + round(noterect.width() / 2),
        end_point.y() - round((end_point.y() - start_point.y()) / 2))

    path = QtGui.QPainterPath(start_point)
    path.cubicTo(control_point_1, control_point_2, end_point)

    end_point = QtCore.QPoint(
        start_point.x(), start_point.y() + round(noterect.height() / 7))

    start_point = path.currentPosition()

    control_point_1 = QtCore.QPoint(
        start_point.x() + (noterect.width() / 2),
        start_point.y() - round((start_point.y() - end_point.y()) / 2))

    control_point_2 = QtCore.QPoint(
        end_point.x() + (noterect.width() / 10),
        end_point.y() + round((start_point.y() - end_point.y()) / 2))

    path.cubicTo(control_point_1, control_point_2, end_point)
    return path


def get_beams_connection_path(noterect1, noterect2):
    rect = QtCore.QRectF(
        noterect1.topRight(),
        QtCore.QPoint(
            noterect2.topRight().x(),
            noterect2.topRight().y() + BEAM_CONNECTION_WIDTH))
    path = QtGui.QPainterPath()
    path.addRect(rect)
    return path


def get_eighth_rest_path(noterect):
    start_point = QtCore.QPoint(
        noterect.left() - round(noterect.width() / 2),
        noterect.top() + round(noterect.height() / 3))

    path = QtGui.QPainterPath(start_point)

    control_point = QtCore.QPoint(
        start_point.x() + (noterect.width() / 5),
        start_point.y() + round(noterect.height() / 8))

    control_point_2 = QtCore.QPoint(
        start_point.x() + noterect.width(),
        start_point.y() + round(noterect.height() / 10))

    end_point = QtCore.QPoint(
        noterect.right() + round(noterect.width() / 2),
        noterect.top() + round(noterect.height() / 4))

    path.cubicTo(control_point, control_point_2, end_point)

    path.lineTo(QtCore.QPoint(
        noterect.left(), noterect.bottom() - round(noterect.height() / 3)))

    path.lineTo(QtCore.QPoint(
        start_point.x() + round(noterect.width() / 3),
        noterect.bottom() - round(noterect.height() / 3)))

    path.lineTo(end_point)

    control_point = QtCore.QPoint(
        control_point.x() + (noterect.width() / 2),
        control_point.y() + round(noterect.height() / 20))

    control_point_2 = QtCore.QPoint(
        control_point.x() - ((noterect.width() / 3) * 2),
        control_point_2.y() + round(noterect.height() / 30))

    path.cubicTo(control_point, control_point_2, start_point)

    path.addEllipse(
        QtCore.QPoint(
            start_point.x() + round(noterect.width() / 2),
            start_point.y()),
        noterect.width() / 2.1, noterect.width() / 2.1)

    return path


def get_slider_segmented_line_path(rect, segment_count=11):
    top = rect.top() + (rect.height() * .75)
    seg_top = top - SLIDER_SEGMENT_HEIGHT
    path = QtGui.QPainterPath(QtCore.QPoint(rect.left(), top))
    path.lineTo(QtCore.QPoint(rect.right(), top))
    for i in range(segment_count):
        path.lineTo(QtCore.QPoint(path.currentPosition().x(), seg_top))
        left = rect.left() + ((rect.width() / (segment_count - 1)) * i)
        path.moveTo(QtCore.QPoint(left, top))
    return path


def get_slider_handler_path(handlerrect):
    path = QtGui.QPainterPath(handlerrect.topLeft())
    path.lineTo(
        QtCore.QPoint(
            handlerrect.left(),
            handlerrect.top() + (handlerrect.height() * .4)))
    path.lineTo(
        QtCore.QPoint(
            handlerrect.left() + (handlerrect.width() / 2),
            handlerrect.top() + (handlerrect.height() * .6)))
    path.lineTo(
        QtCore.QPoint(
            handlerrect.right(),
            handlerrect.top() + (handlerrect.height() * .4)))
    path.lineTo(handlerrect.topRight())
    path.closeSubpath()
    return path


def get_slider_handler_rect(sliderrect, value, segment_count):
    width = (sliderrect.width() / segment_count) - 5
    left = (
        sliderrect.left() +
        ((sliderrect.width() / segment_count) * value) -
        (width / 2))
    return QtCore.QRect(
        left, sliderrect.top(), width, sliderrect.height())


def extract_noterects(rect, number=4):
    width = rect.height() / 6
    left_offset = (rect.width() - width) / (number - 1)

    return [
        QtCore.QRect(
            rect.left() + (width / 2) + (left_offset * i),
            rect.top(),
            width,
            rect.height())
        for i in range(number)]
