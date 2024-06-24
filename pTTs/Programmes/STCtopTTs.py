import numpy as np
import matplotlib.pyplot as plt
import os
from shapely.geometry import Polygon
import functions
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path+"/../../ProgrammesRessources")
Binetaphi2024 = np.load('Binetaphi2024.npy')
Binetaphi2028 = np.load('Binetaphi2028.npy')
Z = np.load('Z.npy')
Values2024 = np.load('ValuesBins2024.npy')
Values2028 = np.load('ValuesBins2028.npy')

N = 16
etamin = 1.305
#######################Build PTTs : array(nb_modules,nb_STCs,nb_PTTs,3) (module,PTTs)-->[phiBin,etaBin,ratio]###################



def pTT_single_STC_layer(args,Layer,STCs): 
    if edges:
        BinXY= functions.binetaphitoXY(Binetaphi2028,Z[Layer-1])
        Values = Values2028
    else :
        BinXY= functions.binetaphitoXY(Binetaphi2024,Z[Layer-1])
        Values = Values2024
    STCs = STCs[Layer-1]
    L = []
    l = []
    for i in range(len(STCs)):
        for j in range(len(STCs[i])):
            pTTs_single_STC= areatocoef(pTT_single_STC(STCs[i][j],z,BinXY,edges,Values))
            l.append(pTTs_single_STC)
        if l != []:
            L.append(l)
        else: print('STC without pTTs')
        l = []
    return(L)






def pTT_single_STC(STC,z,BinXY,edges,Values):
    nb_binphi,nb_bineta,phimin,phimax,etamin,etamax = Values
    nb_binphi,nb_bineta = int(nb_binphi),int(nb_bineta)
    
    L = []
    STC_Poly = functions.pointtopolygon(STC)
    AreaSTC = STC_Poly.area
    eta,phi = functions.etaphicentre(STC,z)
    icentre= int((phi-phimin) *36 /np.pi)
    jcentre= int((eta -etamin) *36 /np.pi)
    for i in range(-4,5):
        for j in range(-4,5):
            if icentre+i >= 0 and icentre+i < nb_binphi:
                if jcentre+j >= 0 and jcentre+j < nb_bineta:
                    Area = AireBinModule(STC,BinXY[(icentre+i)*20 + (jcentre+j)])
                    if Area !=0:
                        L.append([icentre+i,jcentre+j,Area/AreaSTC])
    return(L)



def AireBinModule(STC,Bin): # Renvoie [aire(intersection modulebin)/aire(module)] par bin
    M = functions.pointtopolygon(STC)
    B = functions.pointtopolygon(Bin)
    if M.intersects(B):
        return(M.intersection(B).area)
    else :
        return(0)



def areatocoef(Areas): # Transforme les rapports d'aires en multiple de 1/16
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
