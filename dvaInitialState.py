# -*- coding: utf-8 -*-

#DVAUtils compile dunction used in various algorythm for DVA
#list of point, storage of value 
#

import FreeCAD as app
import FreeCADGui as gui
import DVAUtils as dvu

doc= FreeCAD.ActiveDocument
DvaPts = doc.findObjects("PartDesign::Point")
DvaPts = dvu.listDvaPoints(DvaPts)
Contraintes = doc.findObjects("App::FeaturePython")
Contraintes = dvu.listAssyConstraints(Contraintes)

allVariation = Contraintes + DvaPts
initialState = {}

dict = {}
c = 0
for i in test:
    b=doc.getObject(test[c])
    dict[i]=(b.Law,
             b.Tolerance, 
             b.Meanshift, 
             b.Sd)
    if b.TypeId != 'App::FeaturePython':
        dict[i]+= (b.AttachmentOffset.Base.x,
                    b.AttachmentOffset.Base.y,
                    b.AttachmentOffset.Base.z)
    elif b.TypeId != 'PartDesign::Point':
        dict[i]+= b.Distance
    c+=1
    
    
