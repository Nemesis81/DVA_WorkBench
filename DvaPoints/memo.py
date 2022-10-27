class AttachedPoint():

    def __init__(self,obj):
        obj.Proxy = self
        obj.addExtension('Part::AttachExtensionPython')
        self.Type = "AttachedPoint"

    def execute(self, obj):
        # We need to import the FreeCAD module here too, because we might be running out of the Console
        # (in a macro, for example) where the FreeCAD module has not been imported automatically:
#        import FreeCAD
#        import Part

        f = Part.Point(App.Vector(0, 0, 0)).toShape()
        obj.positionBySupport() #add attachment

        # All done, we can attribute our shape to the object!
        obj.Shape = f


doc = App.ActiveDocument
sels = Gui.Selection.getSelectionEx('',0)
if len(sels) == 1 and sels[0].HasSubObjects and len(sels[0].SubObjects) == 1 and sels[0].SubObjects[0].ShapeType == 'Edge': #one edge or bail out?
    sel =sels[0]
    path = sel.SubElementNames[0]
    res = sel.Object.resolveSubElement(path)
    support = (res[0],res[-1]) # is this general - seems like a hack?
    globalPlacement = sel.Object.getSubObject(path, retType=3)
    pickLoc = globalPlacement.inverse().multVec(sel.PickedPoints[0]) #picked point in LCS
    edge = sel.SubObjects[0]
    parameter = edge.Curve.parameter(pickLoc) #parameter on curve
    curveLoc = edge.valueAt(parameter)
    mapPathParameter = (parameter - edge.FirstParameter)/(edge.LastParameter - edge.FirstParameter) #normalize 0-1
    isBody = (sel.Object.TypeId == 'PartDesign::Body')
    if isBody: #make a Datum Point - already parametric
        point = sel.Object.newObject("PartDesign::Point", "AttachedPoint")
        point.MapMode = 'OnEdge'
    else: #make a FeaturePython wrapped Part.Point
        point = doc.addObject("Part::FeaturePython", "AttachedPoint")
        myPoint = AttachedPoint(point)
        point.ViewObject.Proxy = 0 # This is mandatory unless we code the ViewProvider too.
        point.MapMode = 'NormalToEdge'
    point.Support = support
    point.MapPathParameter = mapPathParameter
    doc.recompute()
    #App.Console.PrintMessage(f'\npicked loc {pickLoc}\n point loc {point.Shape.Point}\n  curve loc {globalPlacement.inverse().multVec(curveLoc)}\n')

else:
    App.Console.PrintMessage(f'Select a single Edge, then run the Macro')
