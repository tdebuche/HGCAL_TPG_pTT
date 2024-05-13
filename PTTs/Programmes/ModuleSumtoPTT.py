import numpy as np
import matplotlib.pyplot as plt
import os
from shapely.geometry import Polygon
from prelim import etaphitoXY
from prelim import etaphiRADtoXY
from prelim import XYtoetaphi
from prelim import polygontopoints
from prelim import pointtopolygon
from prelim import binetaphitoXY
from prelim import binetaphiRADtoXY
from prelim import etaphicentre
from prelim import ModulestoSommets
from prelim import BintoBinSommets

os.chdir("../../Ressources")

Binetaphi = np.load('Binetaphi.npy')
G = np.load('Geometry.npy')
Z = np.load('Z.npy')

etamin = 1.305
N = 16


#########################Build PTTs : array(nb_modules,nb_PTTs,3) (module,PTTs)-->[phiBin,etaBin,ratio] ########################



def pTTModules(Geometry,Layer): #Répartit les énergies des modules dans les Towers pour un layer donné
    z = Z[Layer-1]
    BinXY= binetaphitoXY(Binetaphi,z)
    PolyLimite = Arealimit(Layer)
    Modules = Geometry[Layer-1]
    L = []
    for i in range(len(Modules)):
        if not np.array_equal(Modules[i],np.zeros((2,6))):
            Towers = areatocoef(pTTModule(Modules[i],z,BinXY,PolyLimite))
            L.append(Towers)
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


def pTTModule(Module,z,BinXY,PolyLimite): # Renvoie les rapports [aire(intersection modulebin)/aire(module)]
    L = []
    Mod_Poly = pointtopolygon(Module)
    area_module = Mod_Poly.intersection(PolyLimite).area
    eta,phi = etaphicentre(Module,z)
    icentre= int(phi *36 /np.pi)
    jcentre= int((eta -etamin) *36 /np.pi)
    for i in range(-4,5):
        for j in range(-4,5):
            if (icentre+i)*20 + (jcentre+j) < len(BinXY) and (icentre+i)*20 + (jcentre+j)>= 0:
                Area = AireBinModule(Module,BinXY[(icentre+i)*20 + (jcentre+j)])
                if Area !=0:
                    L.append([icentre+i,jcentre+j,Area/area_module])
    return(L)



def AireBinModule(Module,Bin): # Renvoie [aire(intersection modulebin)/aire(module)] par bin
    M = pointtopolygon(Module)
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

#Layer to plot
Layer = 28

zlay = Z[Layer-1]
BinXY= binetaphitoXY(Binetaphi,zlay)
Mod = G[Layer-1]
Sommets = ModulestoSommets(Mod)
BinSommets = BintoBinSommets(BinXY)
PTT= pTTModules(G,Layer)

"""
plt.figure(figsize = (12,8))

#Modules
for i in range(len(Sommets)):
    plt.plot(Sommets[i][0] + [Sommets[i][0][0]],Sommets[i][1]+ [Sommets[i][1][0]], color = 'black')
#Bins
for i in range(len(BinXY)):
    plt.plot(BinSommets[i][0] + [BinSommets[i][0][0]],BinSommets[i][1]+ [BinSommets[i][1][0]], color = 'red',linewidth = '0.5')

#Edge -> Bins

#Binenplus = BintoBinSommets(binetaphitoXY(Binetaphi[420:480]-np.array([[[0,0,0,0],[2*np.pi/3,2*np.pi/3,2*np.pi/3,2*np.pi/3] ]for i in range(60)]),zlay))

#for i in range(len(Binenplus)):
#    plt.plot(Binenplus[i][0] + [Binenplus[i][0][0]],Binenplus[i][1]+ [Binenplus[i][1][0]], color = 'green')

#Values of sharing
for i in range(len(PTT)):
    for j in range(len(PTT[i])):
        p = pointtopolygon(Mod[i])
        q = pointtopolygon(BinXY[20 * PTT[i][j][0]+ PTT[i][j][1]])
        points = np.array([polygontopoints(p.intersection(q))[0],polygontopoints(p.intersection(q))[1]])
        etam,phim = etaphicentre(points,zlay)
        xm,ym = etaphitoXY(etam,phim,zlay)
        plt.annotate(str(PTT[i][j][2]),(xm,ym))



plt.title(label =  'pTT of layer '+str(Layer))
plt.xlabel('x (mm)')
plt.ylabel('y (mm)')
plt.show()"""

#Record an array with the pTTS
"""
max = 0
for i in range(len(PTT)):
    if len(PTT[i])>max:
        max = len(PTT[i])

PTTarray = np.zeros((len(PTT),max,3))
for i in range(len(PTT)):
    for j in range(len(PTT[i])):
        PTTarray[i,j] = np.array(PTT[i][j])

np.save('pTTModules_Layer' + str(Layer) +'.npy',PTTarray)"""
"""
#Record plots
os.chdir("../Ressources")
for k in range(34):
    if k<13:
        Layer = 2*k + 1
    else:
        Layer = 14 + k
    zlay = Z[Layer-1]
    BinXY= binetaphitoXY(Binetaphi,zlay)
    Mod = G[Layer-1]
    Sommets = ModulestoSommets(Mod)
    BinSommets = BintoBinSommets(BinXY)
    PTT= pTTModules(G,Layer)
    plt.figure(figsize = (36,24))

    #Modules
    for i in range(len(Sommets)):
        plt.plot(Sommets[i][0] + [Sommets[i][0][0]],Sommets[i][1]+ [Sommets[i][1][0]], color = 'black')
    #Bins
    for i in range(len(BinXY)):
        plt.plot(BinSommets[i][0] + [BinSommets[i][0][0]],BinSommets[i][1]+ [BinSommets[i][1][0]], color = 'red',linewidth = '0.5')

#Edge -> Bins

#Binenplus = BintoBinSommets(binetaphitoXY(Binetaphi[420:480]-np.array([[[0,0,0,0],[2*np.pi/3,2*np.pi/3,2*np.pi/3,2*np.pi/3] ]for i in range(60)]),zlay))

#for i in range(len(Binenplus)):
#    plt.plot(Binenplus[i][0] + [Binenplus[i][0][0]],Binenplus[i][1]+ [Binenplus[i][1][0]], color = 'green')

#Values of sharing
    for i in range(len(PTT)):
        for j in range(len(PTT[i])):
            p = pointtopolygon(Mod[i])
            q = pointtopolygon(BinXY[20 * PTT[i][j][0]+ PTT[i][j][1]])
            points = np.array([polygontopoints(p.intersection(q))[0],polygontopoints(p.intersection(q))[1]])
            etam,phim = etaphicentre(points,zlay)
            xm,ym = etaphitoXY(etam,phim,zlay)
            plt.annotate(str(PTT[i][j][2]),(xm,ym),size = 5)

    plt.title(label =  'pTT of layer '+str(Layer))
    plt.xlabel('x (mm)')
    plt.ylabel('y (mm)')
    plt.savefig('pTT of layer '+str(Layer)+' with energies' + '.png')"""