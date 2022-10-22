# -*- coding: utf-8 -*-

# Macro Begin: C:\Users\thierry.garel\AppData\Roaming\FreeCAD\Macro\changeTolernace.FCMacro ++++
import FreeCAD
import numpy as np
import pandas as pd
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

        with open(FilePath, "w", newline="") as f:
            data = csv.writer(f)
            dele=[]
            data.writerow(dele)
        f.close

        ### DVA_Points referes to points with a tolerance inside a Body
        ### in the case study


        DvaPts = Doc.findObjects("PartDesign::Point")
        DvaPts = dvu.listDvaPoints(DvaPts)

        Contraintes = Doc.findObjects("App::FeaturePython")
        Contraintes = dvu.listAssyConstraints(Contraintes)

        InitialState = dvu.initialStateSave(Contraintes + DvaPts, Doc)
        Repet = Doc.getObject("DVA_Analysis").Sample

