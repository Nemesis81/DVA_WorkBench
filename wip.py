for i in CstrValues:
    for i2 in i:
        i2=i2.joint(i2)
        
Repet = 10

CstrValues = np.zeros((Repet, len(Contraintes)),dtype=float)
dvaPtValues = []
AllValues = []
CstrValue=[]

for x in np.arange(0, Repet, 1):
    CstrValues = []
    print(CstrValues)
    for Cstr in Contraintes:
        Variation =  Doc.getObject(Cstr) 
        Print(Variation)
        Variation.Distance = str(dvu.affectValue(Variation.Law, tolerance= Variation.Tolerance))
        Print(Variation.Distance)
        CstrValues.append((Cstr, float(Variation.Distance)))
        print (Cstr, "with value", float(Variation.Distance))
        
CstrValues.append([x, Variation.Label, Variation.Distance])