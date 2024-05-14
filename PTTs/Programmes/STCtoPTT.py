import numpy as np
import matplotlib.pyplot as plt
import os
from shapely.geometry import Polygon
import functions

os.chdir("/eos/user/t/tdebuche/YOURWORKINGAREA/HGCAL_TPG_pTT/ProgrammesRessources")
Binetaphi2024 = np.load('Binetaphi2024.npy')
Binetaphi2028 = np.load('Binetaphi2028.npy')
G = np.load('ModulesGeometry.npy')
Z = np.load('Z.npy')
STCLD = np.load('STCLD.npy')
STCHD = np.load('STCHD.npy')
Values2024 = np.load('ValuesBins2024.npy')
Values2028 = np.load('ValuesBins2028.npy')

N = 16

#######################Build PTTs : array(nb_modules,nb_STCs,nb_PTTs,3) (module,PTTs)-->[phiBin,etaBin,ratio]###################



def pTTSTCs(STCLD,STCHD,Layer,edges): #Répartit les énergies des modules dans les Towers pour un layer donné
    z = Z[Layer-1]
    if edges:
        BinXY= functions.binetaphitoXY(Binetaphi2028,z)
        Values = Values2028
    else :
        BinXY= functions.binetaphitoXY(Binetaphi2024,z)
        Values = Values2024
    PolyLimite = Arealimit(Layer)
    if Layer > 33:
        STC = STCLD[Layer-34]
    else :
        STC = STCHD[Layer-27]
    L = []
    l = []
    for i in range(len(STC)):
        for j in range(len(STC[i])):
            if not np.array_equal(STC[i,j],np.zeros((2,5))):
                Towers = areatocoef(pTTSTC(STC[i,j],z,BinXY,PolyLimite,edges,Values))
                l.append(Towers)
        if l != []:
            L.append(l)
        l = []
    return(L)




def Arealimit(Layer):  #Permet de regarder seulement l'air concernée par les bins
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


def pTTSTC(STC,z,BinXY,PolyLimite,edges,Values): # Renvoie les rapports [aire(intersection modulebin)/aire(module)]
    nb_binphi,nb_bineta,phimin,phimax,etamin,etamax = Values
    
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
