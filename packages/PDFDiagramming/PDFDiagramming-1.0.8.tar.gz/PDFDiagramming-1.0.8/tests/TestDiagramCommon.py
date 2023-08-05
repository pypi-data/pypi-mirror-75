
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pdfdiagrams.Internal import PdfPosition
from pdfdiagrams.Internal import PolygonPoints
from pdfdiagrams.Internal import ScanPoints
from tests.TestBase import TestBase

from pdfdiagrams.DiagramCommon import DiagramCommon


class TestDiagramCommon(TestBase):
    """

        1114,469.071  **************  1122.0, 469.07171
                       *          *
                        *        *
                         *      *
                          *    *
                           *  *
                            *
                        1118, 476


                        1118,460
                             *
                           *  *
                          *    *
                         *      *
                        *        *
                       *          *
        1114,469.071  *            *   1122.0, 469.07171
                       *          *
                        *        *
                         *      *
                          *    *
                           *  *
                            *
                        1118.0, 476.0

    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestDiagramCommon.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestDiagramCommon.clsLogger
        self.diamond: PolygonPoints = [
            PdfPosition(1118.0, 460.0),
            PdfPosition(1122.0, 469.0717),
            PdfPosition(1114.0, 469.0717),
            PdfPosition(1118.0, 476.0)
        ]
        self.arrow: PolygonPoints = [
            PdfPosition(1122.0, 469.0717),
            PdfPosition(1118.0, 476.0),
            PdfPosition(1114.0, 469.0717)
        ]

    def tearDown(self):
        pass

    def testPointLeftOfDiamond(self):

        notInPolygon: PdfPosition = PdfPosition(0.0, 0.0)
        actualAns:    bool = DiagramCommon.pointInsidePolygon(pos=notInPolygon, polygon=self.diamond)

        self.assertFalse(actualAns, 'Diamond check is bad')

    def testInCenterOfDiamond(self):

        inPolygon: PdfPosition = PdfPosition(1118.0, 470.0)
        actualAns: bool = DiagramCommon.pointInsidePolygon(pos=inPolygon, polygon=self.diamond)

        self.assertTrue(actualAns, 'Diamond check in center of diamond is bad')

    def testPointRightOfDiamond(self):

        notInPolygon: PdfPosition = PdfPosition(1122.0, 490.0)
        actualAns:    bool = DiagramCommon.pointInsidePolygon(pos=notInPolygon, polygon=self.diamond)

        self.assertFalse(actualAns, 'Diamond check is bad')

    def testPointLeftOfArrow(self):

        notInPolygon: PdfPosition = PdfPosition(0.0, 0.0)
        actualAns:    bool = DiagramCommon.pointInsidePolygon(pos=notInPolygon, polygon=self.arrow)

        self.assertFalse(actualAns, 'Arrow check is bad')

    def testInCenterOfArrow(self):

        inPolygon: PdfPosition = PdfPosition(1118.0, 472.0)
        actualAns: bool = DiagramCommon.pointInsidePolygon(pos=inPolygon, polygon=self.arrow)

        self.assertTrue(actualAns, 'Diamond check is bad')

    def testPointRightOfArrow(self):

        notInPolygon: PdfPosition = PdfPosition(1122.0, 490.0)
        actualAns:    bool = DiagramCommon.pointInsidePolygon(pos=notInPolygon, polygon=self.arrow)

        self.assertFalse(actualAns, 'Diamond check is bad')

    def testBuildScanPointsForArrow(self):

        scanPoints: ScanPoints = DiagramCommon.buildScanPoints(points=self.arrow)

        self.assertEqual(1114.0, scanPoints.startScan.x, 'Minimum X not correct for arrow')
        self.assertEqual(469.0717,  scanPoints.startScan.y, 'Minimum Y not correct for arrow')

        self.assertEqual(1122.0, scanPoints.endScan.x, 'Max x is not correct for arrow')
        self.assertEqual(476.0, scanPoints.endScan.y, 'Max y is not correct for arrow')

    def testBuildScanPointsForDiamond(self):

        scanPoints: ScanPoints = DiagramCommon.buildScanPoints(points=self.diamond)

        self.assertEqual(1114.0, scanPoints.startScan.x, 'Minimum X not correct for diamond')
        self.assertEqual(460.0, scanPoints.startScan.y, 'Minimum Y not correct for diamond')

        self.assertEqual(1122.0, scanPoints.endScan.x, 'Max x is not correct for diamond')
        self.assertEqual(476.0, scanPoints.endScan.y, 'Max y is not correct for diamond')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestDiagramCommon))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
