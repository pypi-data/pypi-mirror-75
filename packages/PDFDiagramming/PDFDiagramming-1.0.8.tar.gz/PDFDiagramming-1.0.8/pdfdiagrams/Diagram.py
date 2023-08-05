
from typing import List
from typing import Tuple
from typing import cast
from typing import final

from logging import Logger
from logging import getLogger

from os import sep as osSep

from pkg_resources import resource_filename

from pdfdiagrams.Definitions import ClassDefinition
from pdfdiagrams.Definitions import DiagramPadding
from pdfdiagrams.Definitions import EllipseDefinition
from pdfdiagrams.Definitions import UmlLineDefinition
from pdfdiagrams.Definitions import MethodDefinition
from pdfdiagrams.Definitions import Methods
from pdfdiagrams.Definitions import ParameterDefinition
from pdfdiagrams.Definitions import Position
from pdfdiagrams.Definitions import RectangleDefinition
from pdfdiagrams.Definitions import Size

from pdfdiagrams.DiagramCommon import DiagramCommon
from pdfdiagrams.FPDFExtended import FPDFExtended

from pdfdiagrams.Internal import SeparatorPosition

from pdfdiagrams.DiagramLine import DiagramLine

from pdfdiagrams.Defaults import DEFAULT_LINE_WIDTH


class Diagram:
    """

    Always lays out in portrait mode.  Currently only supports UML classes with methods.  Only supports
    inheritance, composition, and aggregation lines.

    You are allowed to set the gap between UML classes both horizontally and vertically.  Also, you are allowed to
    specify the text font size
    """
    MethodsRepr = List[str]

    FPDF_DRAW: final = 'D'

    RESOURCES_PACKAGE_NAME: final = 'pdfdiagrams.resources'
    RESOURCES_PATH:         final = f'pdfdiagrams{osSep}resources'

    RESOURCE_ENV_VAR:       final = 'RESOURCEPATH'

    DEFAULT_FONT_SIZE:      final = 10

    X_NUDGE_FACTOR: final = 4
    Y_NUDGE_FACTOR: final = 4

    def __init__(self, fileName: str, dpi: int, headerText: str = ''):
        """

        Args:
            fileName:   Fully qualified file name
            dpi: dots per inch for the display we are mapping from
        """

        self._fileName: str = fileName
        self._dpi:      int = dpi
        self.logger: Logger = getLogger(__name__)

        pdf = FPDFExtended(headerText=headerText)
        pdf.add_page()

        pdf.set_display_mode(zoom='default', layout='single')

        pdf.set_line_width(DEFAULT_LINE_WIDTH)

        pdf.set_creator('Humberto A. Sanchez II - The Great')
        pdf.set_author('Humberto A. Sanchez II - The Great')

        pdf.set_font('Arial', size=Diagram.DEFAULT_FONT_SIZE)
        # self._pdf:      FPDF = pdf
        self._pdf: FPDFExtended = pdf
        self._pdf.headerText = 'Pyut Diagram Export'

        self._fontSize: int  = Diagram.DEFAULT_FONT_SIZE

        diagramPadding:   DiagramPadding = DiagramPadding()
        self._lineDrawer: DiagramLine    = DiagramLine(pdf=pdf, diagramPadding=diagramPadding, dpi=dpi)

        self._diagramPadding: DiagramPadding = diagramPadding

    @property
    def fontSize(self) -> int:
        return self._fontSize

    @fontSize.setter
    def fontSize(self, newSize: int):
        self._fontSize = newSize

    @property
    def horizontalGap(self) -> int:
        return self._diagramPadding.horizontalGap

    @horizontalGap.setter
    def horizontalGap(self, newValue: int):
        self._diagramPadding.horizontalGap = newValue

    @property
    def verticalGap(self) -> int:
        return self._diagramPadding.verticalGap

    @verticalGap.setter
    def verticalGap(self, newValue):
        self._diagramPadding.verticalGap = newValue

    @property
    def headerText(self) -> str:
        return self._pdf._headerText

    @headerText.setter
    def headerText(self, newValue: str):
        self._pdf._headerText = newValue

    @classmethod
    def retrieveResourcePath(cls, bareFileName: str) -> str:

        try:
            fqFileName: str = resource_filename(Diagram.RESOURCES_PACKAGE_NAME, bareFileName)
        except (ValueError, Exception):
            #
            # Maybe we are in an app
            #
            from os import environ
            pathToResources: str = environ.get(f'{Diagram.RESOURCE_ENV_VAR}')
            fqFileName:      str = f'{pathToResources}/{Diagram.RESOURCES_PATH}/{bareFileName}'

        return fqFileName

    def drawClass(self, classDefinition: ClassDefinition):
        """
        Draw the class diagram defined by the input

        Args:
            classDefinition:    The class definition
        """

        position:      Position = classDefinition.position
        verticalGap:   float = self._diagramPadding.verticalGap
        horizontalGap: float = self._diagramPadding.horizontalGap
        x, y = DiagramCommon.convertPosition(pos=position, dpi=self._dpi, verticalGap=verticalGap, horizontalGap=horizontalGap)
        self.logger.debug(f'x,y: ({x},{y})')

        methodReprs: Diagram.MethodsRepr = self._buildMethods(classDefinition.methods)

        symbolWidth: float = self._drawClassSymbol(classDefinition, rectX=x, rectY=y)

        separatorPosition: SeparatorPosition = self._drawNameSeparator(rectX=x, rectY=y, shapeWidth=symbolWidth)
        self._drawMethods(methodReprs=methodReprs, separatorPosition=separatorPosition)

    def drawUmlLine(self, lineDefinition: UmlLineDefinition):
        """
        Draw the inheritance, aggregation, or composition lines that describe the relationships
        between the UML classes

        Args:
            lineDefinition:   A UML Line definition
        """
        self._lineDrawer.draw(lineDefinition=lineDefinition)

    def drawEllipse(self, definition: EllipseDefinition):
        """
        Draw a general purpose ellipse

        Args:
            definition:     It's definition
        """

        x, y, width, height = self.__convertDefinition(definition)
        self._pdf.ellipse(x=x, y=y, w=width, h=height, style=definition.renderStyle)

    def drawRectangle(self, definition: RectangleDefinition):
        """
        Draw a general purpose rectangle

        Args:
            definition:  The rectangle definition

        """

        x, y, width, height = self.__convertDefinition(definition)
        self._pdf.rect(x=x, y=y, w=width, h=height, style=definition.renderStyle)

    def drawText(self, position: Position, text: str):
        """
        Draw text at the input position.  The method will appropriately convert the
        position to PDF points

        Args:
            position:  The display's x, y position
            text:   The text to display
        """

        x, y = DiagramCommon.convertPosition(position, dpi=self._dpi, verticalGap=self.verticalGap, horizontalGap=self.horizontalGap)
        self._pdf.text(x=x, y=y, txt=text)

    def write(self):
        """
        Call this method when you are done with placing the diagram onto a PDF document.
        """
        self._pdf.output(self._fileName)

    def _drawClassSymbol(self, classDefinition: ClassDefinition, rectX: float, rectY: float) -> float:
        """
        Draws the UML Class symbol.

        Args:
            classDefinition:    The class definition
            rectX:      x position
            rectY:      y position

        Returns:  The computed UML symbol width
        """

        symbolWidth:  float = classDefinition.size.width
        symbolHeight: float = classDefinition.size.height
        size: Size = Size(width=symbolWidth, height=symbolHeight)

        convertedWidth, convertedHeight = self.__convertSize(size=size)
        self._pdf.rect(x=rectX, y=rectY, w=convertedWidth, h=convertedHeight, style=Diagram.FPDF_DRAW)

        nameWidth: int = self._pdf.get_string_width(classDefinition.name)
        textX: float = rectX + ((symbolWidth / 2) - (nameWidth / 2))
        textY: float = rectY + self._fontSize

        self._pdf.text(x=textX, y=textY, txt=classDefinition.name)

        return convertedWidth

    def _drawNameSeparator(self, rectX: float, rectY: float, shapeWidth: float) -> SeparatorPosition:
        """
        Draws the UML separator between the class name and the start of the class definition
        Does the computation to determine where it drew the separator

        Args:
            rectX: x position of symbol
            rectY: y position of symbol (
            shapeWidth: The width of the symbol

        Returns:  Where it drew the separator

        """

        separatorX: float = rectX
        separatorY: float = rectY + self._fontSize + Diagram.Y_NUDGE_FACTOR

        endX: float = rectX + shapeWidth

        self._pdf.line(x1=separatorX, y1=separatorY, x2=endX, y2=separatorY)

        return SeparatorPosition(separatorX, separatorY)

    def _drawMethods(self, methodReprs: MethodsRepr, separatorPosition: SeparatorPosition):

        x: float = separatorPosition.x + Diagram.X_NUDGE_FACTOR
        y: float = separatorPosition.y + Diagram.Y_NUDGE_FACTOR + 8

        for methodRepr in methodReprs:

            self._pdf.text(x=x, y=y, txt=methodRepr)
            y = y + self._fontSize + 2

    def _buildMethods(self, methods: Methods) -> MethodsRepr:

        methodReprs: Diagram.MethodsRepr = []

        for methodDef in methods:

            methodRepr: str = self._buildMethod(methodDef)
            methodReprs.append(methodRepr)

        return methodReprs

    def _buildMethod(self, methodDef: MethodDefinition) -> str:

        methodRepr: str = f'{methodDef.visibility.value} {methodDef.name}'

        nParams:   int = len(methodDef.parameters)
        paramNum:  int = 0
        paramRepr: str = ''
        for parameterDef in methodDef.parameters:
            parameterDef = cast(ParameterDefinition, parameterDef)
            paramNum += 1

            paramRepr = f'{paramRepr}{parameterDef.name}'

            if parameterDef.parameterType is None or len(parameterDef.parameterType) == 0:
                paramRepr = f'{paramRepr}'
            else:
                paramRepr = f'{paramRepr}: {parameterDef.parameterType}'

            if parameterDef.defaultValue is None or len(parameterDef.defaultValue) == 0:
                paramRepr = f'{paramRepr}'
            else:
                paramRepr = f'{paramRepr}={parameterDef.defaultValue}'

            if paramNum == nParams:
                paramRepr = f'{paramRepr}'
            else:
                paramRepr = f'{paramRepr}, '

        methodRepr = f'{methodRepr}({paramRepr})'

        return methodRepr

    def __convertDefinition(self, definition: RectangleDefinition) -> Tuple[float, float, float, float]:
        """

        Args:
            definition:

        Returns: a tuple of x, y, width height
        """
        x, y = DiagramCommon.convertPosition(definition.position, dpi=self._dpi, verticalGap=self.verticalGap, horizontalGap=self.horizontalGap)
        width, height = self.__convertSize(definition.size)

        return x, y, width, height

    def __convertSize(self, size: Size) -> Tuple[float, float]:

        width:  float = DiagramCommon.toPdfPoints(size.width, self._dpi)
        height: float = DiagramCommon.toPdfPoints(size.height, self._dpi)

        return width, height
