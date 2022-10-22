# -*- coding: utf-8 -*-

import FreeCAD as App
import PartDesign
import Part
import FreeCADGui as Gui



class cmd_dvaPoint():
    """My new command"""

    def GetResources(self):
        return {"Pixmap"  : "PartDesign_Point.svg", # the name of a svg file available in the resources
                "Accel"   : "Shift+S", # a default shortcut (optional)
                "MenuText": "Create DVA Point",
                "ToolTip" : "Create a DVA point inside the active body if there is one"}

    def Activated(self):
        """
        Object creation method
        """

        body = Gui.ActiveDocument.ActiveView.getActiveObject('pdbody')
        obj = App.ActiveDocument.addObject('PartDesign::Point', "DVAPoint")
        obj.MapMode = 'Deactivated'
        dvaPoint(obj)
        if type(body)=='NoneType':
            print("No active Body")
        else:
            body.addObject(obj)

        App.ActiveDocument.recompute()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True


class dvaPoint():
    def __init__(self, obj):
        """
        Default constructor
        """

        self.Type = 'dvaPoint'

        #obj.Proxy = self

        obj.addProperty('App::PropertyEnumeration', 'Law', 'DVA', 'Law to apply (normal, uniform ...)').Law
        obj.Law = ["Normal", "Uniform"]
        obj.addProperty('App::PropertyLength', 'Tolerance', 'DVA', 'Tolerance for cp=1.33').Tolerance = 1
        obj.addProperty('App::PropertyLength', 'Sd', 'DVA', 'standard deviation').Sd = '0.15 mm'
        obj.addProperty('App::PropertyLength', 'Meanshift', 'DVA', 'optional meanshift').Meanshift = '0 mm'
        obj.addProperty("App::PropertyBool", "Measurement", "DVA", "Statement to output the simulation values of this point").Measurement = True


    def onChanged(self, obj, prop):
        """
        gives define the data according input
        if input = Tol define Mu and Sigma
        if input = Sigma define Tol
        """
        print(obj.prop)
        # print("line 68")
        # cp = App.ActiveDocument.getObject("DVA_Analysis")
        # print(cp)

        # if type(cp) == 'NoneType':
            # print('No DVA Analysis !')
        # else:
            # cp = doc.getObject("DVA_Analysis").Cp
            # print(cp)
            # obj.Sd = Tolerance / (6*cp)

    def execute(self, obj):
        """
        Called on document recompute
        """
        App.ActiveDocument.recompute()

    def onDocumentRestored(self, obj):
        obj.Proxy = self



Gui.addCommand("DVA Point Creation", cmd_dvaPoint())
