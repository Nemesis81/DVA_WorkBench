# -*- coding: utf-8 -*-

import FreeCAD as App
import numpy as np
import pandas as pd
import csv
import DVAUtils as dvu
import time
from datetime import timedelta
import FreeCADGui as Gui
import os


TOOL_ICONMC = os.path.join(App.getUserAppDataDir(),
                           "Mod",
                           "DVA_WorkBench",
                           "ressources",
                           "DVA_RunMC_Simulation.svg")

TOOL_ICONHLM = os.path.join(App.getUserAppDataDir(),
                            "Mod",
                            "DVA_WorkBench",
                            "ressources",
                            "DVA_RunHLM_Simulation.svg")

class cmd_runMcSimulation():
    """
    Run DVA MonteCarlo Simulation
    """
    def GetResources(self):
        return {"Pixmap"  : TOOL_ICONMC,
                "Accel"   : "Shift+S",
                "MenuText": "Run DVA MonteCarlo simulation",
                "ToolTip" : "Create a DVA point inside the active body if there is one"}

    def Activated(self):
        """
        Object creation method
        """
        start = time.time()
        print("starting simulation at: ", start)
        Doc= App.ActiveDocument
        FilePath = Doc.getObject("DVA_Analysis").OutputFile
        Repet = Doc.getObject("DVA_Analysis").Sample
        with open(FilePath, "w", newline="") as f:
            data = csv.writer(f)
            dele = []
            data.writerow(dele)
        f.close

        # DVA_Points refers to points with a tolerance inside a Body
        # in the case study
        DvaPts = Doc.findObjects("PartDesign::Point")
        DvaPts = dvu.listDvaPoints(DvaPts)

        # Contraintes are the constraint Simulating process variation
        Contraintes = Doc.findObjects("App::FeaturePython")
        Contraintes = dvu.listAssyConstraints(Contraintes)

        DvaPts = DvaPts + Contraintes
        # Mesure are the measurement from Assy3 with DVA upgrade
        Mesure = Doc.getObject("DVA_Analysis").ListPoints
        InitialState = dvu.initialStateSave(DvaPts)

        b = []

        for x in np.arange(0, Repet, 1):
            a = []

            dvu.dvaPtRndVal(DvaPts, a, b, x)
            Gui.runCommand('asm3CmdSolve',0)

            for mes in Mesure:
                MesPt = Doc.getObject(mes)
                if hasattr(MesPt,"Measurement"):
                    if MesPt.Measurement:
                        a.append(float(MesPt.Distance))
                        if x==0:
                            b.append(MesPt.Label)

            if x==0:
                dtNames = np.asarray(b)
                dtNames = np.expand_dims(dtNames,axis=1)

            dt = np.asarray(a)
            dt = np.expand_dims(dt,axis=1)

            if x==0:
                dt2=dt

            dt2 = np.append(dt2, dt, axis=1)
            dvu.backInitialState(InitialState, Doc)
            if Doc.getObject("DVA_Analysis").UpdateGui:
                Gui.updateGui()

            print("simulation loop:", x)

        dtfull = np.concatenate((dtNames,dt2), axis=1)
        dtfull = np.transpose(dtfull)
        pddf = pd.DataFrame(data=dtfull[1:,1:],
                            columns=dtfull[0,1:],
                            dtype=float)

        hist = pddf[["MeasurePoints",
                      "MeasurePoints001"]].hist(bins=8)

        pddf.to_csv(FilePath, sep=',', header=True)

        f.close
        end = time.time()
        print("Simulation performed in : ",timedelta(seconds=end - start))
        App.ActiveDocument.recompute()

        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True





class cmd_runHLMSimulation():
    def GetResources(self):
        return {"Pixmap"  : TOOL_ICONHLM,
                "Accel"   : "",
                "MenuText": "Run HLM simulation",
                "ToolTip" : "Run a High Low Median Simulation for worst case study, and sensitive analysis"}

    def Activated(self):
        """
        Object creation method
        """
        start = time.time()
        print("starting simulation at: ", start)
        Doc= App.ActiveDocument
        FilePath = Doc.getObject("DVA_Analysis").Output_File

        with open(FilePath, "w", newline="") as f:
            data = csv.writer(f)
            dele = []
            data.writerow(dele)
        f.close

        # DVA_Points refers to points with a tolerance inside a Body
        # in the case study
        DvaPts = Doc.findObjects("PartDesign::Point")
        DvaPts = dvu.listDvaPoints(DvaPts)

        # Contraintes are the constraint Simulating process variation
        Contraintes = Doc.findObjects("App::FeaturePython")
        Contraintes = dvu.listAssyConstraints(Contraintes)

        Repet = Doc.getObject("DVA_Analysis").Sample

        # Mesure are the measurement from Assy3 with DVA upgrade
        Mesure = Doc.getObject("DVA_Analysis").DVA_ListPoints
        InitialState = dvu.initialStateSave(Contraintes + DvaPts, Doc)

        # loop on all modifcation point, constraint..
        a = []
        b = []
        for dvaPt in DvaPts:
            dvu.backInitialState(InitialState, Doc)
            for hlm in np.arange(0, 3, 1):
                dvu.backInitialState(InitialState, Doc)

                Variation = Doc.getObject(dvaPt)

                Variation.AttachmentOffset.Base.x = Variation.AttachmentOffset.Base.x
                + dvu.affectHLMValue(hlm, tolerance=Variation.Tolerance)

                Variation.AttachmentOffset.Base.y = Variation.AttachmentOffset.Base.y
                + dvu.affectHLMValue(hlm, tolerance=Variation.Tolerance)

                Variation.AttachmentOffset.Base.z = Variation.AttachmentOffset.Base.z
                + dvu.affectHLMValue(hlm, tolerance=Variation.Tolerance)

                # then for each modification, record status of all mesaurement
                if hasattr(Variation,"Measurement"):
                    if Variation.Measurement:
                        a.extend(dvu.recordMeasurement(Variation))

                Gui.runCommand('asm3CmdSolve',0)

                for mes in Mesure:
                    MesPt = Doc.getObject(mes)
                    if hasattr(MesPt,"Measurement"):
                        if MesPt.Measurement:
                            a.append(float(MesPt.Distance))
                            if hlm==0:
                                b.append(MesPt.Label)

        for Cstr in Contraintes:
            dvu.backInitialState(InitialState, Doc)
            for hlm in np.arange(0, 3, 1):
                Variation = Doc.getObject(Cstr)
                Variation.Distance = str(dvu.affectHLMValue(hlm,tolerance=Variation.Tolerance))
                if Variation.Measurement:
                    a.append(float(Variation.Distance))
                    if hlm == 0: b.append(Variation.Label)
        print(a)




        # then set it again to initial backInitialState
        # then start again with next point


    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

Gui.addCommand("Run H.L.M. Simulation", cmd_runHLMSimulation())
Gui.addCommand("Run MonteCarlo Simulation", cmd_runMcSimulation())
