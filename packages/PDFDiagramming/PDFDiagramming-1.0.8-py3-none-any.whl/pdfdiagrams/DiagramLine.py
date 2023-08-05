
from typing import final

from logging import Logger
from logging import getLogger

from math import pi
from math import sin
from math import atan
from math import cos
from typing import Tuple

from fpdf import FPDF

from pdfdiagrams.Internal import ArrowPoints
from pdfdiagrams.Internal import DiamondPoints
from pdfdiagrams.Internal import PolygonPoints
from pdfdiagrams.Internal import PdfPosition

from pdfdiagrams.Definitions import DiagramPadding
from pdfdiagrams.Definitions import UmlLineDefinition
from pdfdiagrams.Definitions import LineType
from pdfdiagrams.Definitions import Position

from pdfdiagrams.DiagramCommon import DiagramCommon
from pdfdiagrams.Internal import ScanPoints

from pdfdiagrams.UnsupportedException import UnsupportedException


class DiagramLine:
    """
    This class takes responsibility for drawing the various types of lines within the
    described UML classes.  End users generally do not directly use this class.
    It is split off as part of the separation of responsibility principle.
    """
    INHERITANCE_ARROW_HEIGHT: final = 10
    DIAMOND_HEIGHT:           final = 8

    def __init__(self, pdf: FPDF, diagramPadding: DiagramPadding, dpi: int):

        self.logger: Logger = getLogger(__name__)

        self._pdf: FPDF = pdf
        self._dpi: int  = dpi

        self._diagramPadding: diagramPadding  = diagramPadding

    def draw(self, lineDefinition: UmlLineDefinition):
        """
        Draw the line described by the input parameter
        Args:
            lineDefinition:  Describes the line to draw
        """

        source:      Position = lineDefinition.source
        destination: Position = lineDefinition.destination
        lineType:    LineType = lineDefinition.lineType

        if lineType == LineType.Inheritance:
            self._drawInheritanceArrow(src=source, dest=destination)
        elif lineType == LineType.Composition:
            self._drawCompositionSolidDiamond(src=source, dest=destination)
        elif lineType == LineType.Aggregation:
            self._drawAggregationDiamond(src=source, dest=destination)
        else:
            raise UnsupportedException(f'Line definition type not supported: `{lineType}`')

    def _drawInheritanceArrow(self, src: Position, dest: Position):
        """
        Must account for the margins and gaps between drawn shapes
        Must convert to points from screen coordinates
        Draw the arrow first
        Compute the mid point of the bottom line of the arrow
        That is where the line ends

        Args:
            src: start of line
            dest: end line line;  Arrow positioned here
        """
        convertedSrc, convertedDest = self.__convertEndPoints(src, dest)

        points: ArrowPoints = self.__computeTheArrowVertices(convertedSrc, convertedDest)
        self.__drawPolygon(points)

        newEndPoint: PdfPosition = self.__computeMidPointOfBottomLine(points[0], points[2])

        self._pdf.line(x1=convertedSrc.x, y1=convertedSrc.y, x2=newEndPoint.x, y2=newEndPoint.y)

    def _drawCompositionSolidDiamond(self, src: Position, dest: Position):

        convertedSrc, convertedDest = self.__convertEndPoints(src, dest)
        points: DiamondPoints = self.__computeDiamondVertices(convertedSrc, convertedDest)

        self.__drawPolygon(points)
        self.__FillInDiamond(points)

        newEndPoint: PdfPosition = points[3]
        self._pdf.line(x1=convertedSrc.x, y1=convertedSrc.y, x2=newEndPoint.x, y2=newEndPoint.y)

    def _drawAggregationDiamond(self, src: Position, dest: Position):

        convertedSrc, convertedDest = self.__convertEndPoints(src, dest)
        points: ArrowPoints = self.__computeDiamondVertices(convertedSrc, convertedDest)
        self.__drawPolygon(points)

        newEndPoint: PdfPosition = points[3]

        self._pdf.line(x1=convertedSrc.x, y1=convertedSrc.y, x2=newEndPoint.x, y2=newEndPoint.y)

    def __convertEndPoints(self, src: Position, dest: Position) -> Tuple[PdfPosition, PdfPosition]:

        verticalGap:   int = self._diagramPadding.verticalGap
        horizontalGap: int = self._diagramPadding.horizontalGap

        x1, y1 = DiagramCommon.convertPosition(pos=src,  dpi=self._dpi, verticalGap=verticalGap, horizontalGap=horizontalGap)
        x2, y2 = DiagramCommon.convertPosition(pos=dest, dpi=self._dpi, verticalGap=verticalGap, horizontalGap=horizontalGap)

        convertedSrc:  PdfPosition = PdfPosition(x1, y1)
        convertedDest: PdfPosition = PdfPosition(x2, y2)

        return convertedSrc, convertedDest

    def __computeTheArrowVertices(self, src: PdfPosition, dest: PdfPosition)  -> ArrowPoints:
        """
        Draw an arrow at the end of the line source-dest.

        Args:
            src:  points of the segment
            dest:  points of the segment

        Returns:
            A list of positions that describes a diamond to draw
        """
        # x1: float = src.x
        # y1: float = src.y
        # x2: float = dest.x
        # y2: float = dest.y
        #
        # deltaX: float = x2 - x1
        # deltaY: float = y2 - y1
        deltaX, deltaY = self.__computeDeltaXDeltaY(src, dest)
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

        pi_6: float = pi/6      # radians for 30 degree angle

        alpha1: float = alpha + pi_6
        alpha2: float = alpha - pi_6
        size:   float = DiagramLine.INHERITANCE_ARROW_HEIGHT
        x2: float = dest.x
        y2: float = dest.y
        #
        # The names for the left and right points are correct for upward facing arrows
        # They are inverted for downward facing arrows
        #
        arrowTip:   PdfPosition = PdfPosition(x2, y2)
        rightPoint: PdfPosition = PdfPosition(x2 + size * cos(alpha1), y2 + size * sin(alpha1))
        leftPoint:  PdfPosition = PdfPosition(x2 + size * cos(alpha2), y2 + size * sin(alpha2))

        points: ArrowPoints = [rightPoint, arrowTip, leftPoint]

        return points

    def __computeDiamondVertices(self, src: PdfPosition, dest: PdfPosition) -> DiamondPoints:
        """
        Args:
            src:
            dest:
        """
        pi_6: float = pi/6     # radians for 30 degree angle
        x2:   float = dest.x
        y2:   float = dest.y

        deltaX, deltaY = self.__computeDeltaXDeltaY(src, dest)

        if abs(deltaX) < 0.01:  # vertical segment
            if deltaY > 0:
                alpha = -pi/2
            else:
                alpha = pi/2
        else:
            if deltaX == 0:
                if deltaY > 0:
                    alpha = pi/2
                else:
                    alpha = 3 * pi / 2
            else:
                alpha = atan(deltaY/deltaX)
        if deltaX > 0:
            alpha += pi

        alpha1: float = alpha + pi_6
        alpha2: float = alpha - pi_6
        size:   int   = DiagramLine.DIAMOND_HEIGHT

        # noinspection PyListCreation
        points: DiamondPoints = []

        points.append((PdfPosition(x2 + size * cos(alpha1), y2 + size * sin(alpha1))))
        points.append(PdfPosition(x2, y2))
        points.append(PdfPosition(x2 + size * cos(alpha2), y2 + size * sin(alpha2)))
        points.append(PdfPosition(x2 + 2 * size * cos(alpha), y2 + 2 * size * sin(alpha)))

        return points

    def __drawPolygon(self, points: PolygonPoints):

        pdf: FPDF = self._pdf
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

    def __computeMidPointOfBottomLine(self, startPos: PdfPosition, endPos: PdfPosition) -> PdfPosition:
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

    def __computeDeltaXDeltaY(self, src: PdfPosition, dest: PdfPosition) -> Tuple[float, float]:

        x1: float = src.x
        y1: float = src.y
        x2: float = dest.x
        y2: float = dest.y

        deltaX: float = x2 - x1
        deltaY: float = y2 - y1

        return deltaX, deltaY

    def __FillInDiamond(self, points: DiamondPoints):
        """

        Args:
            points:  The polygon that defines the composition diamond

        """
        scanPoints: ScanPoints = DiagramCommon.buildScanPoints(points)

        startX: float = scanPoints.startScan.x
        startY: float = scanPoints.startScan.y

        endX: float = scanPoints.endScan.x
        endY: float = scanPoints.endScan.y

        x = startX
        while x <= endX:
            y = startY
            while y <= endY:
                if DiagramCommon.pointInsidePolygon(pos=PdfPosition(x, y), polygon=points):
                    self._pdf.line(x1=x, y1=y, x2=x, y2=y)
                y += 1
            x += 1
