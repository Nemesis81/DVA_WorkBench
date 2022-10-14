# -*- coding: utf-8 -*-

#DVAUtils compile dunction used in various algorythm for DVA
#list of point, storage of value 
#

import FreeCAD as app
import FreeCADGui as gui
import numpy as np



def listDvaPoints(Objs):
    """Rerurn a list of DVAPoints """
    ptList=[]
    for obj in Objs:
        if hasattr(obj, "Law"):
           ptList.append(obj.Name)
    return ptList



def listAssyConstraints(Objs):
    """Rerurn a list of Constraints upgrade in DVA constraints """
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
            dict[i]=dva + pt
        elif hasattr(b, "Law") and hasattr(b, "Distance"):
            ct= [b.Distance]
            dict[i] =dva + ct
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
    analysis = kwargs.get('analysis', "hlm")
    #https://www.udacity.com/blog/2021/10/python-match-case-statement-example-alternatives.html
    #np.random.seed(1)

    if tol!= None or tol!= 0:
       sig =  tol/6
       mu = 0
    elif sig!= None or sig!= 0:
         tol = sig*3

    if law == "Normal":
       value = np.random.normal(mu,sig)
    
    elif law == "Uniform":
         value = np.random.uniform(-tol/2, tol/2,1)
         value = value[0]
         
    return value