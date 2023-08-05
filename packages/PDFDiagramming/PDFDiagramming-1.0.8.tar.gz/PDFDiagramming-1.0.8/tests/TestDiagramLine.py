
from logging import Logger
from logging import getLogger
from typing import Tuple

from unittest import TestSuite
from unittest import main as unitTestMain

from pdfdiagrams.Defaults import LEFT_MARGIN
from pdfdiagrams.Defaults import TOP_MARGIN

from pdfdiagrams.Definitions import EllipseDefinition
from pdfdiagrams.Definitions import UmlLineDefinition
from pdfdiagrams.Definitions import UmlLineDefinitions
from pdfdiagrams.Definitions import LineType
from pdfdiagrams.Definitions import Position
from pdfdiagrams.Definitions import Size

from pdfdiagrams.Diagram import Diagram
from pdfdiagrams.DiagramCommon import DiagramCommon
from pdfdiagrams.DiagramLine import DiagramLine

from tests.TestBase import TestBase
from tests.TestConstants import TestConstants


class TestDiagramLine(TestBase):

    V_LEFT_X:   int = 900
    V_RIGHT_X:  int = 1050
    V_TOP_Y:    int = 294
    V_BOTTOM_Y: int = 408

    X_INC: int = 50
    X_DEC: int = 50

    TOP_LINE_LEFT_X:  int = V_LEFT_X  - X_DEC
    TOP_LINE_RIGHT_X: int = V_RIGHT_X + X_INC

    H_LEFT_X:         int = V_RIGHT_X + 300
    H_RIGHT_X:        int = H_LEFT_X  + 200
    H_LEFT_TOP_Y:     int = V_TOP_Y
    H_LEFT_BOTTOM_Y:  int = V_BOTTOM_Y
    H_RIGHT_BOTTOM_Y: int = H_LEFT_BOTTOM_Y

    Y_INC: int = 50
    DASH_LINE_SPACE_LENGTH: int = 4

    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestDiagramLine.clsLogger = getLogger(__name__)

    def setUp(self):

        self.logger: Logger = TestDiagramLine.clsLogger

    def tearDown(self):
        pass

    def testOrthogonalInheritanceLines(self):

        diagram: Diagram = Diagram(fileName=f'{TestConstants.TEST_FILE_NAME}-OrthogonalInheritanceLines{TestConstants.TEST_SUFFIX}', dpi=TestConstants.TEST_DPI)

        self.__drawHorizontalBoundaries(diagram)
        self.__drawVerticalBoundaries(diagram)

        lineDrawer: DiagramLine = DiagramLine(pdf=diagram._pdf, diagramPadding=diagram._diagramPadding, dpi=diagram._dpi)

        north, south, east, west = self.__createOrthogonalLines(LineType.Inheritance)
        lineDefinitions: UmlLineDefinitions = [
            north, south, east, west
        ]
        for lineDefinition in lineDefinitions:
            lineDrawer.draw(lineDefinition)

        diagram.write()

    def testOrthogonalCompositionLines(self):

        diagram: Diagram = Diagram(fileName=f'{TestConstants.TEST_FILE_NAME}-OrthogonalCompositionLines{TestConstants.TEST_SUFFIX}', dpi=TestConstants.TEST_DPI)

        self.__drawHorizontalBoundaries(diagram)
        self.__drawVerticalBoundaries(diagram)

        lineDrawer: DiagramLine = DiagramLine(pdf=diagram._pdf, diagramPadding=diagram._diagramPadding, dpi=diagram._dpi)

        north, south, east, west = self.__createOrthogonalLines(LineType.Composition)

        lineDefinitions: UmlLineDefinitions = [
            north, south, east, west
        ]
        for lineDefinition in lineDefinitions:
            lineDrawer.draw(lineDefinition)

        diagram.write()

    ELLIPSE_X: int = V_LEFT_X
    ELLIPSE_Y: int = V_TOP_Y

    ELLIPSE_WIDTH:  int = 200
    ELLIPSE_HEIGHT: int = 200

    ELLIPSE_FILL_STYLE: str = 'D'

    def testDiagonalInheritanceLines(self):

        diagram: Diagram = Diagram(fileName=f'{TestConstants.TEST_FILE_NAME}-DiagonalInheritanceLines{TestConstants.TEST_SUFFIX}', dpi=TestConstants.TEST_DPI)
        self.__drawEllipseForDiagonalInheritanceLines(diagram)

        lineDrawer: DiagramLine = DiagramLine(pdf=diagram._pdf, diagramPadding=diagram._diagramPadding, dpi=diagram._dpi)

        northEast, northWest, southEast, southWest = self.__createDiagonalLines(LineType.Inheritance)
        definitions: UmlLineDefinitions = [northEast, northWest, southEast, southWest]
        for definition in definitions:
            lineDrawer.draw(definition)
        diagram.write()

    def testDiagonalCompositionLines(self):
        diagram: Diagram = Diagram(fileName=f'{TestConstants.TEST_FILE_NAME}-DiagonalCompositionLines{TestConstants.TEST_SUFFIX}', dpi=TestConstants.TEST_DPI)
        self.__drawEllipseForDiagonalInheritanceLines(diagram)

        lineDrawer: DiagramLine = DiagramLine(pdf=diagram._pdf, diagramPadding=diagram._diagramPadding, dpi=diagram._dpi)

        northEast, northWest, southEast, southWest = self.__createDiagonalLines(LineType.Composition)
        definitions: UmlLineDefinitions = [northEast, northWest, southEast, southWest]
        for definition in definitions:
            lineDrawer.draw(definition)
        diagram.write()

    def testOrthogonalAggregationLines(self):
        diagram: Diagram = Diagram(fileName=f'{TestConstants.TEST_FILE_NAME}-OrthogonalAggregationLines{TestConstants.TEST_SUFFIX}', dpi=TestConstants.TEST_DPI)

        self.__drawHorizontalBoundaries(diagram)
        self.__drawVerticalBoundaries(diagram)

        lineDrawer: DiagramLine = DiagramLine(pdf=diagram._pdf, diagramPadding=diagram._diagramPadding, dpi=diagram._dpi)

        north, south, east, west = self.__createOrthogonalLines(LineType.Aggregation)
        lineDefinitions: UmlLineDefinitions = [
            north, south, east, west
        ]
        for lineDefinition in lineDefinitions:
            lineDrawer.draw(lineDefinition)

        diagram.write()

    def testDiagonalAggregationLines(self):

        diagram: Diagram = Diagram(fileName=f'{TestConstants.TEST_FILE_NAME}-DiagonalAggregationLines{TestConstants.TEST_SUFFIX}', dpi=TestConstants.TEST_DPI)
        self.__drawEllipseForDiagonalInheritanceLines(diagram)

        lineDrawer: DiagramLine = DiagramLine(pdf=diagram._pdf, diagramPadding=diagram._diagramPadding, dpi=diagram._dpi)

        northEast, northWest, southEast, southWest = self.__createDiagonalLines(LineType.Aggregation)
        definitions: UmlLineDefinitions = [northEast, northWest, southEast, southWest]
        for definition in definitions:
            lineDrawer.draw(definition)
        diagram.write()

    def __createOrthogonalLines(self, lineType: LineType) -> Tuple[UmlLineDefinition, UmlLineDefinition, UmlLineDefinition, UmlLineDefinition]:

        north: UmlLineDefinition = UmlLineDefinition(lineType=lineType,
                                                     destination=Position(TestDiagramLine.V_RIGHT_X, TestDiagramLine.V_BOTTOM_Y),
                                                     source=Position(TestDiagramLine.V_RIGHT_X, TestDiagramLine.V_TOP_Y))

        south: UmlLineDefinition = UmlLineDefinition(lineType=lineType,
                                                     source=Position(TestDiagramLine.V_LEFT_X, TestDiagramLine.V_BOTTOM_Y),
                                                     destination=Position(TestDiagramLine.V_LEFT_X, TestDiagramLine.V_TOP_Y))

        east: UmlLineDefinition = UmlLineDefinition(lineType=lineType,
                                                    source=Position(TestDiagramLine.H_LEFT_X, TestDiagramLine.H_LEFT_TOP_Y + TestDiagramLine.Y_INC),
                                                    destination=Position(TestDiagramLine.H_RIGHT_X, TestDiagramLine.H_LEFT_TOP_Y + TestDiagramLine.Y_INC))

        west: UmlLineDefinition = UmlLineDefinition(lineType=lineType,
                                                    source=Position(TestDiagramLine.H_RIGHT_X,   TestDiagramLine.H_RIGHT_BOTTOM_Y),
                                                    destination=Position(TestDiagramLine.H_LEFT_X, TestDiagramLine.H_LEFT_BOTTOM_Y)
                                                    )

        return north, south, east, west

    def __createDiagonalLines(self, lineType: LineType) -> Tuple[UmlLineDefinition, UmlLineDefinition, UmlLineDefinition, UmlLineDefinition]:

        pos:  Position          = Position(TestDiagramLine.ELLIPSE_X, TestDiagramLine.ELLIPSE_Y)

        arrowSize: float = TestDiagramLine.ELLIPSE_WIDTH / 2

        center: Position = self.__computeEllipseCenter(pos)
        neDest: Position = self.__computeNorthEastDestination(center=center, arrowSize=arrowSize)
        seDest: Position = self.__computeSouthEastDestination(center=center, arrowSize=arrowSize)
        nwDest: Position = self.__computeNorthWestDestination(center=center, arrowSize=arrowSize)
        swDest: Position = self.__computeSouthWestDestination(center=center, arrowSize=arrowSize)

        northEast: UmlLineDefinition = UmlLineDefinition(lineType=lineType, source=center, destination=neDest)
        northWest: UmlLineDefinition = UmlLineDefinition(lineType=lineType, source=center, destination=nwDest)
        southEast: UmlLineDefinition = UmlLineDefinition(lineType=lineType, source=center, destination=seDest)
        southWest: UmlLineDefinition = UmlLineDefinition(lineType=lineType, source=center, destination=swDest)

        return northEast, northWest, southEast, southWest

    def __drawHorizontalBoundaries(self, diagram: Diagram):

        x1: int = DiagramCommon.toPdfPoints(TestDiagramLine.TOP_LINE_LEFT_X,  diagram._dpi) + LEFT_MARGIN + diagram.verticalGap
        x2: int = DiagramCommon.toPdfPoints(TestDiagramLine.TOP_LINE_RIGHT_X, diagram._dpi) + LEFT_MARGIN + diagram.verticalGap
        y2: int = DiagramCommon.toPdfPoints(TestDiagramLine.V_BOTTOM_Y,       diagram._dpi) + TOP_MARGIN  + diagram.horizontalGap

        diagram._pdf.dashed_line(x1=x1, y1=y2, x2=x2, y2=y2, space_length=TestDiagramLine.DASH_LINE_SPACE_LENGTH)

        y2 = DiagramCommon.toPdfPoints(TestDiagramLine.V_TOP_Y, diagram._dpi) + TOP_MARGIN + diagram.horizontalGap

        diagram._pdf.dashed_line(x1=x1, y1=y2, x2=x2, y2=y2, space_length=TestDiagramLine.DASH_LINE_SPACE_LENGTH)

    def __drawVerticalBoundaries(self, diagram: Diagram):

        x1: int = DiagramCommon.toPdfPoints(TestDiagramLine.H_LEFT_X,  diagram._dpi) + LEFT_MARGIN + diagram.verticalGap
        x2: int = x1
        y1: int = DiagramCommon.toPdfPoints(TestDiagramLine.H_LEFT_TOP_Y,    diagram._dpi) + TOP_MARGIN + diagram.horizontalGap
        y2: int = DiagramCommon.toPdfPoints(TestDiagramLine.H_LEFT_BOTTOM_Y, diagram._dpi) + TOP_MARGIN + diagram.horizontalGap

        diagram._pdf.dashed_line(x1=x1, y1=y1, x2=x2, y2=y2, space_length=TestDiagramLine.DASH_LINE_SPACE_LENGTH)

        x1 = DiagramCommon.toPdfPoints(TestDiagramLine.H_RIGHT_X,  diagram._dpi) + LEFT_MARGIN + diagram.verticalGap
        x2 = x1

        diagram._pdf.dashed_line(x1=x1, y1=y1, x2=x2, y2=y2, space_length=TestDiagramLine.DASH_LINE_SPACE_LENGTH)

    def __drawEllipseForDiagonalInheritanceLines(self, diagram: Diagram):

        eDef: EllipseDefinition = EllipseDefinition()
        pos:  Position          = Position(TestDiagramLine.ELLIPSE_X, TestDiagramLine.ELLIPSE_Y)
        size: Size              = Size(width=TestDiagramLine.ELLIPSE_WIDTH, height=TestDiagramLine.ELLIPSE_HEIGHT)

        eDef.position = pos
        eDef.size     = size
        diagram.drawEllipse(eDef)
        diagram.drawRectangle(eDef)

        center: Position = self.__computeEllipseCenter(pos)

        diagram.drawText(center, text=f'({int(center.x)},{int(center.y)})')

    def __computeEllipseCenter(self, ellipsePos: Position) -> Position:

        x: float = ellipsePos.x
        y: float = ellipsePos.y

        centerX: float = x + (TestDiagramLine.ELLIPSE_WIDTH / 2)
        centerY: float = y + (TestDiagramLine.ELLIPSE_HEIGHT / 2)

        return Position(centerX, centerY)

    def __computeNorthEastDestination(self, center: Position, arrowSize: float) -> Position:
        from math import pi

        radians: float = (pi / 4) * -1.0    # definition of 45 degree angle
        return self.__computeDestination(center=center, arrowSize=arrowSize, radians=radians)

    def __computeSouthEastDestination(self, center: Position, arrowSize: float) -> Position:
        from math import pi

        radians: float = pi / 4
        return self.__computeDestination(center=center, arrowSize=arrowSize, radians=radians)

    def __computeNorthWestDestination(self, center: Position, arrowSize: float) -> Position:
        from math import pi

        radians: float = (pi * 0.75) * -1.0
        return self.__computeDestination(center=center, arrowSize=arrowSize, radians=radians)

    def __computeSouthWestDestination(self, center: Position, arrowSize: float) -> Position:
        from math import pi

        radians: float = pi * 0.75
        return self.__computeDestination(center=center, arrowSize=arrowSize, radians=radians)

    def __computeDestination(self, center: Position, arrowSize: float, radians: float,) -> Position:

        from math import cos
        from math import sin

        return Position(center.x + arrowSize * cos(radians), center.y + arrowSize * sin(radians))


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestDiagramLine))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
