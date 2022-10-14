# DVA_WorkBench
## Purpose

Purpose of this workbench is to be able to perform Dimensional Variation Analysis (DVA) within Freecad.
[Assembly3](https://github.com/realthunder/FreeCAD_assembly3) is used a assembly solver, to calculate the result variation based on assembly variation and parts variation.

## Principle

working steps are the following:

* Create a DVA Analysis object.
* In each part involved, create DVA points and assign tolerance or standard deviation and meanshift.
* Build the assembly3 model uwing DVA points as element to localise the part, following the assembly process expected, using Point/Plane distance
* upgrade the assembly3 constraints to DVAConstraint and assign tolerance or standard deviations and meanshift.
* define in the DVA object:
  * the analysis type
  * sample to run
  * output file
* Run the analysis

results are in the output folder for post treatment.

## to do:
1. devlop sensitive analysis
1. integrate a html report directly in freecad
2. link DVA constraint and DVA point within DVA folder for clarity
