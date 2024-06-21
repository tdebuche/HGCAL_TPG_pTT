import numpy as np
import matplotlib.pyplot as plt
import os
from shapely.geometry import Polygon
import functions
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path + "/../../ProgrammesRessources")

Binetaphi2024 = np.load('Binetaphi2024.npy')
Binetaphi2028 = np.load('Binetaphi2028.npy')
Z = np.load('Z.npy')
Values2024 = np.load('ValuesBins2024.npy')
Values2028 = np.load('ValuesBins2028.npy')
                     

N = 16 #energies divided by N (for the sharing)
etamin = 1.305
#########################Build PTTs : array(nb_modules,nb_PTTs,3) (module,PTTs)-->[phiBin,etaBin,ratio] ########################



def pTTModules(Geometry,Layer,edges): #Share the energy of each module
    z = Z[Layer-1]
    if edges:
        BinXY= functions.binetaphitoXY(Binetaphi2028,z)
        Values = Values2028
    else :
        BinXY= functions.binetaphitoXY(Binetaphi2024,z)
        Values = Values2024
    PolyLimite = Arealimit(Layer)
    Modules = Geometry[Layer-1]
    L = []
    for i in range(len(Modules)):
        if not np.array_equal(Modules[i],np.zeros((2,6))):
            Towers = areatocoef(pTTModule(Modules[i],z,BinXY,PolyLimite,edges,Values))
            L.append(Towers)
    return(L)




def Arealimit(Layer):  #Look at the area covered by bins only (avoid the edges problems in 20**24 configuration)
    Limite = np.zeros((2,50))
    z = Z[Layer-1]
    for i in range(25):
        x,y = functions.etaphitoXY(etamin,i*np.pi/36,z)
        Limite[0,i] = x
        Limite[1,i] = y
        x,y = functions.etaphitoXY(etamin +20 * np.pi/36,(24-i)*np.pi/36,z)
        Limite[0,i+25] = x
        Limite[1,i+25] = y
    PolyLimite = functions.pointtopolygon(Limite)
    return PolyLimite


def pTTModule(Module,z,BinXY,PolyLimite,edges,Values): # Return the sharing of the energy of each module
    nb_binphi,nb_bineta,phimin,phimax,etamin,etamax = Values
    nb_binphi,nb_bineta = int(nb_binphi),int(nb_bineta)
    L = []
    Mod_Poly = functions.pointtopolygon(Module)
    if not edges:
        area_module = Mod_Poly.intersection(PolyLimite).area
    if edges:
        area_module = Mod_Poly.area
    eta,phi = functions.etaphicentre(Module,z)
    icentre= int((phi-phimin) *36 /np.pi)
    jcentre= int((eta -etamin) *36 /np.pi)
    for i in range(-4,5):
        for j in range(-4,5):
            if icentre+i >= 0 and icentre+i < nb_binphi:
                if jcentre+j >= 0 and jcentre+j < nb_bineta:
                    Area = AireBinModule(Module,BinXY[(icentre+i)*20 + (jcentre+j)])
                    if Area !=0:
                        L.append([icentre+i,jcentre+j,Area/area_module])
    return(L)



def AireBinModule(Module,Bin): # Return [area(intersection module and bin)/area(module)] for a given module and a given bin
    M = functions.pointtopolygon(Module)
    B = functions.pointtopolygon(Bin)
    if M.intersects(B):
        return(M.intersection(B).area)
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


