# -*- coding: utf-8 -*-
import os
import FreeCAD
import FreeCADGui
import os



__title__ = "FreeCAD DVA Workbench - Init file"
__author__ = "Nemesis81"
__url__ = "none"



class DVA_Wb (Workbench):

    ICONPATH = os.path.join(FreeCAD.getUserAppDataDir(),"Mod", "DVAWB", "ressources")
    MenuText = "DVA Workbench"
    ToolTip = "A description of my workbench"
    Icon = os.path.join(ICONPATH, "DVA_RunMC_Simulation.svg")

    def Initialize(self):
        """This function is executed when the workbench is first activated.
        It is executed once in a FreeCAD session followed by the Activated function.
        """
        import DvaPoints.DVAPoints #as dvp
        import DvaPoints.ConstraintGrad # as dvc
        import DVAAnalysis #as dva
        import RunSimulation
        self.list = ["DVA Analisys Creation",
                     "DVA Point Creation",
                     "DVA Point UpGrading",
                     "DVA Point DownGrading",
                     "Run H.L.M. Simulation",
                     "Run MonteCarlo Simulation"]

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
