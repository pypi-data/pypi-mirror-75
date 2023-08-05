
from logging import Logger
from logging import getLogger
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from pdfdiagrams.Definitions import ClassDefinition
from pdfdiagrams.Definitions import ClassDefinitions
from pdfdiagrams.Definitions import DefinitionType
from pdfdiagrams.Definitions import UmlLineDefinition
from pdfdiagrams.Definitions import UmlLineDefinitions
from pdfdiagrams.Definitions import LineType
from pdfdiagrams.Definitions import MethodDefinition
from pdfdiagrams.Definitions import ParameterDefinition
from pdfdiagrams.Definitions import Position
from pdfdiagrams.Definitions import Size

from pdfdiagrams.Diagram import Diagram

from tests.TestBase import TestBase

from tests.TestConstants import TestConstants


class TestDiagram(TestBase):
    """
    The following all test with the default horizontal/vertical gaps and the default top/left margins
    """

    BASE_TEST_CLASS_NAME: str = 'TestClassName'

    TEST_LAST_X_POSITION: int = 9
    TEST_LAST_Y_POSITION: int = 6

    CELL_WIDTH:  int = 150  # points
    CELL_HEIGHT: int = 100  # points

    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestDiagram.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestDiagram.clsLogger

    def tearDown(self):
        pass

    def testConstruction(self):

        diagram: Diagram = Diagram(fileName=TestConstants.TEST_FILE_NAME, dpi=TestConstants.TEST_DPI)
        self.assertIsNotNone(diagram, 'Construction failed')

        self.assertEqual(Diagram.DEFAULT_FONT_SIZE, diagram.fontSize, 'Default font size changed')

    def testBasicDiagramDraw(self):

        diagram: Diagram = Diagram(fileName=f'{TestConstants.TEST_FILE_NAME}-Basic{TestConstants.TEST_SUFFIX}', dpi=TestConstants.TEST_DPI)
        classDef: ClassDefinition = ClassDefinition(name=TestDiagram.BASE_TEST_CLASS_NAME,
                                                    size=Size(width=TestDiagram.CELL_WIDTH, height=TestDiagram.CELL_HEIGHT))

        diagram.drawClass(classDef)
        diagram.write()

    def testFillPage(self):

        diagram: Diagram = Diagram(fileName=f'{TestConstants.TEST_FILE_NAME}-Full{TestConstants.TEST_SUFFIX}', dpi=TestConstants.TEST_DPI)

        widthInterval:  int = TestDiagram.CELL_WIDTH // 10
        heightInterval: int = TestDiagram.CELL_HEIGHT // 10

        for x in range(0, TestDiagram.TEST_LAST_X_POSITION):
            scrX: int = (x * TestDiagram.CELL_WIDTH) + (widthInterval * x)

            for y in range(0, TestDiagram.TEST_LAST_Y_POSITION):

                scrY: int = (y * TestDiagram.CELL_HEIGHT) + (y * heightInterval)
                classDef: ClassDefinition = ClassDefinition(name=f'{TestDiagram.BASE_TEST_CLASS_NAME}{x}{y}',
                                                            position=Position(scrX, scrY),
                                                            size=Size(width=TestDiagram.CELL_WIDTH, height=TestDiagram.CELL_HEIGHT))
                diagram.drawClass(classDef)

        diagram.write()

    def testBasicMethods(self):

        diagram: Diagram = Diagram(fileName=f'{TestConstants.TEST_FILE_NAME}-BasicMethods{TestConstants.TEST_SUFFIX}', dpi=TestConstants.TEST_DPI)

        classDef: ClassDefinition = self.__buildCar()

        diagram.drawClass(classDef)

        diagram.write()

    def testBasicHeader(self):

        diagram: Diagram = Diagram(fileName=f'{TestConstants.TEST_FILE_NAME}-BasicHeader{TestConstants.TEST_SUFFIX}',
                                   dpi=TestConstants.TEST_DPI,
                                   headerText='Unit Test Header')
        classDef: ClassDefinition = self.__buildCar()

        diagram.drawClass(classDef)

        diagram.write()

    def testSophisticatedHeader(self):
        from time import gmtime
        from time import strftime

        today = strftime("%d %b %Y %H:%M:%S", gmtime())

        diagram: Diagram = Diagram(fileName=f'{TestConstants.TEST_FILE_NAME}-SophisticatedHeader{TestConstants.TEST_SUFFIX}',
                                   dpi=TestConstants.TEST_DPI,
                                   headerText=f'Pyut Export Version 6.0 - {today}')
        classDef: ClassDefinition = self.__buildCar()

        diagram.drawClass(classDef)

        diagram.write()

    def testSophisticatedLayout(self):

        diagram: Diagram = Diagram(fileName=f'{TestConstants.TEST_FILE_NAME}-SophisticatedLayout{TestConstants.TEST_SUFFIX}', dpi=TestConstants.TEST_DPI)

        classDefinitions: ClassDefinitions = [
            self.__buildCar(),
            self.__buildCat(),
            self.__buildOpie(),
            self.__buildNameTestCase(),
            self.__buildElectricCar()
        ]
        for classDefinition in classDefinitions:
            classDefinition = cast(ClassDefinition, classDefinition)
            diagram.drawClass(classDefinition=classDefinition)

        lineDefinitions: UmlLineDefinitions = self.__buildSophisticatedLineDefinitions()
        for lineDefinition in lineDefinitions:
            diagram.drawUmlLine(lineDefinition=lineDefinition)

        diagram.write()

    def testBuildMethod(self):

        diagram: Diagram = Diagram(fileName=cast(str, None), dpi=cast(int, None))

        initMethodDef: MethodDefinition = self.__buildInitMethod()

        actualRepr:    str = diagram._buildMethod(initMethodDef)
        expectedRepr:  str = '+ __init__(make: str, model: str, year: int=1957)'

        self.assertEqual(expectedRepr, actualRepr, 'Method building is incorrect')

    def testBuildMethods(self):

        diagram: Diagram = Diagram(fileName=cast(str, None), dpi=cast(int, None))

        car: ClassDefinition = self.__buildCar()

        reprs: Diagram.MethodsRepr = diagram._buildMethods(car.methods)

        self.assertEqual(5, len(reprs), 'Generated incorrect number of method representations')

    def testBasicMethod(self):

        # diagram: Diagram = Diagram(fileName=f'{TestConstants.TEST_FILE_NAME}-BasicMethod{TestConstants.TEST_SUFFIX}', dpi=TestConstants.TEST_DPI)
        diagram: Diagram = Diagram(fileName=f'Test-BasicMethod.pdf', dpi=75)

        position: Position = Position(107, 30)
        size:     Size     = Size(width=266, height=100)

        car: ClassDefinition = ClassDefinition(name='Car', position=position, size=size)

        initMethodDef: MethodDefinition = MethodDefinition(name='__init__', visibility=DefinitionType.Public)

        initParam: ParameterDefinition = ParameterDefinition(name='make', parameterType='str', defaultValue='')
        initMethodDef.parameters = [initParam]
        car.methods = [initMethodDef]

        diagram.drawClass(car)

        diagram.write()

    def testMinimalInheritance(self):

        diagram: Diagram = Diagram(fileName='MinimalInheritance.pdf', dpi=75)

        cat:  ClassDefinition = ClassDefinition(name='Gato', position=Position(536, 19), size=Size(height=74, width=113))
        opie: ClassDefinition = ClassDefinition(name='Opie', position=Position(495, 208), size=Size(width=216, height=87))

        diagram.drawClass(classDefinition=cat)
        diagram.drawClass(classDefinition=opie)

        opieToCat: UmlLineDefinition = UmlLineDefinition(lineType=LineType.Inheritance, source=Position(600, 208), destination=Position(600, 93))

        diagram.drawUmlLine(lineDefinition=opieToCat)
        diagram.write()

    def __buildCar(self) -> ClassDefinition:

        car: ClassDefinition = ClassDefinition(name='Car', position=Position(107, 30), size=Size(width=266, height=100))

        initMethodDef:      MethodDefinition = self.__buildInitMethod()
        descMethodDef:      MethodDefinition = MethodDefinition(name='getDescriptiveName', visibility=DefinitionType.Public)
        odometerMethodDef:  MethodDefinition = MethodDefinition(name='readOdometer',      visibility=DefinitionType.Public)
        updateOdoMethodDef: MethodDefinition = MethodDefinition(name='updateOdometer',    visibility=DefinitionType.Public)
        incrementMethodDef: MethodDefinition = MethodDefinition(name='incrementOdometer', visibility=DefinitionType.Protected)

        mileageParam: ParameterDefinition = ParameterDefinition(name='mileage', defaultValue='1')
        updateOdoMethodDef.parameters = [mileageParam]

        milesParam: ParameterDefinition = ParameterDefinition(name='miles', parameterType='int')
        incrementMethodDef.parameters = [milesParam]

        car.methods = [initMethodDef, descMethodDef, odometerMethodDef, updateOdoMethodDef, incrementMethodDef]

        return car

    def __buildCat(self) -> ClassDefinition:

        cat: ClassDefinition = ClassDefinition(name='gato', position=Position(536, 19), size=Size(height=74, width=113))

        initMethod:     MethodDefinition = MethodDefinition('__init')
        sitMethod:      MethodDefinition = MethodDefinition('sit')
        rollOverMethod: MethodDefinition = MethodDefinition('rollOver')

        cat.methods = [initMethod, sitMethod, rollOverMethod]

        return cat

    def __buildOpie(self) -> ClassDefinition:

        opie: ClassDefinition = ClassDefinition(name='Opie', position=Position(495, 208), size=Size(width=216, height=87))

        publicMethod: MethodDefinition = MethodDefinition(name='publicMethod', visibility=DefinitionType.Public, returnType='bool')
        paramDef: ParameterDefinition  = ParameterDefinition(name='param', parameterType='float', defaultValue='23.0')

        publicMethod.parameters = [paramDef]

        opie.methods = [publicMethod]

        return opie

    def __buildElectricCar(self) -> ClassDefinition:

        electricCar: ClassDefinition = ClassDefinition(name='ElectricCar', position=Position(52, 224), size=Size(width=173, height=64))

        initMethod: MethodDefinition = MethodDefinition(name='__init__')
        descMethod: MethodDefinition = MethodDefinition(name='describeBattery')

        makeParameter:  ParameterDefinition = ParameterDefinition(name='make')
        modelParameter: ParameterDefinition = ParameterDefinition(name='model')
        yearParameter:  ParameterDefinition = ParameterDefinition(name='year')

        initMethod.parameters = [makeParameter, modelParameter, yearParameter]
        electricCar.methods = [initMethod, descMethod]
        return electricCar

    def __buildNameTestCase(self) -> ClassDefinition:

        namesTest: ClassDefinition = ClassDefinition(name='NamesTestCase', position=Position(409, 362), size=Size(height=65, width=184))

        testFirst:    MethodDefinition = MethodDefinition(name='testFirstLasName')
        formattedName: MethodDefinition = MethodDefinition(name='getFormattedName')

        firstParam:  ParameterDefinition = ParameterDefinition(name='first')
        lastParam:  ParameterDefinition = ParameterDefinition(name='last')

        formattedName.parameters = [firstParam, lastParam]
        namesTest.methods = [testFirst, formattedName]

        return namesTest

    def __buildInitMethod(self) -> MethodDefinition:

        initMethodDef:  MethodDefinition    = MethodDefinition(name='__init__', visibility=DefinitionType.Public)

        initParam:  ParameterDefinition = ParameterDefinition(name='make',  parameterType='str', defaultValue='')
        modelParam: ParameterDefinition = ParameterDefinition(name='model', parameterType='str', defaultValue='')
        yearParam:  ParameterDefinition = ParameterDefinition(name='year',  parameterType='int', defaultValue='1957')

        initMethodDef.parameters = [initParam, modelParam, yearParam]

        return initMethodDef

    V_LEFT_X:   int = 1100
    V_RIGHT_X:  int = 1250
    V_TOP_Y:    int = 394
    V_BOTTOM_Y: int = 508

    def __buildSophisticatedLineDefinitions(self) -> UmlLineDefinitions:

        opieToCat: UmlLineDefinition = UmlLineDefinition(lineType=LineType.Inheritance, source=Position(600, 208), destination=Position(600, 93))
        eCarToCar: UmlLineDefinition = UmlLineDefinition(lineType=LineType.Inheritance, source=Position(190, 224), destination=Position(190, 129))
        lineDefinitions: UmlLineDefinitions = [
            opieToCat, eCarToCar
        ]

        return lineDefinitions


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestDiagram))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
