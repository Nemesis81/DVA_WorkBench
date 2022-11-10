# -*- coding: utf-8 -*-

# DVAUtils compile function used in various algorythm for DVA
# list of point, storage of value
import numpy as np


def listDvaPoints(Objs):
    """Return a list of DVAPoints objects """
    ptList = []
    for obj in Objs:
        if hasattr(obj, "Law"):
            ptList.append(obj)
    return ptList


def listAssyConstraints(Objs):
    """
    Return a list of Constraints objects upgrade in DVA constraints
    """
    ctrList = []
    for obj in Objs:
        if hasattr(obj, "Law"):
            ctrList.append(obj)
    return ctrList


def initialStateSave(Objs):
    """Return a Dict of all initial values for DVA points an constraint """

    dict = {}
    c = 0
    dva = []
    pt = []
    ct = []
    for obj in Objs:
        dva =[obj.Law,
              obj.Tolerance,
              obj.Meanshift,
              obj.Sd]

        if hasattr(obj, "Law") and hasattr(obj, "Placement"):
            pt = [obj.AttachmentOffset.Base.x,
                  obj.AttachmentOffset.Base.y,
                  obj.AttachmentOffset.Base.z]
            dict[obj] = dva + pt
        elif hasattr(obj, "Law") and hasattr(obj, "Distance"):
            ct = [obj.Distance]
            dict[obj.Name] = dva + ct

        c = c + 1
    return dict


def backInitialState(dict, doc):
    for pt in dict:
        # b = dict
        if isinstance(pt, str):
            b = doc.getObject(pt)
            values = dict.get(pt)
            # print("if is instnce = ",b.Name, b.Distance)
            b.Distance = values[4]

        else:
            b = pt
            values = dict.get(pt)
            #   print("else = ",b.Name)
            b.AttachmentOffset.Base.x = values[4]
            b.AttachmentOffset.Base.y = values[5]
            b.AttachmentOffset.Base.z = values[6]

        b.Law = values[0]
        b.Tolerance = values[1]
        b.Meanshift = values[2]
        b.Sd = values[3]

        #if hasattr(pt, "Law") and hasattr(pt, "Placement"):



        #if hasattr(pt, "Distance"):
            #print("inside elif hasattr(pt, Law) and hasattr(pt, Distance)",
                  #pt.Distance)
            #b.Distance = values[4]


def affectValue(law, **kwargs):
    """
    Affect a random value according Law and parameters, return the value
    law as 1st arg = Normal or Uniform
    **kwargs :
    - tolerance = expected tolerance
    - sigma = standard deviation
    - mu = meanshift
    """
    tol = kwargs.get('tolerance', None)
    sig = kwargs.get('sigma', None)
    mu = kwargs.get('mu', 0)

    if tol!= None or tol!= 0:
       sig =  tol/6
       mu = 0
    elif sig is not None or sig!= 0:
        tol = sig*3

    if law == "Normal":
        value = np.random.normal(mu, sig)

    elif law == "Uniform":
        value = np.random.uniform(-tol/2, tol/2, 1)
        value = value[0]

    return value


def affectHLMValue(hlm, **kwargs):
    """
    Affect a Hig, low or mean value according parameter
    0 = highest value
    1 = mean value
    2 = lowest value
    """
    tol = kwargs.get('tolerance', None)
    sig = kwargs.get('sigma', None)
    mu = kwargs.get('mu', 0)

    if tol is not None or tol != 0:
        sig = tol/6
        mu = 0

    if hlm == 0:
        high = mu + sig*3
        return high

    elif hlm == 1:
        return mu

    elif hlm == 2:
        low = mu - sig*3
        return low


def recordMeasurement(obj):
    """
    record measurment
    """
    ls = ((obj.AttachmentOffset.Base.x,
           obj.AttachmentOffset.Base.y,
           obj.AttachmentOffset.Base.z,
           obj.Shape.Point[0],
           obj.Shape.Point[1],
           obj.Shape.Point[2]))

    return ls


def dvaPtRndVal(obj, vallist, ptname, repet):
    """
    obj => list of DVApoint object  to affect a new alues based on Law
    vallist => list of values
    ptname => list of point name
    repet => numbers of repet to get name on 1st loop
    returns a list of values and a list of point name
    """
    for dvaPt in obj:
        if dvaPt.isDerivedFrom("Part::Feature"):
            ptx = affectValue(dvaPt.Law, tolerance=dvaPt.Tolerance)
            pty = affectValue(dvaPt.Law, tolerance=dvaPt.Tolerance)
            ptz = affectValue(dvaPt.Law, tolerance=dvaPt.Tolerance)

            dvaPt.AttachmentOffset.Base.x = dvaPt.AttachmentOffset.Base.x + ptx
            dvaPt.AttachmentOffset.Base.y = dvaPt.AttachmentOffset.Base.y + pty
            dvaPt.AttachmentOffset.Base.z = dvaPt.AttachmentOffset.Base.z + ptz
            dvaPt.recompute(True)

            if dvaPt.Measurement:
                vallist.extend(recordMeasurement(dvaPt))

                if repet == 0:
                    ptname.extend((dvaPt.Label + " x",
                                   dvaPt.Label + " y",
                                   dvaPt.Label + " z",
                                   dvaPt.Label + " GPx",
                                   dvaPt.Label + " GPy",
                                   dvaPt.Label + " GPz"))

        elif dvaPt.isDerivedFrom("App::FeaturePython"):
            if repet == 0:
                ptname.append(dvaPt.Label)

            if dvaPt.ConstraintType=="PointsPlaneDistance":
                dvaPt.Distance = str(affectValue(dvaPt.Law,
                                                 tolerance=dvaPt.Tolerance,
                                                 sigma=dvaPt.Sd))
                dvaPt.recompute(True)


            if dvaPt.Measurement:
                dvaPt.recompute(True)
                vallist.append(float(dvaPt.Distance))



    return vallist, ptname

def dvaHLMRndVal(obj, vallist, ptname, repet):
    """
    obj => DVApoint object or cstr to affect a new alues based on Law
    vallist => list of values
    ptname => list of point name
    repet => numbers of repet to get name on 1st loop
    returns a list of values and a list of point name
    """
    if obj.isDerivedFrom("Part::Feature"):
        ptx = affectValue(obj.Law, tolerance=obj.Tolerance)
        pty = affectValue(obj.Law, tolerance=obj.Tolerance)
        ptz = affectValue(obj.Law, tolerance=obj.Tolerance)

        obj.AttachmentOffset.Base.x = obj.AttachmentOffset.Base.x + ptx
        obj.AttachmentOffset.Base.y = obj.AttachmentOffset.Base.y + pty
        obj.AttachmentOffset.Base.z = obj.AttachmentOffset.Base.z + ptz
        obj.recompute(True)

        if obj.Measurement:
            vallist.extend(recordMeasurement(obj))

            if repet == 0:
                ptname.extend((obj.Label + " x",
                               obj.Label + " y",
                               obj.Label + " z",
                               obj.Label + " GPx",
                               obj.Label + " GPy",
                               obj.Label + " GPz"))
    elif obj.isDerivedFrom("App::FeaturePython") and obj.ConstraintType=="PointsPlaneDistance":
        obj.Distance = str(affectValue(obj.Law,
                                         tolerance=obj.Tolerance,
                                         sigma=obj.Sd))
        if obj.Measurement and (obj.ConstraintType=="PointsPlaneDistance" or obj.ConstraintType=="MeasurePoints"):
            print(obj.Distance)
            vallist.append(float(obj.Distance))

            if repet == 0:
                ptname.append(obj.Label)

    return vallist, ptname
