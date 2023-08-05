
from typing import List

from enum import Enum

from dataclasses import dataclass
from dataclasses import field

from pdfdiagrams.Defaults import TOP_MARGIN
from pdfdiagrams.Defaults import LEFT_MARGIN
from pdfdiagrams.Defaults import DEFAULT_HORIZONTAL_GAP
from pdfdiagrams.Defaults import DEFAULT_VERTICAL_GAP

ClassName = str


@dataclass
class Position:
    """
    The x and y coordinates are in screen/display resolution.  This module converts
    to points for use in this system

    """
    x: float = 0.0
    y: float = 0.0


@dataclass
class DiagramPadding:

    topMargin:  int = TOP_MARGIN
    leftMargin: int = LEFT_MARGIN

    horizontalGap: int = DEFAULT_HORIZONTAL_GAP
    verticalGap:   int = DEFAULT_VERTICAL_GAP


@dataclass
class Size:
    """
    Defines the size of the input UML definitions;
    """
    width:  float = 100
    height: float = 100


class DefinitionType(Enum):
    """
    Defines the visibility of either methods or fields
    """
    Public    = '+'
    Private   = '-'
    Protected = '#'


@dataclass
class BaseDefinition:

    __slots__ = ['name']
    name: str
    """
    The name associated with the definition.
    """


@dataclass
class ParameterDefinition(BaseDefinition):
    """
    Defines a single parameter for a method
    """
    parameterType: str = ''
    defaultValue:  str = ''


Parameters = List[ParameterDefinition]


@dataclass
class MethodDefinition(BaseDefinition):
    """
    Defines a single method in a UML class
    """

    visibility: DefinitionType = DefinitionType.Public
    returnType: str            = ''
    parameters: Parameters     = field(default_factory=list)


Methods = List[MethodDefinition]


@dataclass
class ClassDefinition(BaseDefinition):
    """
    The class definition.  Currently, does not supports instance properties.
    """

    size:     Size     = Size()
    position: Position = Position(0, 0)
    methods: Methods   = field(default_factory=list)


ClassDefinitions = List[ClassDefinition]


class LineType(Enum):
    """
    The type of line you wish to draw.  Currently, straight assoications are not supported.
    """
    Inheritance  = 0
    Aggregation  = 1
    Composition  = 3
    Association  = 7


@dataclass
class LineDefinition:
    """
    Defines just a line between two points
    """
    source:              Position
    destination:         Position


@dataclass
class UmlLineDefinition(LineDefinition):
    """
    A UML Line definition includes its' type
    """
    lineType:            LineType


UmlLineDefinitions = List[UmlLineDefinition]


class RenderStyle(Enum):

    Draw     = 'D'
    Fill     = 'F'
    DrawFill = 'DF'


@dataclass
class RectangleDefinition:

    renderStyle: RenderStyle = RenderStyle.Draw
    position:    Position    = Position(0, 0)
    size:        Size        = Size(0, 0)


@dataclass
class EllipseDefinition(RectangleDefinition):
    pass
