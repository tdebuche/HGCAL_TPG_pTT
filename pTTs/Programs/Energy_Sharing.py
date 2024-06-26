import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import pTTs.Programs.functions as functions

Binetaphi2024 = np.load('src/Binetaphi2024.npy')
Binetaphi2028 = np.load('src/Binetaphi2028.npy')
Z = np.load('src/Z.npy')
Values2024 = np.load('src/ValuesBins2024.npy')
Values2028 = np.load('src/ValuesBins2028.npy')
                     

N = 16 #energies divided by N (for the sharing)
etamin = 1.305

def reverse_pTTs(args,Layer,Modules,STCs):
    if Layer < 27 or (Layer>=27 and not args.STCs):
        pTTs = pTT_single_layer(args,Layer,Modules)
    else :
        pTTs = pTT_single_layer(args,Layer,STCs)
    if args.Edges == "yes": Values = Values2028
    else : Values = Values2024
    nb_binphi,nb_bineta,phimin,phimax,etamin,etamax = Values
    nb_binphi,nb_bineta = int(nb_binphi),int(nb_bineta)

    reversed_pTTs = [[[] for j in range(nb_bineta)] for i in range(nb_binphi)]                  
    for module_idx in range(len(pTTs)):
        Module = pTTs[module_idx][0]
        for bin_idx in range(len(pTTs[module_idx][1])):
            phi,eta,ratio = pTTs[module_idx][1][bin_idx]
            if args.STCs and Layer >26 :
                reversed_pTTs[phi][eta].append([Module['type'],Module['u'],Module['v'],Module['index'],ratio])
            if Layer < 27 or (Layer>=27 and not args.STCs) :
                reversed_pTTs[phi][eta].append([Module['type'],Module['u'],Module['v'],ratio])
    return(reversed_pTTs)


def pTT_single_layer(args,Layer,Modules): #Share the energy of each module pf one layer
    #choose the scenario
    if args.Edges == "yes":
        BinXY= functions.binetaphitoXY(Binetaphi2028,Z[Layer-1])
        Values = Values2028
    else :
        BinXY= functions.binetaphitoXY(Binetaphi2024,Z[Layer-1])
        Values = Values2024
    Modules = Modules[Layer-1]
    
    #create a list with the enegy sharing
    Bins_per_Modules = []
    for module_idx in range(len(Modules)):
        Module_vertices = [Modules[module_idx]['verticesX'],Modules[module_idx]['verticesY']]
        Bins = areatocoef(pTT_single_Module(BinXY,Module_vertices,Values,Z[Layer-1]))
        Bins_per_Modules.append([Modules[module_idx],Bins])
    return(Bins_per_Modules)




def pTT_single_Module(BinXY,Module,Values,z): # Return the sharing of the energy of each module
    nb_binphi,nb_bineta,phimin,phimax,etamin,etamax = Values
    nb_binphi,nb_bineta = int(nb_binphi),int(nb_bineta)
    pTTs = []
    Module_Polygon = functions.pointtopolygon(Module)
    area_module = Module_Polygon.area
    eta,phi = functions.etaphicentre(Module,z)
    phi_center = int((phi-phimin) *36 /np.pi)
    eta_center = int((eta -etamin) *36 /np.pi)
    for phi in range(-4,5):
        for eta in range(-4,5):
            phi_idx = phi_center + phi
            eta_idx = eta_center + eta
            if phi_idx >= 0 and phi_idx < nb_binphi:
                if eta_idx >= 0 and eta_idx < nb_bineta:
                    Area = AireBinModule(Module,BinXY[(phi_idx)*20 + (eta_idx)])
                    if Area !=0:
                        pTTs.append([phi_idx,eta_idx,Area/area_module])
    return(pTTs)



def AireBinModule(Module,Bin): # Return [area(intersection module and bin)] for a given module and a given bin
    Module = functions.pointtopolygon(Module)
    Bin = functions.pointtopolygon(Bin)
    if Module.intersects(Bin):
        return(Module.intersection(Bin).area)
    else :
        return(0)



def areatocoef(Areas): # Convert overlap area into fraction of 16
    L =[]
    reste = []
    coef = 0
    total = 0
    sum = 0
    if Areas == []:
        return([])
    for i in range(len(Areas)):
        coef = int(N *Areas[i][2])
        L.append([Areas[i][0],Areas[i][1],coef])
        total += coef
        reste.append((Areas[i][2] - coef/N))
        sum += coef
    x = 0
    indicex = 0
    while sum != N:
        x = 0
        for i in range(len(Areas)):
            if reste[i] > x:
                indicex = i
                x = reste[i]
        L[indicex][2] += 1
        reste[indicex] = reste[indicex] - 1/N
        sum +=1
    COEF = []
    for i in range(len(Areas)):
        if  L[i][2] != 0:
            COEF.append(L[i])
    return COEF


