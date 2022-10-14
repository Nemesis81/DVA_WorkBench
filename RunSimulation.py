# -*- coding: utf-8 -*-

# Macro Begin: C:\Users\thierry.garel\AppData\Roaming\FreeCAD\Macro\changeTolernace.FCMacro ++++
import FreeCAD
import numpy as np
import csv   
import DVAUtils as dvu
import time
from datetime import timedelta




class cmd_runSimulationMC():
        """Run DVA MonteCarlo Simulation"""

    def GetResources(self):
        return {"Pixmap"  : "PartDesign_Point.svg", # the name of a svg file available in the resources
                "Accel"   : "Shift+S", # a default shortcut (optional)
                "MenuText": "Create DVA Point",
                "ToolTip" : "Create a DVA point inside the active body if there is one"}
                


    def Activated(self):
        """
        Object creation method
        """

        start = time.time()
        print("starting simulation at: ", start)
        Doc= FreeCAD.ActiveDocument
        FilePath = Doc.getObject("DVA_Analysis").Output_File
        ##"# preparing the file
        file1 = open(FilePath, "w")
        L = []

        file1.writelines(L)
        file1.close
        file1 = open(FilePath, "a")

        ### DVA_Points referes to points with a tolerance inside a Body
        ### in the case study


        DvaPts = Doc.findObjects("PartDesign::Point")
        DvaPts = dvu.listDvaPoints(DvaPts)

        Contraintes = Doc.findObjects("App::FeaturePython")
        Contraintes = dvu.listAssyConstraints(Contraintes)

        InitialState = dvu.initialStateSave(Contraintes + DvaPts, Doc)
        Repet = Doc.getObject("DVA_Analysis").Sample

