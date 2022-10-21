# -*- coding: utf-8 -*-
import os
import FreeCAD
import FreeCADGui

__title__ = "FreeCAD DVA Workbench - Init file"
__author__ = "Nemesis81"
__url__ = "none"


class DVA_Wb (Workbench):

    MenuText = "DVA Workbench"
    ToolTip = "A description of my workbench"
    #Icon = "Plot_workbench_icon.svg"

    def Initialize(self):
        """This function is executed when the workbench is first activated.
        It is executed once in a FreeCAD session followed by the Activated function.
        """
        import DvaPoints.DVAPoints as dvp # import here all the needed files that create your FreeCAD commands
        import DvaPoints.ConstraintGrad as dvc
        import DVAAnalysis as dva
        self.list = [dvp.cmd_dvaPoint(),
                     dvc.cmd_DvaPointDg(),
                     dvc.cmd_dvaPointUg(),
                     dva.cmd_dvaAnalysis() ]      # A list of command names created in the line above
        self.appendToolbar("DVA",self.list) # creates a new toolbar with your commands
        self.appendMenu("DVA tool",self.list) # creates a new menu
        #self.appendMenu(["An existing Menu","My submenu"],self.list) # appends a submenu to an existing menu

    def Activated(self):
        """This function is executed whenever the workbench is activated"""
        return

    def Deactivated(self):
        """This function is executed whenever the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This function is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        #self.appendContextMenu("DVAPoints",self.list) # add commands to the context menu

    def GetClassName(self):
        # This function is mandatory if this is a full Python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"

Gui.addWorkbench(DVA_Wb())
