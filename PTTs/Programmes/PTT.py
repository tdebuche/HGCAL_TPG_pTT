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
from prelim import STCtoSTCSommets
from STCtoPTT import pTTSTCs
from ModuleSumtoPTT import pTTModules

os.chdir("../../Ressources")

UV = np.load('uv.npy')
Binetaphi = np.load('Binetaphi.npy')
G = np.load('Geometry.npy')
Z = np.load('Z.npy')
STCLD = np.load('STCLD.npy')
STCHD = np.load('STCHD.npy')
etamin = 1.305
N = 16

######### PTTarray -> array(24,20,maxmodulesperPTT,5(or6)) -> 5 for CE-E (without STC indices) -> 6 for CE-H ########
############# 24 -> phi, 20 -> eta, maxmod... ok, 5 : i (numéro du module), u,v, ratio (for CEE) ##########
############# 24 -> phi, 20 -> eta, maxmod... ok, 6 : i (numéro du module), u,v, ratio, indice STC (for CEH) #######


def PTTLayer(Layer,STCyesorno):
    if Layer < 27:
        return pTTModules(G,Layer)
    else :
        if not STCyesorno:
            return pTTModules(G,Layer)       #without STCs
        if STCyesorno :
            return pTTSTCs(STCLD,STCHD,Layer)  #with STCs



def constructionPTT(Layer,STCyesorno):
    listpttpermodules = PTTLayer(Layer,STCyesorno)
    if Layer < 48 and not STCyesorno : #put 48 if without STCs
        L =[[[] for j in range(20)] for i in range(24)]
        for i in range(len(listpttpermodules)):
            for j in range(len(listpttpermodules[i])):
                iptt,jptt,ratio = listpttpermodules[i][j]
                u = UV[Layer-1,i,0]
                v = UV[Layer-1,i,1]
                L[iptt][jptt].append([i,u,v,ratio])
    if Layer < 27 and STCyesorno :   # and 27 if with STCs
        L =[[[] for j in range(20)] for i in range(24)]
        for i in range(len(listpttpermodules)):
            for j in range(len(listpttpermodules[i])):
                iptt,jptt,ratio = listpttpermodules[i][j]
                u = UV[Layer-1,i,0]
                v = UV[Layer-1,i,1]
                L[iptt][jptt].append([i,u,v,ratio])

    if Layer > 26 and STCyesorno :
        L =[[[] for j in range(20)] for i in range(24)]
        for i in range(len(listpttpermodules)):
         for j in range(len(listpttpermodules[i])):
                for k in range(len(listpttpermodules[i][j])):
                    iptt,jptt,ratio = listpttpermodules[i][j][k]
                    u = UV[Layer-1,i,0]
                    v = UV[Layer-1,i,1]
                    L[iptt][jptt].append([i,u,v,j,ratio])

    return(L)


def PTTarray(Layer,STCyesorno):
    L = constructionPTT(Layer,STCyesorno)
    max = 0
    for i in range(len(L)):
        for j in range(len(L[i])):
            if len(L[i][j]) >max:
                max = len(L[i][j])
    if Layer < 27:
        A = np.zeros((24,20,max,4))
    else :
        if not STCyesorno:
            A = np.zeros((24,20,max,4)) #without STCs
        if STCyesorno:
            A = np.zeros((24,20,max,5)) #with STCs
    for i in range(len(L)):
        for j in range(len(L[i])):
            for k in range(len(L[i][j])):
                A[i,j,k] = np.array(L[i][j][k])
    return A


###############################################################################################################################

"""
#Layer to plot
Layer = 32

zlay = Z[Layer-1]
BinXY= binetaphitoXY(Binetaphi,zlay)
Mod = G[Layer-1]
Sommets = ModulestoSommets(Mod)
BinSommets = BintoBinSommets(BinXY)
test = constructionPTT(Layer)

if Layer >33:
    STC = STCLD[Layer-34]
    STCSommets = STCtoSTCSommets(STCLD[Layer-34])
if Layer <34 :
    STC = STCHD[Layer-27]
    STCSommets = STCtoSTCSommets(STCHD[Layer-27])


plt.figure(figsize = (12,8))

#Modules
for i in range(len(Sommets)):
    plt.plot(Sommets[i][0] + [Sommets[i][0][0]],Sommets[i][1]+ [Sommets[i][1][0]], color = 'black',linewidth = 0.5)
#Bin
for i in range(len(BinXY)):
    plt.plot(BinSommets[i][0] + [BinSommets[i][0][0]],BinSommets[i][1]+ [BinSommets[i][1][0]], color = 'red',linewidth = 0.5)

for i in range(len(test)):
    for j in range(len(test[i])):
        for k in range(len(test[i][j])):
            indice = test[i][j][k][0]
            x = (Sommets[indice][0][0]+Sommets[indice][0][3])/2
            y =(Sommets[indice][1][0]+Sommets[indice][1][3])/2
            #plt.annotate('('+str(test[i][j][k][1])+','+str(test[i][j][k][2])+')',(x,y))

#STC
for i in range(len(STCSommets)):
    for j in range(len(STCSommets[i])):
        stc = STCSommets[i][j]
        plt.plot(stc[0]+[stc[0][0]],stc[1]+[stc[1][0]],linewidth = 0.2,color  = 'blue') #STC


plt.title(label =  'pTT of layer '+str(Layer))
plt.xlabel('x (mm)')
plt.ylabel('y (mm)')
plt.show()
"""
