The documentation is [here](https://hasii2011.github.io/pdfdiagrams/pdfdiagrams/index.html).



Sample Snippets



Create a basic class

```python
diagram: Diagram = Diagram(fileName='basicClass.pdf', dpi=75)
classDef: ClassDefinition = ClassDefinition(name='BasicClass', size=Size(width=100, height=100))

diagram.drawClass(classDef)
diagram.write()
```



Create a class with a method

```python
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

```



Create inheritance diagram



```python
diagram: Diagram = Diagram(fileName='MinimalInheritance.pdf', dpi=75)

cat:  ClassDefinition = ClassDefinition(name='Gato', position=Position(536, 19), size=Size(height=74, width=113))
opie: ClassDefinition = ClassDefinition(name='Opie', position=Position(495, 208), size=Size(width=216, height=87))

diagram.drawClass(classDefinition=cat)
diagram.drawClass(classDefinition=opie)

opieToCat: UmlLineDefinition = UmlLineDefinition(lineType=LineType.Inheritance, source=Position(600, 208), destination=Position(600, 93))

diagram.drawUmlLine(lineDefinition=opieToCat)
diagram.write()
```

