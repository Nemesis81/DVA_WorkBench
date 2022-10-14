# -*- coding: utf-8 -*-

import FreeCAD as App
import PartDesign
import Part
import FreeCADGui as Gui



class cmd_DvaPointDg():
    """My new command"""

    def GetResources(self):
        return {"Pixmap"  : "Draft_Downgrade.svg", # the name of a svg file available in the resources
                "Accel"   : "", # a default shortcut (optional)
                "MenuText": "Downgrade Constraint DVA Point",
                "ToolTip" : "Downgrade a DVA point or constraint by removing DVA property"}

    def Activated(self):
        """
        Object creation method
        """
        
        obj = Gui.Selection.getSelection()
        dvaPointDg(obj)
        App.ActiveDocument.recompute()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True



class dvaPointDg():

    def __init__(self, objg):
        """
        Default constructor
        """
        for obj in objg:
            obj.removeProperty('Law')
            obj.removeProperty("Tolerance")
            obj.removeProperty('Sd')
            obj.removeProperty('Meanshift')

    def execute(self, obj):
        """
        Called on document recompute
        """
        App.ActiveDocument.recompute()
Gui.addCommand("DVA Point DownGrading", cmd_DvaPointDg())



class cmd_dvaPointUg():
    """My new command"""

    def GetResources(self):
        return {"Pixmap"  : "a2p_RepairTree.svg", # the name of a svg file available in the resources
                "Accel"   : "", # a default shortcut (optional)
                "MenuText": "Upgrade Constraint DVA Point",
                "ToolTip" : "Upgrade a DVA point or constraint by adding DVA property"}

    def Activated(self):
        """
        Object creation method
        """
        
        objg = Gui.Selection.getSelection()
        dvaPointUg(objg)
        App.ActiveDocument.recompute()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True



class dvaPointUg():
    
    def __init__(self, objg):
        """
        Default constructor
        """

        for obj in objg:
            obj.addProperty('App::PropertyEnumeration', 'Law', 'DVA', 'Law to apply (normal, uniform ...)').Law
            obj.Law = ["Normal", "Uniform"]
            obj.addProperty('App::PropertyLength', 'Tolerance', 'DVA', 'Tolerance for cp=1.33').Tolerance = 1
            obj.addProperty('App::PropertyLength', 'Sd', 'DVA', 'standard deviation').Sd = '0.15 mm'
            obj.addProperty('App::PropertyLength', 'Meanshift', 'DVA', 'optional meanshift').Meanshift = '0 mm'
            obj.addProperty("App::PropertyBool", "Measurement", "DVA", "Statement to output the simulation values of this point").Measurement = True

    def execute(self, obj):
        """
        Called on document recompute
        """
        App.ActiveDocument.recompute()
        
Gui.addCommand("DVA Point UpGrading", cmd_dvaPointUg())