
from typing import List

from fpdf import FPDF

from pdfdiagrams.Internal import ArrowPoints
from pdfdiagrams.Internal import PdfPosition

from pdfdiagrams.Definitions import Position


def doHelloWorld():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Hello World!')
    pdf.output('tutorial1.pdf', 'F')


def drawLines():
    pdf = FPDF()
    pdf.add_page()
    pdf.line(10, 10, 10, 100)
    pdf.set_line_width(1)
    pdf.set_draw_color(255, 0, 0)
    pdf.line(20, 20, 100, 20)
    pdf.output('drawLines.pdf')


def drawShapes():
    pdf = FPDF(orientation='L', unit='pt', format=(1000, 2000))

    pdf.set_left_margin(10.0)

    pdf.add_page()

    pdf.set_fill_color(255, 0, 0)
    pdf.set_display_mode(zoom='fullwidth', layout='single')

    pdf.set_line_width(0.5)
    pdf.set_fill_color(0, 255, 0)
    pdf.set_creator('Humberto A. Sanchez II - The Great')
    pdf.set_subject('UML Diagram')

    pdf.add_font(family='Mono', fname='MonoFonto.ttf', uni=True)
    pdf.add_font(family='FuturistFixed', fname='FuturistFixedWidth.ttf', uni=True)
    pdf.add_font(family='Vera', fname='Vera.ttf', uni=True)

    pdf.set_font("Mono", size=10)
    pdf.rect(40, 40, 100, 50)
    pdf.text(x=45, y=50, txt='Mono Text')

    pdf.set_font("FuturistFixed", size=10)
    pdf.rect(x=220, y=40, w=100, h=50, style='D')
    pdf.text(x=225, y=50, txt='FFixed')

    pdf.set_font("Vera", size=10)
    pdf.rect(40, 140, 100, 50, 'D')
    pdf.text(x=45, y=150, txt='Vera Text')

    pdf.set_font("Vera", size=8)

    for y in range(0, 610, 10):
        pdf.text(x=0, y=y, txt=str(y))

    for x in range(0, 990, 10):
        pdf.dashed_line(x1=x, y1=0, x2=x, y2=8)

    pdf.output('drawShapes.pdf')


def drawTriangle():
    pdf = FPDF(orientation='L', unit='pt', format='A4')

    pdf.set_left_margin(10.0)

    pdf.add_page()

    pdf.set_fill_color(255, 0, 0)
    pdf.set_display_mode(zoom='fullwidth', layout='single')

    pdf.set_line_width(0.5)
    pdf.set_fill_color(0, 255, 0)

    x:       int = 200
    y:       int = 205
    xLeft:   int = x - 5
    xRight:  int = x + 5
    yBottom: int = y + 6

    pdf.line(x1=x, y1=y, x2=xLeft,  y2=yBottom)
    pdf.line(x1=x, y1=y, x2=xRight, y2=yBottom)
    pdf.line(x1=xLeft, y1=yBottom, x2=xRight, y2=yBottom)

    pdf.output('drawTriangle.pdf')


ARROW_SIZE: float = 8.0     # in points


def getArrowPoints(src: Position, dest: Position)  -> ArrowPoints:
    """
    Draw an arrow at the end of the line source-dest.

    Args:
        src:  points of the segment
        dest:  points of the segment

    Returns:
        A list of positions that describes a diamond to draw
    """
    from math import pi, atan, cos, sin

    x1: float = src.x
    y1: float = src.y
    x2: float = dest.x
    y2: float = dest.y

    deltaX: float = x2 - x1
    deltaY: float = y2 - y1
    if abs(deltaX) < 0.01:   # vertical segment
        if deltaY > 0:
            alpha = -pi/2
        else:
            alpha = pi/2
    else:
        if deltaX == 0:
            alpha = pi/2
        else:
            alpha = atan(deltaY/deltaX)
    if deltaX > 0:
        alpha += pi

    pi_6: float = pi/6

    alpha1: float = alpha + pi_6
    alpha2: float = alpha - pi_6
    size:   float = ARROW_SIZE

    # noinspection PyListCreation
    points: ArrowPoints = []

    points.append(PdfPosition(x2 + size * cos(alpha1), y2 + size * sin(alpha1)))
    points.append(PdfPosition(x2, y2))
    points.append(PdfPosition(x2 + size * cos(alpha2), y2 + size * sin(alpha2)))

    return points


def getFPDF():

    pdf = FPDF(orientation='L', unit='pt', format='A4')

    pdf.set_left_margin(10.0)

    pdf.add_page()

    pdf.set_fill_color(255, 0, 0)
    pdf.set_display_mode(zoom='fullwidth', layout='single')

    pdf.set_line_width(0.5)
    pdf.set_fill_color(0, 255, 0)

    return pdf


def drawPolygon(pdf: FPDF, points: ArrowPoints):

    ptNumber: int = 0
    for point in points:

        x1: float = point.x
        y1: float = point.y

        if ptNumber == len(points) - 1:
            nextPoint = points[0]
            x2: float = nextPoint.x
            y2: float = nextPoint.y
            pdf.line(x1, y1, x2, y2)
            break
        else:
            nextPoint = points[ptNumber + 1]
            x2: float = nextPoint.x
            y2: float = nextPoint.y
            pdf.line(x1, y1, x2, y2)
        ptNumber += 1


def getBottomLineMidPoint(startPos: PdfPosition, endPos: PdfPosition):
    """
    These two coordinates are the two end-points of the bottom leg of the inheritance arrow
    midPoint = (x1+x2/2, y1+y2/2)

    Args:
        startPos: start of line
        endPos:   end of line

    Returns:  Midpoint between startPos - endPos

    """
    x1: float = startPos.x
    y1: float = startPos.y
    x2: float = endPos.x
    y2: float = endPos.y

    midX: float = (x1 + x2) / 2
    midY: float = (y1 + y2) / 2

    return PdfPosition(midX, midY)


def drawInheritanceArrow(pdf: FPDF, src: Position, dest: Position):

    x1: float = src.x
    y1: float = src.y
    # x2: float = dest.x
    # y2: float = dest.y

    points = getArrowPoints(src, dest)
    drawPolygon(pdf, points)

    newEndPoint: PdfPosition = getBottomLineMidPoint(points[0], points[2])

    pdf.line(x1=x1, y1=y1, x2=newEndPoint.x,  y2=newEndPoint.y)


def drawArrows():

    LINE_LENGTH: float = 100

    CENTER_X: float = 400.0
    CENTER_Y: float = 200.0
    pdf: FPDF = getFPDF()

    src:  Position = Position(CENTER_X, CENTER_Y)

    north: Position = Position(CENTER_X, CENTER_Y - LINE_LENGTH)
    south: Position = Position(CENTER_X, CENTER_Y + LINE_LENGTH)

    east:  Position = Position(CENTER_X + LINE_LENGTH, CENTER_Y)
    west:  Position = Position(CENTER_X - LINE_LENGTH, CENTER_Y)

    northEast: Position = Position(CENTER_X + LINE_LENGTH, CENTER_Y-LINE_LENGTH)
    southEast: Position = Position(CENTER_X + LINE_LENGTH, CENTER_Y+LINE_LENGTH)

    northWest: Position = Position(CENTER_X - LINE_LENGTH, CENTER_Y-LINE_LENGTH)
    southWest: Position = Position(CENTER_X - LINE_LENGTH, CENTER_Y+LINE_LENGTH)
    destPositions: List[Position] = [
        north, east, south, west,
        northEast, southEast, northWest, southWest
    ]

    for destPos in destPositions:
        drawInheritanceArrow(pdf=pdf, src=src, dest=destPos)

    pdf.output('drawArrows.pdf')


def drawPoints():

    pdf = FPDF(orientation='L', unit='pt', format='A4')

    pdf.set_left_margin(10.0)

    pdf.add_page()

    pdf.set_fill_color(255, 0, 0)
    pdf.set_display_mode(zoom='fullwidth', layout='single')

    pdf.set_line_width(0.5)
    pdf.set_fill_color(0, 255, 0)

    startX: int = 200
    lastX:  int = 400
    incX:   int = 2
    y:      int = 205

    for x in range(startX, lastX, incX):
        pdf.line(x1=x, y1=y, x2=x, y2=y)

    pdf.output('drawPoints.pdf')


if __name__ == '__main__':
    drawPoints()
