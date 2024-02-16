# DVA_WorkBench
## Purpose

Purpose of this workbench is to be able to perform Dimensional Variation Analysis (DVA) within Freecad.
[Assembly3](https://github.com/realthunder/FreeCAD_assembly3) is used a assembly solver, to calculate the result variation based on assembly variation and parts variation.

## Principle

working steps are the following:

* Create a DVA Analysis object.
* In each part involved, create DVA points and assign tolerance or standard deviation and meanshift.
* Build the assembly3 model using DVA points as element to localise the part, following the assembly process expected, using Point/Plane distance
* upgrade the assembly3 constraints to DVAConstraint and assign tolerance or standard deviations and meanshift.
* define in the DVA object:
  * the analysis type
  * sample to run
  * output file
* Run the analysis
* results are in the csv file define in the DVA Analysis obect.

see example file in the exaple folder to get an overview

## Important point:
As for now it only works with FreeCAD Linkbranch, due to this [bug](https://forum.freecadweb.org/viewtopic.php?f=20&t=72256)


## to do:
1. develop different kind of analysis:
  * Monte carlo analysis.
  * sensitive analysis based on HLM (High Mean Low) values of each tolerance of the assembly
  * Worst Case analysis based on all value in Max/min condition (need to know direction of impact....)
2. integrate a html report directly in freecad (Streamlit? matplot only?)
3. link DVA constraint and DVA point within DVA folder for clarity.
4. see the possiblity to revive the [GD&T WB](https://github.com/juanvanyo/FreeCAD-GDT)
