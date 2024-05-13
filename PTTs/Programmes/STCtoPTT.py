import numpy as np
import matplotlib.pyplot as plt
import os
from shapely.geometry import Polygon
from functions import etaphitoXY
from functions import etaphiRADtoXY
from functions import XYtoetaphi
from functions import polygontopoints
from functions import pointtopolygon
from functions import binetaphitoXY
from functions import binetaphiRADtoXY
from functions import etaphicentre
from functions import ModulestoVertices
from functions import BintoBinVertices
from functions import STCtoSTCVertices

os.chdir("../../ProgrammesRessources")

Binetaphi = np.load('Binetaphi2024.npy')
#Binetaphi = np.load('Binetaphi2028.npy')
G = np.load('Geometry.npy')
Z = np.load('Z.npy')
STCLD = np.load('STCLD.npy')
STCHD = np.load('STCHD.npy')
etamin = 1.305
N = 16

#######################Build PTTs : array(nb_modules,nb_STCs,nb_PTTs,3) (module,PTTs)-->[phiBin,etaBin,ratio]###################



def pTTSTCs(STCLD,STCHD,Layer): #Répartit les énergies des modules dans les Towers pour un layer donné
    z = Z[Layer-1]
    BinXY= binetaphitoXY(Binetaphi,z)
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
                Towers = areatocoef(pTTSTC(STC[i,j],z,BinXY,PolyLimite))
                l.append(Towers)
        if l != []:
            L.append(l)
        l = []
    return(L)




def Arealimit(Layer):  #Permet de regarder seulement l'air concernée par les bins
    Limite = np.zeros((2,50))
    z = Z[Layer-1]
    for i in range(25):
        x,y = etaphitoXY(etamin,i*np.pi/36,z)
        Limite[0,i] = x
        Limite[1,i] = y
        x,y = etaphitoXY(etamin +20 * np.pi/36,(24-i)*np.pi/36,z)
        Limite[0,i+25] = x
        Limite[1,i+25] = y
    PolyLimite = pointtopolygon(Limite)
    return PolyLimite


def pTTSTC(STC,z,BinXY,PolyLimite): # Renvoie les rapports [aire(intersection modulebin)/aire(module)]
    L = []
    STC_Poly = pointtopolygon(STC)
    AreaSTC = STC_Poly.area
    eta,phi = etaphicentre(STC,z)
    icentre= int(phi *36 /np.pi)
    jcentre= int((eta -etamin) *36 /np.pi)
    for i in range(-4,5):
        for j in range(-4,5):
            if (icentre+i)*20 + (jcentre+j) < len(BinXY) and (icentre+i)*20 + (jcentre+j)>= 0:
                Area = AireBinModule(STC,BinXY[(icentre+i)*20 + (jcentre+j)])
                if Area !=0:
                    L.append([icentre+i,jcentre+j,Area/AreaSTC])
    return(L)



def AireBinModule(STC,Bin): # Renvoie [aire(intersection modulebin)/aire(module)] par bin
    M = pointtopolygon(STC)
    B = pointtopolygon(Bin)
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



################################################################################################################################
"""
#Layer to plot
Layer = 27

zlay = Z[Layer-1]
BinXY= binetaphitoXY(Binetaphi,zlay)
Mod = G[Layer-1]
ModuleVertices = ModulestoVertices(Mod)
BinVertices = BintoBinVertices(BinXY)

if Layer >33:
    STC = STCLD[Layer-34]
    STCVertices = STCtoSTCSommets(STCLD[Layer-34])
if Layer <34 :
    STC = STCHD[Layer-27]
    STCVertices = STCtoSTCSommets(STCHD[Layer-27])

PTT= pTTSTCs(STCLD,STCHD,Layer)



plt.figure(figsize = (12,8))

#Modules
for i in range(len(ModuleVertices)):
    plt.plot(ModuleVertices[i][0] + [ModuleVertices[i][0][0]],ModuleVertices[i][1]+ [ModuleVertices[i][1][0]], color = 'black',linewidth = 0.5)
#Bin
for i in range(len(BinVertices)):
    plt.plot(BinVertices[i][0] + [BinVertices[i][0][0]],BinVertices[i][1]+ [BinVertices[i][1][0]], color = 'red',linewidth = 0.5)

for i in range(len(STCVertices)):
    for j in range(len(STCVertices[i])):
            stc = STCSommets[i][j]
            plt.plot(stc[0]+[stc[0][0]],stc[1]+[stc[1][0]],linewidth = 0.2,color  = 'blue') #STC
    if not np.array_equal(STC[i,j],np.zeros((2,5))):
        for k in range(len(PTT[i][j])):
            p = pointtopolygon(STC[i,j])
            q = pointtopolygon(BinXY[20 * PTT[i][j][k][0]+ PTT[i][j][k][1]])
            points = np.array([polygontopoints(p.intersection(q))[0],polygontopoints(p.intersection(q))[1]])
            etam,phim = etaphicentre(points,zlay)
            xm,ym = etaphitoXY(etam,phim,zlay)                
            plt.annotate(str(PTT[i][j][k][2]),(xm,ym))



plt.title(label =  'pTT of layer '+str(Layer))
plt.xlabel('x (mm)')
plt.ylabel('y (mm)')

#plt.xlim(400,650)
#plt.ylim(100,300)
plt.show()"""
