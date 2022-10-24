# -*- coding: utf-8 -*-

# DVAUtils compile function used in various algorythm for DVA
# list of point, storage of value
#

# import FreeCAD as app
# import FreeCADGui as gui
import numpy as np



def listDvaPoints(Objs):
    """Return a list of DVAPoints """
    ptList=[]
    for obj in Objs:
        if hasattr(obj, "Law"):
           ptList.append(obj.Name)
    return ptList


def listAssyConstraints(Objs):
    """Re-run a list of Constraints upgrade in DVA constraints """
    ctrList=[]
    for obj in Objs:
        if hasattr(obj, "Law"):
            ctrList.append(obj.Name)
    return ctrList


def initialStateSave(Objs,doc):
    """Return a Dict of all initial values for DVA points an constraint """

    dict = {}
    c = 0
    dva = []
    pt =[]
    ct = []
    for i in Objs:
        b = doc.getObject(Objs[c])
        dva =[b.Law,
              b.Tolerance,
              b.Meanshift,
              b.Sd]

        if hasattr(b, "Law") and hasattr(b, "Placement"):
            pt = [b.AttachmentOffset.Base.x,
                  b.AttachmentOffset.Base.y,
                  b.AttachmentOffset.Base.z]
            dict[i] = dva + pt
        elif hasattr(b, "Law") and hasattr(b, "Distance"):
            ct = [b.Distance]
            dict[i] = dva + ct
            #print(dict)

        c = c + 1
    return dict


def backInitialState(dict, doc):
    for pt in dict:
        b = dict
        b = doc.getObject(pt)
        values = dict.get(pt)
        b.Law = values[0]
        b.Tolerance = values[1]
        b.Meanshift = values[2]
        b.Sd = values[3]

        if hasattr(b, "Law") and hasattr(b, "Placement"):
            b.AttachmentOffset.Base.x = values[4]
            b.AttachmentOffset.Base.y = values[5]
            b.AttachmentOffset.Base.z = values[6]

        elif hasattr(b, "Law") and hasattr(b, "Distance"):
            b.Distance = values[4]


def affectValue(law, **kwargs):
    """Affect a random value according Law and parameters, return the value """
    tol = kwargs.get('tolerance', None)
    sig = kwargs.get('sigma', None)
    mu = kwargs.get('mu', 0)

    if tol!= None or tol!= 0:
       sig =  tol/6
       mu = 0
    elif sig is not None or sig!= 0:
         tol = sig*3

    if law == "Normal":
        value = np.random.normal(mu,sig)

    elif law == "Uniform":
        value = np.random.uniform(-tol/2, tol/2,1)
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

    if tol is not None or tol!= 0:
        sig =  tol/6
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
    ls=((obj.AttachmentOffset.Base.x,
         obj.AttachmentOffset.Base.y,
         obj.AttachmentOffset.Base.z,
         obj.Shape.Point[0],
         obj.Shape.Point[1],
         obj.Shape.Point[2]))

    return ls
