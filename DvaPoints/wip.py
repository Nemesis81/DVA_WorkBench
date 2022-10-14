



def inputMuSig(tolerance):
    sig =  tol/6
    mu = 0
    return sig
    
def inputSig(sig):
    tol = sig*3
    return tol
    
def normalLaw(mu,sig):
    
    value = np.random.normal(mu,sig)
    return value

def uniformLam(mu,sig):
    
    value = np.random.uniform(-tol/2, tol/2,1)
    value = value[0]
    return value